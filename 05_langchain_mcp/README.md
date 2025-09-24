# 04_langchain_mcp

여기서는 LangChain ReAct 에이전트가 **로컬 함수형 툴 + FastMCP 서버 툴**을 동시에 활용하는 예제를 다룹니다. 기존 03단계보다 다양한 도구 선택과 외부(MCP) 호출 흐름을 살펴볼 수 있습니다.

## 1. 환경 준비
1. 루트에서 `.env` 파일을 설정하고 `source .env` (권장)
2. 이 디렉터리에서 의존성 설치

```bash
uv sync
```

## 2. MCP 서버 실행 (선택)
LangChain 스크립트가 `mcp_server.py`를 임베드해 실행하므로 별도로 띄울 필요는 없습니다. 다만 MCP 프로토콜을 직접 관찰하고 싶다면 다른 터미널에서 서버를 실행해 둘 수 있습니다.
```bash
uv run python mcp_server.py
```
서버는 `campaign_compass`, `audience_scanner`, `email_blueprint` 세 가지 MCP 툴을 제공합니다.

## 3. LangChain 에이전트 실행
```bash
uv run python react_with_mcp.py
```
에이전트는 다음과 같이 동작합니다.
- 로컬 함수형 툴: 제품 스냅샷, 내부 지표 계산 등
- MCP 브리징 툴: 실행 중인 FastMCP 서버의 툴을 호출 (competitor/audience 분석, 이메일 개요)

로그에서 MCP 툴 호출이 어떻게 이루어지는지 확인하세요. 응답에는 MCP가 반환한 structured content가 포함됩니다.

## 4. 실습 포인트
- LangChain의 `Tool` 인터페이스로 MCP 호출을 감싸는 방법
- MCP 서버가 반환하는 구조화 데이터를 LangChain 에이전트가 어떻게 활용하는지
- MCP 툴 호출 실패 시 재시도나 예외 처리 전략은 어떻게 설계할지 토론해 보기

## 5. 마무리
서버를 종료할 때는 MCP 터미널에서 `Ctrl+C`를 입력하세요. 에이전트 측은 MCP 서버가 종료되면 자동으로 오류를 보고합니다.
