# 01_fastmcp_tool

FastMCP로 MCP 서버(툴)를 간단히 만들어 보고, 로컬 클라이언트로 호출하는 최소 예제입니다.

## 1. 환경 준비
```bash
uv sync
```

## 2. 서버 실행
기본적으로 `stdio` 전송 방식을 사용하므로, 별도 인자를 주지 않아도 됩니다.
```bash
uv run python server.py
```
다른 터미널에서 클라이언트를 실행하거나, 아래와 같이 in-process 테스트 코드로 도구 호출을 확인할 수 있습니다.

## 3. 클라이언트 테스트
```bash
uv run python client.py
```
출력 예시
```
등록된 툴: ['greet', 'extract_todos']
greet → 안녕하세요, 수강생! FastMCP에 오신 것을 환영해요.
extract_todos → {'result': ['데이터 정리해야 하고, todo: FastMCP 실습 복습하기']}
```

> 실제 MCP 호환 클라이언트(예: Claude Desktop)의 `fastmcp.json` 설정에 `01_fastmcp_tool/server.py`를 등록하면 동일한 도구를 사용할 수 있습니다.
