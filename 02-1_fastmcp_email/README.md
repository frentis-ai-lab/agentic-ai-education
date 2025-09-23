# 02-1 FastMCP Email Tool

OpenAI + Gmail SMTP를 사용한 이메일 작성 및 발송 MCP 서버

## 기능

- **compose_email**: OpenAI 이메일 작성
- **send_email**: Gmail SMTP 발송
- **improve_email**: 이메일 개선

## 설치

```bash
cd 02-1_fastmcp_email
uv sync
cp .env.example .env
# .env 파일에서 API 키 설정
```

### 환경변수 설정 (.env)
```env
OPENAI_API_KEY=sk-your-key
GMAIL_USER=your@gmail.com
GMAIL_APP_PASSWORD=16자리앱비밀번호
```

### Gmail 앱 비밀번호
1. Google 계정 > 보안 > 2단계 인증 활성화
2. 앱 비밀번호 생성 (16자리)
3. 공백 없이 `.env`에 입력

## 사용법

### 1. 서버 실행
```bash
uv run python server.py
# http://localhost:8000/mcp/ 에서 실행
```

### 2. 테스트
```bash
uv run python client.py
```

### 3. Claude Desktop에서 사용

HTTP 서버 연결을 위해 `mcp-remote` 프록시 사용:

```json
{
  "mcpServers": {
    "email-tool": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:8000/mcp/"],
      "env": {
        "MCP_TRANSPORT_STRATEGY": "http-only"
      }
    }
  }
}
```

**주의**:
- Claude Desktop은 HTTP 서버에 직접 연결 불가 (프록시 필요)
- FREE 버전은 HTTP MCP 지원 제한
- `npx mcp-remote` 패키지가 필요할 수 있음

## 문제 해결

- **Import 오류**: `uv sync --reinstall`
- **Gmail 오류**: 앱 비밀번호 재생성, 공백 제거 확인
- **연결 오류**: 서버 실행 상태 확인