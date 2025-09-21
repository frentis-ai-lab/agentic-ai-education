"""LangChain agent that mixes local tools with FastMCP tools."""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from dotenv import load_dotenv
from fastmcp import Client, FastMCP
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from mcp_server import app as mcp_app

load_dotenv()

PROXY_SERVER = FastMCP.as_proxy(mcp_app)


def _call_mcp(tool_name: str, **arguments: Any) -> str:
    async def _invoke() -> str:
        async with Client(PROXY_SERVER) as client:
            result = await client.call_tool(tool_name, arguments)
            if result.structured_content:
                return json.dumps(result.structured_content, ensure_ascii=False, indent=2)
            if result.content:
                texts = []
                for block in result.content:
                    text = getattr(block, "text", None)
                    if text:
                        texts.append(text)
                if texts:
                    return "\n".join(texts)
            return "(no content returned)"

    return asyncio.run(_invoke())


def get_product_snapshot(product: str) -> str:
    catalog = {
        "Agentic AI 교육": "LLM 기반 워크플로우와 MCP 실습을 포함한 4주 과정",
        "FastLaunch 패키지": "3주 안에 PoC를 만들기 위한 페어 코칭 프로그램",
    }
    return catalog.get(product, "등록된 제품을 찾을 수 없습니다.")


def internal_kpi(last_ctr: float, goal_ctr: float) -> str:
    lift = goal_ctr - last_ctr
    return f"지난 CTR {last_ctr:.1f}% → 목표 {goal_ctr:.1f}%. 추가로 {lift:.1f}% 포인트 상승이 필요합니다."


def internal_kpi_tool(text: str) -> str:
    try:
        last_str, goal_str = [part.strip() for part in text.split(",", 1)]
        return internal_kpi(float(last_str), float(goal_str))
    except Exception as exc:  # pragma: no cover - defensive
        return f"입력 형식은 '18.0,23.0'과 같이 쉼표로 구분된 수치여야 합니다. ({exc})"


def campaign_compass_tool(task: str) -> str:
    return _call_mcp("campaign_compass", product=task)


def audience_scanner_tool(segment: str) -> str:
    return _call_mcp("audience_scanner", segment=segment)


def email_blueprint_tool(query: str) -> str:
    payload = {
        "product": os.getenv("DEFAULT_PRODUCT", "Agentic AI 교육"),
        "segment": query,
        "ask": "다음 주에 20분 상담 미팅 제안",
    }
    return _call_mcp("email_blueprint", **payload)


def build_agent() -> ChatOpenAI:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model_name, temperature=0.2)


def main() -> None:
    llm = build_agent()
    tools = [
        Tool(
            name="ProductSnapshot",
            description="제품명을 입력하면 요약을 반환합니다.",
            func=get_product_snapshot,
        ),
        Tool(
            name="InternalKPI",
            description="마지막 CTR과 목표 CTR을 'last,goal' 형태로 입력하면 차이를 알려줍니다.",
            func=internal_kpi_tool,
        ),
        Tool(
            name="MCP_CampaignCompass",
            description="제품명을 넣으면 MCP 서버에서 런칭 계획과 메시지 각도를 받아옵니다.",
            func=campaign_compass_tool,
        ),
        Tool(
            name="MCP_AudienceScanner",
            description="세그먼트명을 전달하면 MCP 서버가 최신 트렌드와 우려사항을 반환합니다.",
            func=audience_scanner_tool,
        ),
        Tool(
            name="MCP_EmailBlueprint",
            description="세그먼트명을 입력하면 MCP 서버가 이메일 제목과 본문 개요를 생성합니다.",
            func=email_blueprint_tool,
        ),
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    prompt = (
        "Agentic AI 교육을 SaaS 파트너 마케터에게 소개하는 이메일 초안과 핵심 포인트를 정리해 주세요. "
        "필요하다면 내부 지표(지난 CTR 18%, 목표 23%)와 MCP 툴을 활용해 경쟁사 동향과 이메일 구조를 확인하세요."
    )
    response = agent.run(prompt)
    print("\n최종 답변:\n", response)


if __name__ == "__main__":
    main()
