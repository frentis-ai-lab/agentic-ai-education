"""Quick client smoke-test for the FastMCP server."""

import asyncio
from fastmcp import Client, FastMCP

from server import app


async def main() -> None:
    proxy_server = FastMCP.as_proxy(app)
    async with Client(proxy_server) as client:
        tools = await client.list_tools()
        print("등록된 툴:", [tool.name for tool in tools])

        greeting = await client.call_tool("greet", {"name": "수강생"})
        print("greet →", greeting.content[0].text)

        todos = await client.call_tool(
            "extract_todos",
            {
                "note": "이번 주 해야 할 것: 데이터 정리해야 하고, todo: FastMCP 실습 복습하기",
            },
        )
        print("extract_todos →", todos.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
