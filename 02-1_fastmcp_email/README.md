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

`mcp.json` 파일에 추가:
```json
{
  "mcpServers": {
    "email-tool": {
      "url": "http://localhost:8000/mcp/"
    }
  }
}
```

**주의**: Claude Desktop FREE 버전은 HTTP MCP 서버를 지원하지 않습니다. Cursor나 다른 MCP 클라이언트를 사용하세요.

## 문제 해결

- **Import 오류**: `uv sync --reinstall`
- **Gmail 오류**: 앱 비밀번호 재생성, 공백 제거 확인
- **연결 오류**: 서버 실행 상태 확인