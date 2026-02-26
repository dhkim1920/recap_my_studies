# Dag 번들 Dag Bundles

## 정의
Dag 번들은 하나 이상의 Dag 파일과 이와 연관된 파일의 모음이다. 예로 다른 Python 스크립트, 구성 파일, 기타 리소스가 포함될 수 있다.

## 가져올 수 있는 위치
- 로컬 디렉토리
- Git 리포지토리
- 기타 외부 시스템

배포 관리자는 사용자 지정 소스를 지원하기 위해 자체 Dag 번들 클래스를 작성할 수 있으며, Airflow 배포 환경에서 둘 이상의 Dag 번들을 정의해 Dag를 더 효율적으로 구성할 수 있다.

## 목적과 특징
- 번들을 상위 레벨로 유지하여 Dag 실행에 필요한 모든 요소를 버전 관리할 수 있다.
- Airflow 2 및 이전 버전의 Dags 폴더와 유사하지만 더 강력한 기능을 제공한다.
- 버전 관리를 지원하여 특정 버전의 Dag 번들을 사용해 작업을 실행하도록 보장한다.
- 실행 중간에 Dag가 업데이트되더라도 전체 실행 동안 동일한 코드를 사용할 수 있게 한다.

## 왜 중요한가
### 버전 제어 Version Control
실행 중간에 Dag가 업데이트되더라도 전체 실행 과정에서 동일한 코드를 사용할 수 있도록 한다.

### 확장성 Scalability
수많은 Dag를 논리적인 단위로 구성하여 Airflow가 이를 효율적으로 관리할 수 있도록 한다.

### 유연성 Flexibility
Git 리포지토리 같은 외부 시스템과 통합해 Dag를 소싱할 수 있도록 지원한다.

## Dag 번들의 종류
Airflow는 특정 사용 사례에 맞춘 여러 유형의 Dag 번들을 지원한다.

### airflow.dag_processing.bundles.local.LocalDagBundle
- Dag 파일이 포함된 로컬 디렉토리를 참조한다.
- 개발 및 테스트 환경에 이상적이다.
- 번들의 버전 관리를 지원하지 않으므로 작업은 항상 최신 코드를 사용하여 실행된다.

### airflow.providers.git.bundles.git.GitDagBundle
- Git 리포지토리와 통합된다.
- Airflow가 리포지토리에서 직접 Dag를 가져올 수 있게 한다.

### airflow.providers.amazon.aws.bundles.s3.S3DagBundle
- Dag 파일이 포함된 S3 버킷을 참조한다.
- 번들의 버전 관리를 지원하지 않으므로 작업은 항상 최신 코드를 사용하여 실행된다.

## 구성 Configuring Dag bundles
- Dag 번들은 dag_bundle_config_list에서 구성한다.
- 하나 이상의 Dag 번들을 추가할 수 있다.
- 이전 버전과의 호환성을 위해 Airflow는 기본으로 기존 Dags 폴더 역할의 로컬 Dag 번들을 추가한다.
- 원하지 않으면 기본 로컬 Dag 번들을 제거할 수 있다.
- 기본 로컬 Dag 번들을 유지하면서 Git Dag 번들 등 다른 번들을 추가할 수도 있다.

### URL 관련
- Dag 번들에서 제공하는 기본 URL과 다른 뷰 URL이 필요하면 구성의 kwargs에서 URL을 변경할 수 있다.
- 번들 속성을 나타내는 자리 표시자 예 {subdir} 를 사용할 수 있다.
- URL은 안전성 검증을 거치며 안전하지 않다고 판단되면 보안을 위해 None으로 설정된다.

### refresh_interval
- kwargs로 각 Dag 번들마다 refresh_interval을 덮어쓸 수 있다.
- Dag 프로세서가 번들을 새로 고치거나 새 파일을 찾는 주기를 제어한다.

### Git 설치 관련
- Airflow 3.0.2부터 기본 이미지에 git이 사전 설치되어 있다.
- 그 이전 버전은 Docker 이미지에 git을 직접 설치해야 한다.

## 사용자 가장과 함께 사용 Using DAG Bundles with User Impersonation
DAG 번들과 함께 run_as_user를 사용할 때는, 가장된 사용자가 기본 Airflow 프로세스가 생성한 번들 파일에 접근할 수 있도록 파일 권한을 설정해야 한다.

- 모든 가장된 사용자와 Airflow 사용자는 동일한 그룹에 속해야 한다.
- umask 설정 예 umask 0002 을 구성해야 한다.

이 권한 기반 접근 방식은 임시 해결책이며, 향후 버전의 Airflow는 슈퍼바이저 기반 번들 작업을 통해 다중 사용자 액세스를 처리하여 공유 그룹 권한의 필요성을 없앨 예정이다.

## 사용자 정의 Dag 번들 작성 Writing custom Dag bundles
BaseDagBundle 클래스를 확장해 자체 Dag 번들을 구현할 때 다음 메서드를 구현한다.

### 추상 메서드 Abstract Methods
#### path
- 이 번들의 Dag 파일이 저장된 디렉토리의 Path를 반환해야 한다.
- Airflow는 처리할 Dag 파일을 찾기 위해 이 속성을 사용한다.

#### get_current_version
- 번들의 현재 버전을 문자열로 반환해야 한다.
- Airflow는 작업을 실행할 때 해당 버전의 번들을 다시 가져오기 위해 이 버전을 __init__에 전달한다.
- 버전 관리가 지원되지 않으면 None을 반환해야 한다.

#### refresh
- 원본에서 번들의 내용을 새로 고치는 작업을 처리해야 한다.
- 예 원격 리포지토리에서 최신 변경 사항 가져오기
- Dag 프로세서가 번들을 최신 상태로 유지하기 위해 주기적으로 사용한다.

### 선택적 메서드 Optional Methods
#### __init__
- GitDagBundle의 tracking_ref 같은 추가 매개변수로 번들을 초기화하도록 확장할 수 있다.
- 적절한 초기화를 위해 부모 클래스의 __init__ 메서드를 호출해야 한다.
- 네트워크 호출처럼 비용이 많이 드는 작업은 인스턴스화 중 지연을 막기 위해 피해야 한다.
- 비용이 큰 작업은 initialize 메서드에서 수행해야 한다.

#### initialize
- 번들이 Dag 프로세서나 워커에서 처음 사용되기 전에 호출된다.
- 번들의 콘텐츠에 접근할 때만 비용이 많이 드는 작업을 수행하도록 허용한다.

#### view_url
- 외부 시스템 예 Git 리포지토리의 웹 인터페이스 에서 번들을 볼 수 있는 URL을 문자열로 반환해야 한다.

## 기타 고려사항 Other Considerations
### 버전 관리 Versioning
번들이 버전 관리를 지원하는 경우 initialize, get_current_version, refresh가 버전별 로직을 처리하도록 구현되어야 한다.

### 동시성 Concurrency
- 워커는 많은 번들을 동시에 생성할 수 있다.
- 번들 객체에 대한 호출을 직렬화하지 않는다.
- 기본 기술에서 문제가 발생할 수 있다면 번들 클래스가 자체적으로 잠금 처리를 해야 한다.
- 예 리포지토리 복제 시 하나의 번들 객체만 복제하도록 보장

### 트리거러 제한 Triggerer Limitation
- DAG 번들은 트리거러 구성 요소에서 초기화되지 않는다.
- 트리거가 DAG 번들 내의 코드에서 올 수 없다.
- 사용자 정의 트리거가 필요하면 DAG 번들이 아니라 Python 환경의 sys.path에서 사용할 수 있도록 구성해야 한다.
