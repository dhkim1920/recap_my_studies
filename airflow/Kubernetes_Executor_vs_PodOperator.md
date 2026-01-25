
# Airflow on Kubernetes: Executor vs PodOperator

## 1. Kubernetes Executor

Airflow 스케줄러가 Task 인스턴스마다 개별 Pod를 생성하여 실행하는 **실행 메커니즘**

- **동적 할당:** Task가 생성될 때 Pod가 생성되고, 종료되면 Pod도 삭제 (Scale-to-Zero)
- **리소스 효율성:** 상시 가동되는 Worker가 필요 없어 클라우드 비용 절감에 유리
- **격리성:** 각 Task가 독립된 환경에서 실행되므로 의존성 충돌이 없다.
- **설정 방식:** `airflow.cfg` 또는 DAG의 `executor_config`를 통해 리소스(CPU/Mem)를 세밀하게 제어 가능

---

## 2. KubernetesPodOperator

특정 Task를 정의할 때 사용하는 **Operator**로, Airflow 외부의 컨테이너 환경을 호출하는 방식

- **언어 독립성:** Airflow(Python) 환경과 상관없이 Java, Go, R 등 모든 언어의 Docker 이미지를 실행 가능
- **완전한 분리:** Task 로직과 Airflow 라이브러리 간의 결합도가 0에 가깝다.
- **범용성:** `CeleryExecutor`나 `LocalExecutor`를 사용하는 환경에서도 특정 Task만 K8s에서 실행하고 싶을 때 사용 가능 (Celery랑 하이브리드로 사용 가능)
- **설정 예시:**
```python
k8s_task = KubernetesPodOperator(
    task_id="run_container",
    image="my-custom-image:latest",
    namespace="airflow",
    name="k8s-pod-example"
)

```

---

## 3. 주요 비교 요약

| 항목 | Kubernetes Executor | KubernetesPodOperator |
| --- | --- | --- |
| **개념** | Airflow의 **실행 인프라 결정** | 개별 **Task의 실행 도구** |
| **환경 구성** | Airflow Worker 이미지 내에서 실행 | 사용자가 지정한 임의의 이미지에서 실행 |
| **주요 장점** | 인프라 관리 자동화 및 비용 최적화 | 실행 환경의 완전한 자유도 (Docker 기반) |
| **의존성** | Airflow 설정 및 설치된 패키지에 의존 | Docker 이미지 내부 설정에만 의존 |
| **적합한 사례** | 일반적인 데이터 파이프라인 운영 | 복잡한 라이브러리 사용 혹은 이기종 언어 작업 |
