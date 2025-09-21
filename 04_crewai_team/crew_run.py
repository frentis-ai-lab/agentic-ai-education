"""CrewAI demo: marketer → human sales → mailer collaboration."""

from __future__ import annotations

import argparse
import os
from crewai import Agent, Crew, Process, Task


def build_agents(model_name: str) -> tuple[Agent, Agent, Agent]:
    marketer = Agent(
        role="Growth Marketer",
        goal="새로운 Agentic AI 교육 과정을 홍보할 시장 진입 전략을 만든다.",
        backstory=(
            "다양한 SaaS 스타트업 캠페인을 런칭한 경험이 있으며, "
            "데이터 기반 메시지 구성을 좋아한다."
        ),
        llm=model_name,
        verbose=True,
    )

    sales = Agent(
        role="Account Executive",
        goal="마케터의 초안을 검토하고 실제 고객 상황에 맞게 조정한다.",
        backstory="고객사와 밀접하게 일하며, 톤앤매너와 일정 현실성을 중요하게 본다.",
        llm=model_name,
        verbose=False,
        allow_delegation=False,
    )

    mailer = Agent(
        role="Email Copywriter",
        goal="확정된 메시지를 기반으로 짧고 명확한 이메일 초안을 완성한다.",
        backstory="B2B 세일즈 이메일을 5년 넘게 작성한 전문 메일러.",
        llm=model_name,
        verbose=True,
    )

    return marketer, sales, mailer


def build_tasks(marketer: Agent, sales: Agent, mailer: Agent) -> tuple[Task, Task, Task]:
    brief = Task(
        name="시장 요약",
        description=(
            "제품 '{{product}}'을(를) '{{audience}}'에게 소개하기 위한 핵심 메시지와 "
            "3개의 실행 아이디어를 정리하세요."
        ),
        expected_output="bullet point 목록으로 핵심 메시지 3개와 실행 아이디어 3개를 제시",
        agent=marketer,
    )

    sales_review = Task(
        name="영업 검토",
        description=(
            "마케터가 작성한 시장 요약을 검토하고 실제 고객 관점에서 수정 제안 2가지를 남기세요.\n"
            "현장 일정, 주요 이해관계자, 제안 수위를 고려합니다."
        ),
        expected_output="현실성을 높이기 위한 수정 제안 2가지 (문장형)",
        agent=sales,
        context=[brief],
        human_input=True,
    )

    email = Task(
        name="이메일 초안",
        description=(
            "최종 이메일 초안을 작성하세요.\n"
            "- 대상: '{{audience}}' 세그먼트 고객\n"
            "- 제품: '{{product}}'\n"
            "- 마케터 요약과 영업 의견을 모두 반영\n"
            "- 제목과 본문(3단락 이내) 포함"
        ),
        expected_output="제목과 본문이 포함된 이메일 초안",
        agent=mailer,
        context=[brief, sales_review],
    )

    return brief, sales_review, email


def run(product: str, audience: str, model_name: str) -> str:
    marketer, sales, mailer = build_agents(model_name)
    brief, sales_review, email = build_tasks(marketer, sales, mailer)

    crew = Crew(
        agents=[marketer, sales, mailer],
        tasks=[brief, sales_review, email],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"product": product, "audience": audience})
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="CrewAI 마케팅 이메일 협업 예제")
    parser.add_argument("product", nargs="?", default="Agentic AI 교육 과정")
    parser.add_argument("audience", nargs="?", default="B2B 마케팅 담당자")
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        help="사용할 LLM 이름(OpenAI 호환)",
    )
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY 환경 변수를 설정해 주세요.")

    summary = run(args.product, args.audience, args.model)
    print("\n=== 최종 이메일 ===\n")
    print(summary)


if __name__ == "__main__":
    main()
