# 07_mem0_cli_chat – 학습 노트

## 학습 목표
- Streamlit 없이 터미널 환경에서 mem0 장기 기억 흐름을 체험
- 사용자 발화 → mem0 저장 → 관련 기억 검색 → LLM 응답 재생산 과정 익히기
- 기억 리스트를 사람이 읽을 수 있는 형태로 출력해 디버깅 및 교육 자료로 활용

## 아키텍처 개요
1. **mem0 클라이언트**
   - `mem0.MemoryClient` + 고정 user_id(`cli-demo-user`)
   - `memory_utils.py`를 통해 add/search 래핑
2. **LangChain LLM**
   - `ChatOpenAI` 사용, 프롬프트에 memories 텍스트/JSON 동시 제공
   - 기억이 없을 때는 정중히 모른다고 답하도록 시스템 지시명령 포함
3. **CLI 루프 (`chat_cli.py`)**
   - 입력 → mem0 저장 → 검색 결과 콘솔 출력 → LLM 응답 출력 → 반복
   - `exit`, `quit`, `q` 입력 시 종료

## 실행 & 관찰 포인트
- 검색된 기억이 어떤 순서로 출력되는지 확인하고, 응답에 해당 문구가 포함되는지 비교
- 같은 user_id를 유지하면 이전 입력이 다시 활용되는 것을 확인
- 필요 시 `.env`에서 `MEM0_CLI_USER_ID`를 바꿔 다른 사용자의 기억을 테스트

## 심화 질문
- 사용자별 user_id를 CLI 인자나 옵션으로 받아 실서비스에 맞추려면?
- 정기적으로 `get_summary`를 호출하여 누적 정보를 정리하거나 노이즈를 제거하려면?
- CLI가 아닌 REST/Slack 봇 등 다른 채널과 연동하려면 어떤 구조가 필요할까?
