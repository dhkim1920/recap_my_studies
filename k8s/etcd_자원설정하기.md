
# etcd 하드웨어 권장 사양 보고서

**대상 환경:** Kubernetes 3 Node Cluster (Airflow on K8s, 2,500 DAGs)

## 1. 개요 및 권장 등급
3개의 물리/가상 노드로 구성된 Kubernetes 클러스터는 etcd 문서 기준 **Small Cluster** (노드 50개 미만) 범주에 해당한다.
Airflow DAG가 2,500개라 하더라도, etcd에 저장되는 데이터는 Airflow의 로직이 아닌 Kubernetes 오브젝트(Pod, Secret, ConfigMap 등)의 상태 정보이므로, 물리적 노드 3개가 생성할 수 있는 부하 내에서는 Small 등급 사양으로 충분하다.
## 2. 하드웨어 구성 권장안

| 구성 요소 | 권장 사양 | 비고 |
| :--- | :--- | :--- |
| **CPU** | **2 vCPU** | 일반적인 부하에서 충분함[3, 4] |
| **Memory** | **8 GB** | 데이터 캐싱 및 워처(watcher) 관리에 충분[3, 4] |
| **Disk** | **SSD (필수)** | 낮은 지연 시간(Low Latency)이 핵심[5, 6] |
| **Disk Performance** | **50+ Seq IOPS** | 클라우드 환경에서는 Max Concurrent IOPS 3,000+ 권장[7] |
| **Network** | **1GbE** | 데이터 센터 내부 통신 권장[8] |

---

## 3. 상세 설명

### 3.1. CPU (프로세서)
*   **권장:** 2 vCPU
*   **이유:** etcd는 요청을 메모리에서 처리하므로, 노드 3개 규모와 같이 클라이언트 요청이 적은 환경(초당 1,000 요청 미만)에서는 많은 CPU가 필요하지 않습니다. 2~4 코어면 원활하게 작동합니다[4].

### 3.2. Memory (메모리)
*   **권장:** 8 GB
*   **이유:** etcd는 키-값 데이터를 적극적으로 메모리에 캐싱합니다. 3노드 클러스터의 메타데이터 크기는 100MB 미만일 가능성이 높으므로 8GB 메모리는 매우 넉넉한 수준입니다[1, 4].

### 3.3. Storage (디스크) **[가장 중요]**
*   **권장:** SSD (NVMe 또는 고성능 클라우드 SSD)
*   **이유:** etcd의 안정성은 디스크 쓰기 속도(Wal write latency)에 전적으로 의존합니다. 디스크가 느리면 하트비트 타임아웃이 발생하여 클러스터 리더 선출이 반복되는 장애가 발생할 수 있습니다[5].
*   **성능 지표:**
    *   최소 **50 Sequential IOPS**가 보장되어야 합니다[7].
    *   AWS/GCP 등 클라우드 환경에서는 `Max concurrent IOPS`가 표기되므로, 보통 **3,000 ~ 3,600 IOPS** 이상을 제공하는 디스크 타입을 선택하는 것이 안전합니다[3].

### 3.4. Network (네트워크)
*   **권장:** 1GbE, 동일 데이터 센터 배치
*   **이유:** 멤버 간 복제 지연을 최소화하기 위해 낮은 지연 시간(Low Latency)이 중요합니다. 3노드 규모에서는 1GbE 대역폭으로도 충분합니다[8].

---

## 4. 클라우드 공급자별 예시 구성 (Small Cluster 기준)
문서에서 제안하는 50노드 미만 클러스터용 레퍼런스 모델입니다[3].

*   **AWS:** `m4.large` (2 vCPU, 8GB RAM, EBS 최적화)
*   **GCE:** `n1-standard-2` + 50GB PD SSD (2 vCPU, 7.5GB RAM)

## 5. Airflow 운영 시 참고 사항
*   **부하의 분리:** 2,500개의 DAG로 인한 부하는 etcd가 아닌 **Airflow Metadata DB(PostgreSQL/MySQL)**와 **Scheduler**에 집중됩니다. etcd 사양을 늘리는 것보다 DB 사양을 확보하는 것이 성능에 더 큰 영향을 줍니다.
*   **Pod Churn:** 만약 2,500개의 DAG가 매우 짧은 시간 동안 수천 개의 Pod를 동시에 생성하고 삭제한다면, 안정성을 위해 한 단계 위인 **Medium Cluster** 사양(4 vCPU, 16GB RAM)을 고려할 수 있다



> 참고 문서: Hardware recommendations | etcd
