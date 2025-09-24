# 09. CrewAI + MCP 뉴스레터 시스템

## 목표
CrewAI 멀티 에이전트와 MCP 도구를 결합한 AI 뉴스레터 자동 제작/발송 시스템을 구현합니다.

## 핵심 개념
- **MCP 도구 통합**: FastMCP 서버를 CrewAI 에이전트에 연결
- **멀티 에이전트 협업**: 뉴스 수집 → 큐레이션 → 디자인 → 발송
- **실용적 자동화**: RSS 피드부터 실제 이메일 발송까지

## 실습 단계
1. MCP 뉴스레터 서버 구현 (RSS, 이메일 도구)
2. CrewAI 에이전트 4개 정의
   - News Researcher (뉴스 수집)
   - Content Editor (큐레이션)
   - Newsletter Designer (HTML 생성)
   - Email Campaign Manager (발송)
3. MCP 클라이언트를 CrewAI 도구로 통합
4. 완전 자동화 워크플로우 테스트

## 주요 학습 포인트
- 프레임워크 간 도구 재사용 (MCP 표준화)
- 복잡한 멀티 스텝 자동화 구현
- 실제 비즈니스 워크플로우 모델링

## 다음 단계
Google A2A SDK를 사용한 고급 멀티 에이전트 시스템을 학습합니다.