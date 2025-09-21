"""CrewAI-backed agent server that speaks the A2A-style JSON protocol."""

from __future__ import annotations

import os
from typing import Any

from crewai import Agent, Crew, Process, Task
from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

APP_NAME = "crew-marketer"


class MessageRecord(BaseModel):
    sender: str
    message: str


class A2ARequest(BaseModel):
    conversation_id: str
    sender: str
    message: str
    history: list[MessageRecord] = Field(default_factory=list)


class A2AResponse(BaseModel):
    reply: str
    agent: str = APP_NAME
    meta: dict[str, Any] = Field(default_factory=dict)


def build_agent() -> Agent:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model_name, temperature=0.2)
    return Agent(
        role="Growth Strategist",
        goal="신규 Agentic 교육 과정의 시장 진입 전략을 신속하게 도출한다.",
        backstory=(
            "다양한 SaaS 런칭 경험을 갖춘 마케터로서, 제품 포지셔닝과 실행 아이디어를 "
            "명확한 아웃라인으로 정리한다."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


agent = build_agent()
app = FastAPI(title="CrewAI A2A Agent", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metadata")
def metadata() -> dict[str, Any]:
    return {
        "agent": APP_NAME,
        "framework": "CrewAI",
        "description": "Strategic marketer that drafts launch plans for Agentic AI offerings.",
        "expected_output": "bullet outline with campaign focus and suggested next steps",
    }


@app.post("/a2a/message", response_model=A2AResponse)
def handle_message(payload: A2ARequest) -> A2AResponse:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY 환경 변수가 필요합니다.")

    history_text = "\n".join(
        f"- {record.sender}: {record.message}" for record in payload.history
    )
    prompt = (
        "당신은 Agentic AI 교육 과정의 마케팅 리더입니다. \n"
        "대화 기록:\n"
        f"{history_text or '- (이전 대화 없음)'}\n\n"
        f"새 요청({payload.sender}): {payload.message}\n"
        "실행이 가능한 전략 개요를 bullet point로 3~4개 제안하고, "
        "마지막에 다음 행동 항목을 2개 정리하세요."
    )

    dynamic_task = Task(
        description=prompt,
        expected_output="실행 전략 bullet + action items",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[dynamic_task],
        process=Process.sequential,
        verbose=False,
    )
    try:
        result = crew.kickoff()
    except Exception as exc:  # pragma: no cover - surface helpful error
        raise HTTPException(status_code=500, detail=f"Crew 실행 중 오류: {exc}") from exc

    reply_text = str(result)
    return A2AResponse(reply=reply_text, meta={"history_items": len(payload.history)})


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
