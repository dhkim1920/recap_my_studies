# Airflow 3.0.x에서 AIP-72 Task Execution Interface가 실제로 어떻게 동작할까?

Airflow 3.x 아키텍처에서는 태스크와 워커가 메타데이터 DB에 직접 접근하지 않는다. 런타임 상호작용은 API 서버를 통해 수행하며, 이 상호작용은 Task Execution API가 담당한다. 원격 실행을 위한 경량 런타임으로 Task SDK를 제공한다.

## Airflow 2.x와 3.x의 차이
### Airflow 2.x
- 모든 컴포넌트가 메타데이터 DB와 직접 통신한다.
- 워커가 DB에 직접 연결해 태스크를 실행한다.
- 사용자 코드가 DB 세션이나 모델을 import해 메타데이터 DB에 영향을 줄 수 있다.
- DB 연결 수가 과도해 확장에 부담이 될 수 있다.

### Airflow 3.x
- API 서버가 태스크와 워커 관점에서 메타데이터 DB로 가는 단일 접근 지점이다.
- 워커는 DB가 아니라 API 서버와 통신한다.
- DAG Processor와 Triggerer도 Variables, Connections 등이 필요할 때 Task Execution 메커니즘을 사용한다.

## Task Execution API와 Task SDK가 하는 일
Task SDK 문서에서 다음 내용을 명시한다.
- 태스크 코드의 메타데이터 DB 직접 접근을 제한한다.
- Task Execution API가 상태 전이, heartbeat, XCom, 리소스 fetch 같은 런타임 상호작용을 처리한다.
- 서비스 지향 아키텍처를 지원하며, 새 Task Execution API를 통해 태스크를 원격 실행할 수 있다.
- 원격 실행을 위해 Task SDK를 제공하며, 컨테이너, 엣지 환경, 다른 런타임 같은 외부 시스템에서 Airflow 태스크를 실행할 수 있다.
- Airflow 3.0에서 DAG 작성 인터페이스를 `airflow.sdk` 네임스페이스로 제공한다.

## Airflow 3.0 릴리스 관점 설명
Airflow 3.0 릴리스 블로그는 AIP-72 Task Execution Interface를 다음처럼 설명한다.
- Airflow를 클라이언트-서버 아키텍처로 진화시키는 핵심 구성 요소다.
- Task Execution Interface의 입력 지점으로 API 서버가 포함된다.
- 이 기반 기능이 Task Execution API 형태로 멀티 클라우드 배포와 멀티 언어 지원을 가능하게 한다.
- Airflow 3 릴리스에는 Python Task SDK가 포함되어 기존 DAG와의 호환성을 제공한다.
