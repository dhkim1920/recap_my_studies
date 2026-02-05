# AI 기술 적용 및 활용

## Gen AI (Generative AI)

- 텍스트, 이미지, 오디오, 코드 등을 생성하는 AI  
- 대표 사례: ChatGPT, DALL·E, GitHub Copilot  
- 기반 기술: GPT, Diffusion, GAN 등  
- 활용: 문서 요약, 대화, 이미지 생성, 코드 자동 작성 등

## Agentic AI

- 단순 생성이 아니라 **목표 달성형 AI**  
- 기능: 도구 연동, 자동 실행, 외부 시스템 통합  
- 예시: AutoGPT, Devin, OpenAgents  
- 기술 구성: Gen AI + Planning + Tool 사용 + Memory

### Gen AI vs Agentic AI

| 항목       | Gen AI                     | Agentic AI                                  |
|------------|----------------------------|---------------------------------------------|
| 목적       | 콘텐츠 생성                | 자율적 목표 수행, 작업 실행                 |
| 기술       | GPT 등 생성 모델 기반       | 생성 + 계획 + 실행 + 도구 사용             |
| 활용       | 대화 응답, 콘텐츠 제작     | 시스템 통합, 자동화 에이전트 역할 수행     |
| 예시       | ChatGPT, DALL·E            | AutoGPT, Devin                              |

## Generative BI

- Gen AI를 이용해 자연어로 질의 시 BI 리포트를 자동 생성  
- 기능: Text2SQL → 차트 자동 생성  
- 예시: "지난달 매출 추이 보여줘" → SQL 생성 → 시각화 자동 생성

## RAG (Retrieval-Augmented Generation)

- LLM이 답변을 생성하기 전, 관련 외부 데이터를 검색하여 응답 품질 향상  
- 구성:
  - Retrieval: DB 스키마, 문서 등 검색  
  - Generation: 검색 결과 기반 응답 생성  
- 활용: Text2SQL에서 정확한 테이블 정보 반영 등

## Prompting

- LLM에게 주는 명령문(프롬프트)을 설계하는 기법  
- 역할: 원하는 형식의 정확한 응답 유도  
- 예시:  
  "You are a SQL expert. Given a question and table schema, write a valid SQL query."
