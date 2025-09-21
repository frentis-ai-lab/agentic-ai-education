"""FastMCP server exposing marketing helper tools."""

from __future__ import annotations

import random
from datetime import date, timedelta

from fastmcp import FastMCP

app = FastMCP(
    name="langchain-mcp",
    instructions="Marketing insight server providing campaign data and email outlines.",
)

SEGMENT_TRENDS = {
    "교육 담당자": [
        "사내 온보딩 자동화에 관심이 높음",
        "AI 윤리 가이드라인 교육 컨텐츠 수요 증가",
        "MZ 세대 학습자 경험에 집중하는 추세",
    ],
    "마케터": [
        "캠페인 ROI와 빠른 실험 반복을 강조",
        "1분 이하 숏폼 학습 콘텐츠 선호",
        "LLM 기반 개인화 이메일이 높은 클릭률 기록",
    ],
}


@app.tool
def campaign_compass(product: str, launch_window_weeks: int = 6) -> dict[str, str]:
    """Return a lightweight launch plan with suggested kickoff and messaging angle."""

    start = date.today() + timedelta(weeks=1)
    kickoff = start.strftime("%Y-%m-%d")
    launch = (start + timedelta(weeks=launch_window_weeks)).strftime("%Y-%m-%d")
    angle = random.choice(
        [
            "파일럿 성공 사례를 강조",
            "온보딩 시간을 40% 단축",
            "실무형 실습으로 빠른 ROI",
        ]
    )
    return {
        "product": product,
        "kickoff": kickoff,
        "target_launch": launch,
        "angle": angle,
    }


@app.tool
def audience_scanner(segment: str) -> dict[str, list[str]]:
    """Summarise audience motivations and objections."""

    trends = SEGMENT_TRENDS.get(segment, ["최근 데이터가 부족합니다. 실사용자 인터뷰가 필요합니다."])
    objections = [
        "예산 대비 효과가 명확한지",
        "팀원 학습 시간 확보가 가능한지",
        "기존 시스템과의 통합 난이도",
    ]
    return {"segment": [segment], "trends": trends, "objections": objections}


@app.tool
def email_blueprint(product: str, segment: str, ask: str) -> dict[str, list[str]]:
    """Generate a subject and outline for a warm outreach email."""

    subject = f"{segment} 전용 {product} 빠른 소개"
    intro = f"안녕하세요, {segment}를 위해 준비한 {product} 주요 내용 공유드립니다."
    body = [
        "최근 유사 조직에서의 성과와 핵심 지표 요약",
        "팀 구성원이 바로 활용할 수 있는 실습 모듈 강조",
        f"다음 주 20분 미팅 제안 및 {ask} 요청",
    ]
    closing = "필요하시면 데모 계정과 교육 자료 샘플을 바로 전달드리겠습니다."
    return {"subject": [subject], "paragraphs": [intro, *body, closing]}


if __name__ == "__main__":  # pragma: no cover
    app.run()
