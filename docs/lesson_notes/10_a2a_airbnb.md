# 10. Google A2A SDK 멀티 에이전트 시스템

## 목표
Google Agent Development Kit (ADK)와 A2A SDK를 사용한 멀티 에이전트 협업 시스템을 구현합니다.

## 핵심 개념
- **Agent2Agent (A2A)**: Google의 에이전트 간 통신 프로토콜
- **Host Agent**: 사용자 요청을 분석하고 적절한 에이전트에게 작업 위임
- **Remote Agents**: 특화된 기능을 제공하는 독립적인 에이전트들
- **MCP 통합**: 각 에이전트가 MCP 서버와 연동하여 외부 도구 활용

## 시스템 구조
1. **Host Agent**: 사용자 요청 분석 및 작업 라우팅
2. **Airbnb Agent**: 숙박 검색 및 예약 관련 작업
3. **Weather Agent**: 날씨 정보 조회 및 분석
4. **MCP Servers**: 각 에이전트가 사용하는 외부 도구들

## 실습 단계
1. Python 3.13 환경 구성 (A2A SDK 요구사항)
2. Google API 키 및 Vertex AI 설정
3. 각 에이전트 서버 구현 (Airbnb, Weather)
4. Host Agent의 요청 라우팅 로직 구현
5. 멀티 에이전트 협업 시나리오 테스트

## 주요 학습 포인트
- 대규모 멀티 에이전트 아키텍처 설계
- 에이전트 간 안전한 통신 및 데이터 검증
- 실제 상용 서비스 수준의 에이전트 시스템 구조

## 다음 단계
차세대 AI 에이전트 기술 동향과 미래 발전 방향을 탐구합니다.