"""AutoGen a2a demo with mem0-backed personal profile agent."""

from __future__ import annotations

import json
import os
from typing import Annotated

from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent
from mem0 import MemoryClient

USER_ID = "lecture-student"


def ensure_memories(client: MemoryClient) -> None:
    seed_facts = [
        "나는 서울 강남에서 일하고 매주 수요일 오전에 교육 세션을 연다.",
        "내 직함은 Enablement Lead이고 5월에 Agentic 교육 론칭을 준비 중이다.",
        "올해 목표는 파트너사 10곳에 Agentic 파일럿을 확산하는 것이다.",
        "취미는 주말 등산과 보드게임 모임이다.",
    ]
    for fact in seed_facts:
        client.add(messages=[{"role": "user", "content": fact}], user_id=USER_ID)


def build_llm_config() -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 환경 변수를 설정해 주세요.")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return {
        "config_list": [
            {
                "model": model_name,
                "api_key": api_key,
            }
        ],
        "temperature": 0.1,
    }


def main() -> None:
    mem0_key = os.getenv("MEM0_API_KEY")
    if not mem0_key:
        raise RuntimeError("MEM0_API_KEY 환경 변수를 설정해 주세요 (https://docs.mem0.ai).")

    client = MemoryClient(api_key=mem0_key)
    ensure_memories(client)

    llm_config = build_llm_config()

    controller = UserProxyAgent(
        name="controller",
        human_input_mode="NEVER",
        default_auto_reply="요청과 결과만 중계하세요.",
        description="도구 실행과 대화 흐름을 관리하는 컨트롤러",
        llm_config=llm_config,
    )

    profile_agent = AssistantAgent(
        name="profile",
        llm_config=llm_config,
        system_message=(
            "너는 개인 비서야. 사용자의 장기 기억(mem0)에 접근할 수 있어. "
            "기억을 조회하는 툴을 적극적으로 사용해 질문에 답해."
        ),
    )

    campaign_agent = AssistantAgent(
        name="campaign",
        llm_config=llm_config,
        system_message=(
            "너는 캠페인 설계자야. profile 에이전트가 주는 정보를 바탕으로 "
            "맞춤형 온보딩 이메일 개요를 작성해."
        ),
    )

    @controller.register_for_execution()
    @profile_agent.register_for_llm(
        name="search_profile",
        description="mem0에 저장된 사용자 정보를 자연어로 검색합니다.",
    )
    def search_profile(query: Annotated[str, "찾고 싶은 사용자 정보"] = "") -> str:
        results = client.search(query, user_id=USER_ID, top_k=3)
        return json.dumps(results, ensure_ascii=False, indent=2)

    group = GroupChat(
        agents=[controller, profile_agent, campaign_agent],
        messages=[],
        max_round=8,
    )
    manager = GroupChatManager(groupchat=group, llm_config=llm_config)

    controller.initiate_chat(
        manager,
        message=(
            "profile 에이전트는 사용자의 백그라운드를 조사하고, "
            "campaign 에이전트는 그 정보를 활용해 맞춤형 온보딩 이메일 개요를 작성해."
        ),
    )


if __name__ == "__main__":
    main()
