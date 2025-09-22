# 08_a2a_basics

AutoGen(`pyautogen`)으로 에이전트-투-에이전트(a2a) 대화를 구성하는 기본 예제입니다.

## 1. 준비
1. 루트 `.env`에서 OPENAI_API_KEY를 설정하고 `source .env` (권장)
2. 이 디렉터리에서 의존성을 설치합니다.

```bash
# .env를 사용하지 않는 경우 직접 설정
export OPENAI_API_KEY=sk-...
uv sync
```

## 2. 실행
```bash
uv run python basic_chat.py
```
- `planner` : 구조를 잡는 전략가
- `writer` : 이메일 본문을 작성하는 카피라이터
- `reviewer` : 대화를 관리하는 UserProxyAgent (자동 응답)

> 참고: 코드 실행에 Docker가 필요하지 않도록 스크립트에서 `use_docker=False`를 설정했습니다.

GroupChatManager를 통해 다중 에이전트가 순환하며 메시지를 주고받고, `max_round` 내에 결과를 도출합니다.

## 3. 강의 포인트
- AutoGen은 대화형 협업에 특화되어 있어, 다양한 롤을 가진 에이전트를 쉽게 붙일 수 있습니다.
- `UserProxyAgent`에 `human_input_mode="NEVER"`를 주면 완전 자동화, `ALWAYS`로 주면 중간에 직접 개입할 수 있습니다.
