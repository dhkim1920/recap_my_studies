# 클러스터 정책 Cluster Policies

## 개요
클러스터 전체 수준에서 DAG나 Task를 확인하거나 변경하기 위해 클러스터 정책을 사용할 수 있다. 또한 dag_id나 기타 속성을 기반으로 클러스터 전체 설정을 DAG에 일괄 적용할 수도 있다.

## 주요 사용 사례
- DAG나 Task가 특정 기준을 충족하는지 확인
- DAG나 Task에 기본 인수 default arguments 설정
- 사용자 정의 라우팅 로직 수행

## 세 가지 주요 클러스터 정책 유형
### dag_policy
- 매개변수: dag DAG
- 실행 시점: DagBag에서 DAG를 로드하는 시점에 실행

### task_policy
- 매개변수: task BaseOperator
- 실행 시점: DagBag에서 태스크를 파싱하여 태스크가 생성될 때 실행
- 특징: 특정 DagRun에서 실행 중인 태스크가 아니라 향후 실행될 모든 태스크 인스턴스에 적용

### task_instance_mutation_hook
- 매개변수: task_instance TaskInstance
- 적용 범위: 특정 DagRun과 관련된 단일 태스크 인스턴스
- 실행 시점과 위치: 태스크 인스턴스가 실행되기 직전에, Dag 파일 프로세서가 아닌 워커 내부에서 실행

## 예외 처리 및 우선순위
- 규정에 어긋나 로드되지 않아야 하는 DAG나 Task가 있다면 정책 내에서 AirflowClusterPolicyViolation 예외를 발생시켜 실행을 막을 수 있다.
- 의도적으로 DAG를 건너뛰고 싶다면 AirflowClusterPolicySkipDag 예외를 발생시킬 수 있으며, 이는 Airflow 웹 UI나 데이터베이스에 오류로 기록되지 않는다.
- 클러스터 정책에서 설정한 추가 속성은 DAG 파일에 정의된 속성보다 우선 적용된다.
  - 예: DAG 파일과 클러스터 정책 모두에서 sla를 설정하면 클러스터 정책의 값이 우선함

## 정책 함수 정의 방법
정책을 구성하는 방법은 두 가지이며, 정책 함수의 인수 이름은 문서에 지정된 이름과 정확히 일치해야 한다.

### airflow_local_settings.py 사용
- Python 검색 경로에 airflow_local_settings.py 파일을 생성한다.
- 정책 이름과 일치하는 호출 가능 객체 callables 를 추가한다.
- 기본적으로 AIRFLOW_HOME 내의 config 폴더 등이 검색 경로에 포함될 수 있다.

### Pluggy 인터페이스 진입점 사용
- Pluggy 인터페이스를 사용하는 사용자 정의 모듈에서 pyproject.toml 및 setuptools를 이용해 진입점 entrypoint 을 설정한다.
- 고급 사용자를 위한 방식이며 airflow.policy 그룹 내에 고유한 이름으로 등록해야 한다.

## 사용 가능한 정책 함수
### task_policy task
- 태스크가 DagBag에 로드된 후 태스크의 매개변수를 변경하거나 실행을 중지할 수 있다.
- 활용 예: 특정 큐 queue 강제, 최대 실행 시간 timeout 정책 적용

### dag_policy dag
- DAG가 로드된 후 DAG의 매개변수를 변경하거나 실행을 중지할 수 있다.
- 활용 예: 기본 사용자 강제, 모든 DAG에 태그가 구성되어 있는지 확인

### task_instance_mutation_hook task_instance
- Airflow 스케줄러가 대기열에 넣기 전에 태스크 인스턴스를 변경한다.
- 활용 예: 재시도 중 태스크 인스턴스 수정

### pod_mutation_hook pod
- 스케줄링을 위해 Kubernetes 클라이언트에 전달되기 전에 포드 V1Pod 객체 를 변경한다.
- 주 용도: 워커 포드에 사이드카 sidecar 나 초기화 init 컨테이너 추가

### get_airflow_context_vars context
- 태스크 실행 시 환경 변수로 사용할 수 있는 Airflow 컨텍스트 변수를 기본값에 주입한다.

## 적용 예시 및 주의사항
### DAG 정책 주의사항
- dag_policy는 DAG가 완전히 로드된 후에 적용된다.
- 이 정책에서 default_args 매개변수를 덮어쓰더라도 효과가 없다.
- 기본 오퍼레이터 설정을 재정의하려면 task_policy를 사용해야 한다.

### 에러 집계 모범 사례
- 적용할 확인 규칙이 여러 개라면 별도의 Python 모듈에서 규칙을 관리한다.
- 단일 정책 함수에서 이를 집계하여 하나의 AirflowClusterPolicyViolation 예외로 UI에 보고하는 방식을 권장한다.

### Task 인스턴스 변경 시 주의사항
- task_instance_mutation_hook을 활용해 재시도되는 태스크를 다른 큐로 라우팅하는 등의 처리가 가능하다.
- priority_weight는 가중치 규칙에 의해 동적으로 결정되므로 이 훅 내에서 임의로 변경할 수 없다.
