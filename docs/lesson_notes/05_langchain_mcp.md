# 05. LangChain + MCP 통합

## 목표
LangChain ReAct 에이전트에서 MCP(Model Context Protocol) 도구를 사용합니다.

## 핵심 개념
- **MCP 클라이언트**: `mcp` 패키지를 사용한 도구 연결
- **도구 변환**: MCP 도구를 LangChain Tool로 변환
- **하이브리드 에이전트**: 로컬 도구 + MCP 도구 조합

## 실습 단계
1. MCP 서버 실행 (별도 터미널)
2. MCP 클라이언트로 도구 연결
3. LangChain Tool 래퍼 구현
4. ReAct 에이전트에 도구 추가
5. 통합 테스트 실행

## 주요 학습 포인트
- MCP 프로토콜을 통한 도구 재사용
- 서로 다른 프레임워크 간 도구 공유
- 에이전트 아키텍처의 모듈화

## 다음 단계
mem0를 사용한 메모리 관리 기초를 학습합니다.