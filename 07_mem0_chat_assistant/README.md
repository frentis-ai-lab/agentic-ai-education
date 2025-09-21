# 07_mem0_chat_assistant

Streamlit 기반 대화형 챗봇으로 mem0의 장기 기억을 체험합니다. 이전 단계(06)에서 다룬 mem0 API를 LangChain/Streamlit과 결합하여, 사용자가 입력한 정보가 이후 대화에 반영되는 모습을 확인할 수 있습니다.

## 1. 준비
1. 루트 `.env`에 다음 값을 설정하고 `source .env` (권장)
   - `OPENAI_API_KEY`
   - `MEM0_API_KEY`
2. 의존성 설치
   ```bash
   uv sync
   ```

## 2. 실행
```bash
uv run streamlit run app.py
```

## 3. 주요 기능
- **세션별 user_id 자동 생성**: Streamlit 세션 상태를 통해 user_id를 유지하고, 동일 브라우저에서 대화를 이어갈 때 mem0에 저장된 기억을 재활용합니다.
- **user_id 편집**: 사이드바에서 user_id를 직접 수정하거나 새로 발급하여, 새 세션이나 특정 사용자의 기억을 손쉽게 전환합니다.
- **기억 저장/검색**: 사용자의 메시지를 mem0에 저장하고, LangChain LLM 호출 전에 관련 기억을 검색하여 함께 전달합니다.
- **최근 기억 표시**: 요약과 검색 결과를 카드 형태로 보여주어, JSON을 읽지 않아도 어떤 기억이 활용되었는지 바로 파악할 수 있습니다.

## 4. 파일 구성
- `app.py` : Streamlit 앱 엔트리포인트
- `memory_utils.py` : mem0 저장/검색/요약을 담당하는 간단한 유틸리티 래퍼

## 5. 확장 아이디어
- 멀티 유저 지원 (로그인/별도 user_id 입력)
- 일정 횟수마다 `MemoryClient.get_summary`로 요약을 자동 표시
- 대화 종료 후 mem0에서 기억 삭제/정리 기능 추가
