"""Call the packaged FastMCP server without spawning a subprocess."""

import asyncio
from fastmcp import Client, FastMCP

from hello_mcp import app


async def main() -> None:
    proxy = FastMCP.as_proxy(app)
    async with Client(proxy) as client:
        tools = await client.list_tools()
        print("툴 목록:", [tool.name for tool in tools])
        status = await client.call_tool(
            "marketing_update",
            {"product_name": "에이전틱 교육 과정", "audience": "운영팀"},
        )
        print("marketing_update →", status.content[0].text)

        meeting = await client.call_tool(
            "summarize_meeting",
            {
                "notes": (
                    "- 런칭 일정은 다음 주로 확정\n"
                    "- Risk: 콘텐츠 검수 일정이 겹쳐 있음\n"
                    "- 온보딩 가이드 작성 중"
                )
            },
        )
        print("summarize_meeting →", meeting.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
