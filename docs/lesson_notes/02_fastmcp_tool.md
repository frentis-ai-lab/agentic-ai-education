# 02_fastmcp_tool – 학습 노트

## 학습 목표
- FastMCP 서버의 기본 구조와 `@app.tool` 데코레이터 사용법 이해
- MCP 클라이언트가 툴 목록을 조회하고 호출하는 end-to-end 흐름 체험
- 구조화 응답(`structuredContent`)이 언제/어떻게 생성되는지 확인

## 아키텍처 개요
1. **Server (`server.py`)**
   - `FastMCP` 인스턴스를 생성하고 메타데이터(이름, instructions)를 정의
   - `greet`, `extract_todos` 두 툴을 등록 → 단일 프로세스에서 MCP 서버 구동 (`app.run()`)
2. **Client (`client.py`)**
   - `FastMCP.as_proxy(app)`로 같은 프로세스 내에서 MCP 통신을 시뮬레이션
   - `Client.list_tools()` → MCP의 `tools/list`
   - `Client.call_tool()` → MCP의 `tools/call` (구조화 응답 파싱 포함)

## 실행 & 관찰 포인트
- `uv run python server.py` 로 서버를 띄운 뒤 CLI/README에 적힌 대로 클라이언트 호출
- 출력에서 `structured_content` 키가 나타나는지 확인 → `extract_todos` 반환값이 리스트일 때 자동 스키마 생성됨
- MCP 호환 클라이언트(예: Claude Desktop)에 `server.py`를 등록해 동일 툴을 실제 UI에서 호출해보면 추가 경험 가능

## 심화 질문
- FastMCP 툴에 매개변수 타입 힌트를 바꿔보면 JSON 스키마는 어떻게 변할까?
- `app.tool`에 `description`, `tags`를 추가하면 MCP 클라이언트에는 어떤 식으로 노출될까?
- 실서비스에서는 `app.run_stdio()` 외 다른 트랜스포트(HTTP, SSE)를 언제 고려해야 할까?
