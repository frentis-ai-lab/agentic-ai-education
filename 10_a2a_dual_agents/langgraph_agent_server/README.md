# LangGraph Agent Server

LangGraph로 구현된 A2A 호환 에이전트 서버입니다. Crew 에이전트가 준 결과를 기반으로 이메일 초안을 작성하는 역할을 담당합니다.

## 실행 방법
```bash
uv sync
uv run uvicorn server:app --reload --port 8002
```

## API 요약
- `GET /health`
- `GET /metadata`
- `POST /a2a/message`

`POST /a2a/message` 요청은 LangGraph 파이프라인으로 전달되어, 이전 히스토리와 입력 메시지를 바탕으로 최종 이메일 초안을 생성합니다.
