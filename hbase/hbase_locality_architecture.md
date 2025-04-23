
# HBase RegionServer와 DataNode 배치 전략

## 1. HBase RegionServer를 DataNode에 배치하는 이유

### 장점: Locality 최적화
- HBase는 데이터를 flush/write 할 때 HDFS에 HFile로 저장
- 이때 RegionServer가 DataNode와 같은 노드에 있다면, HDFS는 로컬 디스크에 우선적으로 저장

**장점 요약:**
- 네트워크 I/O 감소
- 디스크 접근 속도 향상
- 전체 시스템 성능 향상

> HBase는 랜덤 읽기가 많고, 읽기 병목이 생기기 쉬운 구조이기 때문에 Locality 확보가 매우 중요합니다.

### 단점: 자원 경합 발생
- MapReduce 작업이 수행되면 DataNode에 디스크 및 CPU 부하 발생
- 같은 노드에서 RegionServer도 메모리, 디스크, CPU를 공유하게 됨

**문제점:**
- RegionServer의 응답 속도 저하
- GC 지연이나 HBase read/write 지연 발생 가능

## 2. 그럼 왜 이렇게 구성할까??

- HBase는 **지연(latency)** 이 중요한 서비스용 스토리지
- Locality를 확보하지 않으면 네트워크를 타는 I/O가 많아져 read latency 급증
- 즉, HBase의 성능 핵심은 데이터가 **“가까이”** 있는가임

## 3. 최적 운영 전략 (추천)

| 구성 요소      | 위치                       | 목적                            |
|----------------|----------------------------|---------------------------------|
| NameNode       | 별도 서버 (RAID 구성)       | 메타데이터 보호                 |
| HBase Master   | Hadoop Master와 동일 (OK)  | Region 배치, split 관리         |
| RegionServer   | DataNode와 동일            | Local flush/write 확보          |
| MapReduce      | YARN NodeManager 분산      | 자원 경합을 최소화하도록 조절   |

> 또한, HBase는 MR job보다 long-running process이므로, MR이 자원을 다 쓰는 일이 없도록 YARN resource limit을 명확히 제한하는 것도 필요
