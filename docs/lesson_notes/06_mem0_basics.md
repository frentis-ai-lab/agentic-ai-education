# 06_mem0_basics – 학습 노트

## 학습 목표
- mem0 API를 사용해 사용자 메모리를 생성/검색/요약하는 순서를 익히기
- `user_id`를 기준으로 사용자별 장기 기억을 관리하는 패턴 이해
- 검색 질의(`search`)와 요약(`get_summary`) 결과를 비교 분석

## 아키텍처 개요
1. **환경 구성**
   - `MEM0_API_KEY` 설정 필수 (mem0 클라우드 계정)
   - `MemoryClient`로 API 호출 객체 생성
2. **저장 로직**
   - `client.add(messages=[...], user_id=USER_ID)`
   - `messages` 배열은 chat-like 포맷을 따라 role/content 형태로 구성
3. **검색 & 요약**
   - `client.search(query, user_id, top_k)` → 관련 메모리 목록
   - `client.get_summary(filters={"user_id": ...})` → mem0가 자체 요약 생성

## 실행 & 관찰 포인트
- `seed_facts` 내용을 바꾸며 검색 결과의 정확도를 확인
- 같은 `user_id`로 여러 번 실행하면 mem0가 어떻게 기존 메모리를 업데이트/병합하는지 체크
- 요약 결과에 포함되지 않는 요소가 있다면 어떤 사실이 중요하다고 판단했는지 토론

## 심화 질문
- mem0의 `metadata` 필드를 사용하면 어떤 추가 정보를 함께 저장할 수 있을까?
- 사내 데이터베이스와 mem0를 함께 사용할 때, 동기화 전략은 어떻게 설계할까?
- 개인정보/프라이버시 측면에서 어떤 고려가 필요한가?
