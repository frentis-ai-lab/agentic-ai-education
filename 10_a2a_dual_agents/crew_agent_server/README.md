# Crew Agent Server

CrewAI 기반 A2A 대응 에이전트 서버입니다. `POST /a2a/message` 엔드포인트를 통해 메시지를 전달하면, 마케팅 전략 초안을 작성해 반환합니다.

## 실행 방법
```bash
uv sync
uv run uvicorn server:app --reload --port 8001
```

## API 요약
- `GET /health` — 상태 확인
- `GET /metadata` — 에이전트 설명/핵심 태그 제공
- `POST /a2a/message` — 메시지를 입력하면 CrewAI 크루가 응답을 생성

요청 형식 예시:
```json
{
  "conversation_id": "demo-session",
  "sender": "user",
  "message": "Agentic 교육 과정 론칭 계획을 도와줘",
  "history": [
    {"sender": "user", "message": "..."}
  ]
}
```

응답 형식:
```json
{
  "reply": "...",
  "agent": "crew-marketer",
  "meta": {"tokens_used": 123}
}
```

이 서버는 후속 단계에서 오케스트레이션 UI가 호출하는 첫 번째 Agent 역할을 수행합니다.
