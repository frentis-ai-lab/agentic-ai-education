# 04_crewai_team

CrewAI로 마케터 → 영업(휴먼) → 메일러 구조의 협업 플로우를 구성합니다.

## 1. 준비
```bash
export OPENAI_API_KEY=sk-...
uv sync
```
> 모델은 기본적으로 `gpt-4o-mini`를 사용하며, `--model` 옵션으로 다른 OpenAI 호환 모델을 지정할 수 있습니다.

## 2. 실행
```bash
uv run python crew_run.py "Agentic AI 교육" "SaaS 파트너 마케터"
```
실행 흐름
1. 마케터(agent)가 시장 요약과 실행안을 작성
2. 영업 담당자(task, `human_input=True`)가 콘솔에서 피드백을 입력
3. 메일러(agent)가 최종 이메일 초안을 작성

## 3. 강의 포인트
- CrewAI는 `Agent`와 `Task`, `Crew` 3요소만 이해하면 쉽게 시나리오를 확장할 수 있습니다.
- `human_input=True`를 통해 실제 담당자가 개입하는 하이브리드 워크플로우를 구현할 수 있습니다.
- 이후 단계에서 MCP 도구나 벡터 검색 등을 `tools`로 주입해 복잡도를 높일 수 있습니다.
