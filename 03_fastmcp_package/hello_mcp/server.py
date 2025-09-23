"""Packaged FastMCP server that can be invoked via console script."""

from fastmcp import FastMCP

app = FastMCP(
    name="hello-mcp",
    instructions="Packaged FastMCP server for demonstration.",
)


@app.tool(description="Return a canned status update for onboarding demos.")
def marketing_update(product_name: str, audience: str = "팀") -> str:
    """Create a short status update template."""

    return (
        f"{audience} 여러분, {product_name} 런칭 준비 상황은 80% 완료되었습니다. "
        "이번 주에는 베타 피드백 정리와 최종 페이지 검수를 함께 진행해 주세요."
    )


@app.tool(description="Summarise highlights and risks from meeting notes.")
def summarize_meeting(notes: str) -> dict[str, list[str]]:
    """Split meeting notes into highlights and risks."""

    highlights: list[str] = []
    risks: list[str] = []
    for line in notes.splitlines():
        clean = line.strip().lstrip("-•* ")
        if not clean:
            continue
        if any(token in clean.lower() for token in ["risk", "block", "우려", "문제"]):
            risks.append(clean)
        else:
            highlights.append(clean)
    if not highlights:
        highlights.append("공유할 주요 성과가 발견되지 않았어요.")
    if not risks:
        risks.append("현재 위험 요소는 보이지 않아요.")
    return {"highlights": highlights, "risks": risks}


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
