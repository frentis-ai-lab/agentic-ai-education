# 08_a2a_mem0_profile

mem0에 저장된 개인정보를 활용하는 AutoGen a2a 에이전트 예제입니다.

## 1. 환경 변수 설정
1. 루트 `.env`에 `OPENAI_API_KEY`, `MEM0_API_KEY`를 지정하고 `source .env` (권장)
2. 이 디렉터리에서 의존성을 설치합니다.

```bash
# .env를 사용하지 않는 경우 직접 설정
export OPENAI_API_KEY=sk-...
export MEM0_API_KEY=mem0_xxx
uv sync
```

## 2. 실행
```bash
uv run python personal_agents.py
```
실행하면 다음 흐름을 확인할 수 있습니다.
1. `ensure_memories`가 mem0에 기본 프로필 사실을 저장
2. `profile` 에이전트가 `search_profile` 툴을 호출해 사용자 기억을 조회
3. `campaign` 에이전트가 해당 정보를 받아 맞춤형 이메일 개요를 작성

## 3. 강의 포인트
- AutoGen의 `register_for_llm` + `register_for_execution` 패턴으로 외부 API(mem0)를 도구로 연결
- 사용자별 `user_id`를 유지하면 장기 기억을 갖는 개인 비서 에이전트를 구성할 수 있습니다.
- 이후 단계에서는 동일한 패턴으로 MCP 기반 도구를 추가해 복합 A2A 에이전트를 만들 수 있습니다.
