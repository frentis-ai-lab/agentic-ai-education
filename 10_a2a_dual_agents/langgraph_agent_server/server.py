"""LangGraph-backed agent server that consumes Crew output and drafts emails."""

from __future__ import annotations

import os
from typing import Any, Annotated, TypedDict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

APP_NAME = "langgraph-writer"
SYSTEM_PROMPT = (
    "You are an email copywriter who receives planning notes from a marketing strategist.\n"
    "Write concise onboarding emails (subject + body with 2-3 short paragraphs) that personalize the tone."
)


class EmailState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


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


load_dotenv()


def build_graph() -> StateGraph:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model_name, temperature=0.1)

    def call_model(state: EmailState) -> dict[str, list[BaseMessage]]:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    workflow = StateGraph(EmailState)
    workflow.add_node("writer", call_model)
    workflow.set_entry_point("writer")
    workflow.add_edge("writer", END)
    return workflow.compile()


def convert_history(records: list[MessageRecord]) -> list[BaseMessage]:
    messages: list[BaseMessage] = [SystemMessage(content=SYSTEM_PROMPT)]
    for record in records:
        messages.append(HumanMessage(content=f"{record.sender}: {record.message}"))
    return messages


graph = build_graph()
app = FastAPI(title="LangGraph A2A Agent", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metadata")
def metadata() -> dict[str, Any]:
    return {
        "agent": APP_NAME,
        "framework": "LangGraph",
        "description": "Turns strategy notes into structured onboarding emails.",
        "expected_output": "Subject line and warm onboarding email body.",
    }


@app.post("/a2a/message", response_model=A2AResponse)
def handle_message(payload: A2ARequest) -> A2AResponse:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY 환경 변수가 필요합니다.")

    history_messages = convert_history(payload.history)
    history_messages.append(HumanMessage(content=f"{payload.sender}: {payload.message}"))

    try:
        result = graph.invoke({"messages": history_messages})
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"LangGraph 실행 오류: {exc}") from exc

    reply_msg = result["messages"][-1]
    return A2AResponse(reply=reply_msg.content, meta={"history_items": len(payload.history)})


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8002, reload=True)
