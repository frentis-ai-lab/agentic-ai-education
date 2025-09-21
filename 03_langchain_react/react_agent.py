"""LangChain ReAct agent that consults simple marketing helper tools."""

import os

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

load_dotenv()


PRODUCT_SNAPSHOTS: dict[str, str] = {
    "에이전틱 교육": "AI 에이전트 빌딩 기초와 실습을 묶은 4주 프로그램",
    "프리미엄 플랜": "기업 맞춤 Agentic AI 전략 컨설팅",
}

SEGMENT_GUIDES: dict[str, str] = {
    "마케터": "ROI, 실행 가능성, 캠페인 캘린더를 강조하세요.",
    "교육 담당자": "학습 효율, 비용 절감, 인증 코스를 강조하세요.",
}


def get_product_snapshot(name: str) -> str:
    return PRODUCT_SNAPSHOTS.get(name, "제품 정보를 찾을 수 없습니다.")


def get_segment_tip(segment: str) -> str:
    return SEGMENT_GUIDES.get(segment, "해당 세그먼트용 템플릿이 없습니다.")


def last_campaign_result(_: str) -> str:
    return "작년 봄: 이메일 캠페인 CTR 18%, 전환율 6% 기록"


def build_agent() -> ChatOpenAI:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model_name, temperature=0.2)


def run_demo() -> None:
    llm = build_agent()
    tools = [
        Tool(
            name="ProductSnapshot",
            description="제품명을 받아 핵심 특징을 알려줍니다.",
            func=get_product_snapshot,
        ),
        Tool(
            name="SegmentTip",
            description="세그먼트명을 받아 커뮤니케이션 팁을 제공합니다.",
            func=get_segment_tip,
        ),
        Tool(
            name="CampaignHistory",
            description="최근 캠페인 결과 요약을 조회합니다.",
            func=last_campaign_result,
        ),
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    prompt = (
        "프리미엄 플랜을 교육 담당자에게 이메일로 소개하려고 해요. "
        "지난 캠페인 성과를 참고해 간단한 제안서를 요약해 주세요."
    )
    response = agent.run(prompt)
    print("\n최종 답변:\n", response)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY 환경 변수를 설정해 주세요.")
    run_demo()
