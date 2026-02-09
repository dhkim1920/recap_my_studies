
# Airflow Scheduler OOM 이슈 분석 및 해결 방안

## 1. 개요
- **현상:** Airflow 스케줄러 파드에 대용량 메모리를 할당했음에도 불구하고, 메모리 사용량이 선형적으로 증가하여 결국 OOM으로 파드가 재시작됨
- **대상 버전:** Airflow 3.0.0 ~ 3.1.3
- **주요 원인:** Docker 이미지 빌드 시 컴파일 파일(.pyc) 제거로 인한 메모리 파편화 및 OpenTelemetry(OTEL) 객체 누수

## 2. 주요 원인 상세

### ① .pyc 파일 부재로 인한 메모리 파편화 (가장 치명적)
- **원인:** Airflow 3.0.x 초기 버전의 Docker 이미지는 경량화를 위해 빌드 과정에서 `find . -name "*.pyc" -delete` 명령어로 컴파일된 Python 바이트코드 파일을 모두 삭제함
- **문제점:** 
  - 스케줄러가 프로세스를 포킹할 때마다 소스 코드를 메모리 상에서 실시간으로 재컴파일해야 함
  - 이로 인해 OS의 Copy-on-Write(CoW) 최적화가 작동하지 않고, **각 프로세스가 독립적인 메모리를 과도하게 점유**하게 됨
  - DAG 개수가 많을수록(수천 개) 메모리 소모 속도가 기하급수적으로 빨라져 50GB도 버티지 못함

### ② OpenTelemetry (OTEL) Tracing 누수
- **원인:** Airflow 3.0부터 도입된 OTEL 트레이싱 기능이 활성화된 경우, 생성된 Trace 객체가 GC되지 않고 메모리에 잔존
- **문제점:** 스케줄러 루프가 돌 때마다 메모리가 선형적으로 계속 쌓임

## 3. 영향 받는 버전 및 수정 내역

| 구분 | 버전 범위 | 상태 | 비고 |
| :--- | :--- | :--- | :--- |
| **발생 버전** | **3.0.0 ~ 3.1.3** | **Known Issue** | 해당 버전의 공식 이미지는 .pyc 파일이 제거된 상태임 |
| **수정 버전** | **3.1.4 이상** | **Fixed** | PR #58944 반영 (이미지에 .pyc 포함) |
| **수정 시기** | 2025년 12월 | Merge 완료 | 3.1.4 릴리스부터 적용 |

## 4. 관련 이슈 링크

### Core Issue
1.  **PR #58944: Do not remove .pyc and .pyo files after building Python**
    *   **내용:** 이미지 빌드 시 컴파일 파일을 지우지 않도록 수정하여 메모리 파편화 해결.
    *   **링크:** [GitHub PR #58944](https://github.com/apache/airflow/pull/58944)

2.  **Issue #58509: Airflow Memory Leak in Dag-Processor, Scheduler**
    *   **내용:** DAG가 없는 상태에서도 메모리가 새는 현상 및 3.0/3.1 버전에서의 구조적 누수 보고.
    *   **링크:** [GitHub Issue #58509](https://github.com/apache/airflow/issues/58509)

### 부가 이슈 (OTEL 관련)
3.  **Discussion #53771: Memory Leak in OpenTelemetry Tracing**
    *   **내용:** OTEL 활성화 시 스케줄러 메모리 폭증 논의.
    *   **링크:** [GitHub Discussion #53771](https://github.com/apache/airflow/discussions/53771)

## 5. Action Plan

### A. 근본적 해결 (권장)
- **버전 업그레이드:** Airflow 버전을 **3.1.4 이상**으로 업그레이드.
- **이미지 재빌드:** 만약 커스텀 이미지를 사용 중이라면, `Dockerfile`에서 `.pyc` 파일을 삭제하는 로직을 반드시 제거할 것
    ```dockerfile
    # 아래와 같은 라인이 있다면 삭제 또는 주석 처리
    # RUN find . -name "*.pyc" -delete
    ```

### B. 임시 조치 -  업그레이드 전까지 적용

**1. 스케줄러 자동 재시작 설정**
메모리가 가득 차기 전에 스케줄러 프로세스를 스스로 리셋하여 메모리를 반환시키자.
- **airflow.cfg**
    ```ini
    [scheduler]
    num_runs = 500  # 500번 루프 후 프로세스 재시작
    ```
- **환경 변수 (Kubernetes)**
    ```yaml
    env:
      - name: AIRFLOW__SCHEDULER__NUM_RUNS
        value: "500"
    ```

**2. OTEL 비활성화**
혹시 모를 누수를 방지하기 위해 명시적으로 끄자.
- **환경 변수**
    ```yaml
    env:
      - name: AIRFLOW__TRACES__OTEL_ON
        value: "False"
    ```
