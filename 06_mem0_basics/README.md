# 06_mem0_basics

mem0 클라우드 API를 이용해 개인화된 정보를 저장하고 검색하는 기초 예제입니다.

## 1. 환경 변수 설정
1. 루트에서 `.env` 파일에 `MEM0_API_KEY`를 지정하고 `source .env` (권장)
2. 이 디렉터리에서 의존성을 설치합니다.

```bash
# .env를 사용하지 않는 경우 직접 설정
export MEM0_API_KEY=mem0_xxx
uv sync
```
> API 키는 [Mem0 문서](https://docs.mem0.ai)에서 발급 받을 수 있습니다.

## 2. 실행
```bash
uv run python memory_demo.py
```
- `client.add(...)` : 사용자(`user_id`)별 사실을 저장
- `client.search(...)` : 자연어 쿼리로 관련 메모리 검색
- `client.get_summary(...)` : 저장된 정보의 요약을 자동 생성

## 3. 강의 포인트
- mem0는 LLM과 별개로 장기 기억 스토리지를 제공하므로, 사용자 맥락을 지속적으로 반영할 수 있습니다.
- 이후 단계에서 `user_id`를 에이전트 ID와 매핑하면 개인 비서 스타일의 에이전트를 쉽게 만들 수 있습니다.
