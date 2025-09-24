# 03. FastMCP Email 도구

## 목표
OpenAI + Gmail SMTP를 사용한 이메일 작성 및 발송 MCP 서버를 구현합니다.

## 핵심 개념
- **이메일 작성**: OpenAI API를 사용한 자동 이메일 생성
- **Gmail SMTP**: Google 앱 비밀번호를 통한 이메일 발송
- **HTTP 전송**: FastMCP의 HTTP 서버 모드

## 실습 단계
1. Gmail 앱 비밀번호 설정 (2단계 인증 필수)
2. OpenAI API 키 및 Gmail 설정
3. 이메일 작성 도구 (`compose_email`) 구현
4. 이메일 발송 도구 (`send_email`) 구현
5. HTTP 서버로 MCP 도구 제공
6. Claude Desktop 연결 테스트

## 주요 학습 포인트
- 외부 API 통합 (OpenAI, Gmail)
- 환경변수를 통한 인증 정보 관리
- HTTP 전송 모드와 프록시 사용법

## 다음 단계
FastMCP 도구를 Python 패키지로 배포하는 방법을 학습합니다.