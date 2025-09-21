# 02_fastmcp_package

FastMCP 서버를 패키징하고 `fastmcp.json`에 등록하는 전체 흐름을 담은 예제입니다.

## 1. 로컬 개발 환경
```bash
uv sync

# 개발 중에는 editable 설치로 빠르게 테스트할 수 있습니다.
uv pip install --editable .
uv run hello-mcp-server
```

## 2. PyPI(TestPyPI) 업로드 플로우
실제 배포는 PyPI 또는 TestPyPI에 wheel을 업로드한 뒤, 클라이언트 환경에서 `pip install agentic-hello-mcp` 형태로 설치하는 것을 권장합니다.

1. **배포용 빌드**
   ```bash
   uv build
   ```
2. **TestPyPI 업로드 예시**
   ```bash
   uvx twine upload --repository testpypi dist/*
   # 실제 PyPI에 배포할 때는 --repository pypi 사용
   ```
   > 최초 업로드 전에는 `~/.pypirc` 등 인증 정보가 필요합니다. TestPyPI는 `https://test.pypi.org/account/register/`에서 계정을 만들 수 있습니다. API 토큰은 보통 `~/.pypirc`에 `username=__token__`, `password=pypi-...` 형태로 보관하거나, 업로드 직전에 `TWINE_USERNAME=__token__`, `TWINE_PASSWORD=pypi-...`를 일시적으로 export하는 방식을 권장합니다 (민감 정보는 `.env`에 저장하지 마세요).
3. **클라이언트 설치**
   ```bash
   # TestPyPI에 배포했다면 extra-index-url을 사용해 설치
   pip install --extra-index-url https://test.pypi.org/simple agentic-hello-mcp
   ```
   설치가 완료되면 `hello-mcp-server` 콘솔 스크립트가 PATH에 등록되어 MCP 클라이언트가 바로 실행할 수 있습니다.

## 3. 설치 없이 바로 실행하기 (빠른 검증)
패키지를 시스템에 남기지 않고 바로 실행하려면 `pipx run` 또는 `uv tool run`을 사용할 수 있습니다.

```bash
# pipx 이용 (사전 설치 필요)
pipx run --spec agentic-hello-mcp hello-mcp-server

# uv 이용
uv tool run --from agentic-hello-mcp hello-mcp-server

# TestPyPI에서 가져와야 한다면 index URL 지정
uv tool run --index-url https://test.pypi.org/simple \
    --from agentic-hello-mcp hello-mcp-server
```

Claude Desktop의 `fastmcp.json`에서 `command`를 위 명령어로 설정하면 별도 설치 없이도 MCP 서버를 띄울 수 있습니다. 다만 매 실행마다 패키지를 내려받으므로, 지속 사용 시에는 `pipx install` 또는 `uv tool install`로 PATH에 등록하는 방식을 권장합니다.

## 4. MCP 설정 파일 적용 예시
`fastmcp.json`을 Claude Desktop 등 MCP 호환 클라이언트 설정에 추가하면 설치된 `hello-mcp-server`를 그대로 사용할 수 있습니다.
```json
{
  "mcpServers": {
    "hello-mcp": {
      "type": "stdio",
      "command": "hello-mcp-server",
      "description": "Packaged FastMCP demo server"
    }
  }
}
```

## 5. 로컬 클라이언트 스모크 테스트
패키지 설치와 무관하게, 동일 프로세스에서 툴 동작을 빠르게 확인하려면 다음을 실행하세요.
```bash
uv run python demo_client.py
```
출력 예시
```
툴 목록: ['marketing_update', 'summarize_meeting']
marketing_update → 운영팀 여러분, 에이전틱 교육 과정 런칭 준비 상황은 80% 완료되었습니다.
...
```

> PyPI에 배포하면 팀원들이 `pip install agentic-hello-mcp` 또는 `pipx run --spec agentic-hello-mcp hello-mcp-server`와 같은 명령으로 동일한 MCP 툴을 바로 사용할 수 있습니다.
