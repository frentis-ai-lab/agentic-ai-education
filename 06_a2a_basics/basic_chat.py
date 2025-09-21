"""AutoGen group chat a2a demo."""

from __future__ import annotations

import os
from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent


def build_llm_config() -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 환경 변수가 필요합니다.")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return {
        "config_list": [
            {
                "model": model_name,
                "api_key": api_key,
            }
        ],
        "temperature": 0.2,
    }


def main() -> None:
    llm_config = build_llm_config()

    planner = AssistantAgent(
        name="planner",
        llm_config=llm_config,
        system_message=(
            "너는 프로젝트 플래너야. 요청을 분석해서 필요한 단계들을 정의하고, "
            "각 단계에 대해 작가 에이전트에게 넘길 지시문을 작성해."
        ),
    )

    writer = AssistantAgent(
        name="writer",
        llm_config=llm_config,
        system_message=(
            "너는 이메일 카피라이터야. planner가 준 지시문을 바탕으로, "
            "3단락 이내의 이메일을 작성하고 받은 피드백을 반영해."
        ),
    )

    reviewer = UserProxyAgent(
        name="reviewer",
        human_input_mode="NEVER",
        default_auto_reply=(
            "두 에이전트가 합의하면 'APPROVED'라고 말하고, 결과만 요약해서 알려줘."
        ),
        description="최종 결과를 확인하는 자동화된 리뷰어",
        llm_config=llm_config,
    )

    group = GroupChat(
        agents=[planner, writer, reviewer],
        messages=[],
        max_round=6,
    )

    manager = GroupChatManager(groupchat=group, llm_config=llm_config)

    reviewer.initiate_chat(
        manager,
        message=(
            "신규 Agentic 교육 론칭을 알리는 환영 이메일을 작성해. "
            "planner가 구조를 잡고 writer가 본문을 작성해야 해."
        ),
    )


if __name__ == "__main__":
    main()
