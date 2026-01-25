# Airflow on Kubernetes 실무 운영 전략 요약

## 1. 하이브리드 실행 전략: Celery + KubernetesPodOperator

하나의 Executor에 의존하지 않고, 작업의 성격에 따라 최적의 실행 방식을 선택

- **일반 태스크 (가벼운 작업):** `Celery Executor` 기반의 공통 Worker에서 실행
- **장점:** 이미 떠 있는 워커를 사용하므로 Pod 생성 오버헤드(Latency)가 거의 없다.

- **특수/중량 태스크 (Heavyweight/Custom):** `KubernetesPodOperator (KPO)`를 사용하여 별도 Pod에서 실행
- **장점:** 특정 작업이 메모리를 과다 점유해도 공통 워커에 영향을 주지 않으며, 개별 작업에 최적화된 Docker 이미지를 사용 가능

---

## 2. 리소스 최적화 및 격리 (Multi-Tenancy)

공용 클러스터 내에서 여러 팀이나 프로젝트가 자원을 효율적으로 나눠 쓰는 방식

- **Namespace 분리:** 프로젝트별로 논리적 공간을 분리하여 자원 간섭을 원천 차단
- **Resource Quota:** 네임스페이스별 CPU/Memory 최대 사용량을 제한하여 특정 프로젝트의 독점을 방지
- **Node Selector & Tolerations:** 고성능 작업(GPU 등)이나 중요 작업은 지정된 전용 노드에서만 실행되도록 스케줄링을 제어

---

## 3. CI/CD 및 이미지/DAG 관리 자동화

대규모 환경에서 유지보수 효율을 극대화하기 위한 관리 기법

- **이미지 경량화:** 베이스 이미지를 최소화하여 Pod 기동 시 이미지 Pulling 속도를 개선
  - multi-stage build 등으로 경량화
- **Git-Sync 사이드카 활용:** * DAG 코드가 변경될 때마다 컨테이너 이미지를 새로 빌드하지 않도록하자
- `git-sync`가 사이드카 형태로 떠서 Git 저장소의 변경사항을 실시간으로 Pod 내 공유 볼륨에 동기화
- **공통 라이브러리 모듈화:** 중복되는 로직은 내부 라이브러리(Python 패키지 등)로 만들어 이미지 빌드 시 포함시켜 코드 중복을 줄임
