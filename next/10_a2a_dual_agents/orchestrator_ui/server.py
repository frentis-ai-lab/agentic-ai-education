"""Minimal HTML UI orchestrating CrewAI & LangGraph agents using an A2A-style loop."""

from __future__ import annotations
import os
import uuid
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

load_dotenv()

CREW_AGENT_URL = os.getenv("CREW_AGENT_URL", "http://localhost:8001")
LANGGRAPH_AGENT_URL = os.getenv("LANGGRAPH_AGENT_URL", "http://localhost:8002")

app = FastAPI(title="A2A Orchestrator UI", version="0.1.0")
templates = Jinja2Templates(directory="templates")


class StepRequest(BaseModel):
    conversation_id: str
    message: str = Field(min_length=1)


class StepResponse(BaseModel):
    conversation_id: str
    history: list[dict[str, str]]


sessions: dict[str, list[dict[str, str]]] = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/start")
async def start_conversation() -> JSONResponse:
    conversation_id = uuid.uuid4().hex
    sessions[conversation_id] = []
    return JSONResponse({"conversation_id": conversation_id, "history": []})


async def call_agent(
    agent_url: str,
    conversation_id: str,
    sender: str,
    message: str,
    history: list[dict[str, str]],
) -> dict[str, Any]:
    payload = {
        "conversation_id": conversation_id,
        "sender": sender,
        "message": message,
        "history": history,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{agent_url}/a2a/message", json=payload)
    response.raise_for_status()
    return response.json()


@app.post("/api/step", response_model=StepResponse)
async def run_step(request: StepRequest) -> StepResponse:
    history = sessions.get(request.conversation_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Unknown conversation_id")

    history.append({"sender": "user", "message": request.message})

    try:
        crew_result = await call_agent(
            CREW_AGENT_URL,
            request.conversation_id,
            sender="user",
            message=request.message,
            history=history,
        )
    except httpx.HTTPError as exc:  # pragma: no cover
        raise HTTPException(status_code=502, detail=f"Crew agent 호출 실패: {exc}") from exc

    crew_reply = crew_result.get("reply", "")
    history.append({"sender": "crew", "message": crew_reply})

    try:
        writer_result = await call_agent(
            LANGGRAPH_AGENT_URL,
            request.conversation_id,
            sender="crew",
            message=crew_reply,
            history=history,
        )
    except httpx.HTTPError as exc:  # pragma: no cover
        raise HTTPException(status_code=502, detail=f"LangGraph agent 호출 실패: {exc}") from exc

    writer_reply = writer_result.get("reply", "")
    history.append({"sender": "writer", "message": writer_reply})

    return StepResponse(conversation_id=request.conversation_id, history=history)


@app.get("/api/conversations/{conversation_id}")
async def get_history(conversation_id: str) -> JSONResponse:
    history = sessions.get(conversation_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Unknown conversation_id")
    return JSONResponse({"conversation_id": conversation_id, "history": history})


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
