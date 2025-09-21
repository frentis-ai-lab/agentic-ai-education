# 03_langchain_react

LangChain의 ReAct 에이전트 패턴으로 간단한 마케팅 씬을 시뮬레이션합니다.

## 1. 환경 준비
```bash
export OPENAI_API_KEY=sk-...
uv sync
```
> 기본 모델은 `gpt-4o-mini`로 설정했습니다. 다른 모델을 쓰려면 `OPENAI_MODEL` 환경 변수를 지정하세요.

## 2. 실행
```bash
uv run python react_agent.py
```
실행하면 ReAct 에이전트가 주어진 툴(ProductSnapshot, SegmentTip, CampaignHistory)을 순차적으로 호출하며 답변을 구성하는 로그가 출력됩니다.

## 3. 강의 포인트
- ReAct는 `생각(Thought) → 행동(Action) → 관찰(Observation)` 루프를 명확하게 확인할 수 있어 학습용으로 적합합니다.
- 툴은 단순 Python 함수로 정의하되, 자연어 설명(description)을 충분히 달아주면 모델이 선택에 도움을 받습니다.
- 실제 서비스에서는 벡터검색, CRM API 호출 등의 복잡한 툴로 대체할 수 있습니다.
