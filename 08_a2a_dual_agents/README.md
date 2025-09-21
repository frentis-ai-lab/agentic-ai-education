# 08_a2a_dual_agents

두 개의 독립 에이전트 서버(CrewAI, LangGraph)와 이를 조율하는 오케스트레이션 UI 서버를 통해 A2A(Agent-to-Agent) 패턴을 실습합니다. 구조는 [A2A 프로젝트](https://github.com/a2aproject/A2A)에서 소개하는 프로토콜을 간소화해 학습용으로 구성했습니다.

## 구성
| 폴더 | 설명 | 기본 포트 |
| --- | --- | --- |
| `crew_agent_server` | CrewAI 기반 전략가 에이전트 (`POST /a2a/message`) | 8001 |
| `langgraph_agent_server` | LangGraph 기반 카피라이터 에이전트 | 8002 |
| `orchestrator_ui` | FastAPI + Jinja UI, 두 에이전트를 순차 호출 | 8000 |

각 폴더는 독립적인 `pyproject.toml`과 `uv` 환경을 사용합니다.

## 전체 실행 순서
1. **Crew 에이전트 서버 실행**
   ```bash
   cd crew_agent_server
   uv sync
   uv run uvicorn server:app --port 8001 --reload
   ```

2. **LangGraph 에이전트 서버 실행**
   ```bash
   cd ../langgraph_agent_server
   uv sync
   uv run uvicorn server:app --port 8002 --reload
   ```

3. **오케스트레이터 UI 실행**
   ```bash
   cd ../orchestrator_ui
   uv sync
   uv run uvicorn server:app --port 8000 --reload
   ```

4. 브라우저에서 `http://localhost:8000` 접속 후 메시지를 입력하면 다음 흐름이 수행됩니다.
   1. 사용자의 입력 → Crew 에이전트로 전송 → 전략 개요 응답
   2. Crew 응답 → LangGraph 에이전트로 전달 → 맞춤 이메일 작성
   3. UI에 두 응답이 순차적으로 표시

## 프로토콜 요약
세 서버는 A2A 프로젝트의 기본 아이디어를 따라 `POST /a2a/message` 형식으로 통신합니다.
```json
{
  "conversation_id": "string",
  "sender": "user | crew | writer",
  "message": "...",
  "history": [
    {"sender": "user", "message": "..."},
    {"sender": "crew", "message": "..."}
  ]
}
```

응답은 다음과 같이 `reply` 필드를 포함합니다.
```json
{
  "reply": "...",
  "agent": "crew-marketer",
  "meta": {"history_items": 2}
}
```

UI 서버는 세션별로 대화 히스토리를 메모리에 보관하며, 필요에 따라 Redis 등 외부 저장소로 대체할 수 있습니다.

## 확장 아이디어
- Crew/LangGraph 에이전트에 MCP 툴을 연결해 실제 데이터를 활용
- UI에서 에이전트 선택, 병렬 호출 등 추가 Orchestration 패턴 실험
- A2A 프로젝트의 `a2a-sdk`를 도입해 표준 프로토콜을 그대로 구현
