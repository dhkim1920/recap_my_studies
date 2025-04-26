# Hadoop 기본 개념 정리

## Apache Hadoop이란?
- 대규모 데이터를 **분산 저장** 및 **병렬 처리**할 수 있는 오픈 소스 프레임워크이다.  
- 저비용 하드웨어를 이용하여 대량 데이터를 저장하고 처리할 수 있다.

## Hadoop 구성 요소

| 구성 요소         | 설명                                                                 |
|------------------|-----------------------------------------------------------------------|
| **HDFS**          | 대용량 데이터 분산 저장 파일 시스템                                   |
| **YARN**          | 클러스터 자원 관리 및 작업 스케줄링                                    |
| **MapReduce**     | 데이터 병렬 처리 모델                                                 |
| **Hadoop Common** | 하둡에서 공통으로 사용되는 라이브러리와 유틸리티                       |


### 1. HDFS (Hadoop Distributed File System)
- 대용량 데이터를 여러 노드에 **분산 저장**  
- **블록 기반 저장**: 기본적으로 128MB 크기의 블록 단위로 저장  
- **마스터-슬레이브 구조**  
  - **NameNode**: 메타데이터 관리 (파일 이름, 블록 위치 등)  
  - **DataNode**: 실제 데이터 블록 저장  
- **복제 정책**: 기본 복제 수는 3으로, 데이터 안정성 확보  
  - hadoop3 부터 Erasure Coding 제공하여 1.5개만 유지가능, 복구가 느림, 자주쓰는 데이터는 안하는게 좋음
- **내결함성**: 노드 장애 시 복제본을 통해 데이터 복구  
![hdfs_architecture.png](hdfs_architecture.png)

#### HDFS 동작 흐름
1. 사용자가 데이터를 업로드하면 **NameNode**가 메타데이터를 관리  
2. 데이터가 여러 블록으로 나뉘어 **DataNode**에 분산 저장  
3. 복제본을 여러 노드에 저장하여 **데이터 안정성** 보장  

### Hadoop 2.x NameNode 메타데이터 관리
- NameNode는 파일 메타데이터를 **메모리(RAM)에 적재**해서 관리
- **파일 수와 디렉토리 수가 많아 질수록 NameNode 메모리 요구량이 증가**
- 디스크에 **fsimage**, **editlog** 파일로 메타데이터를 저장(Checkpoint)
  - 위치 설정: `dfs.namenode.name.dir` 

### fsimage란 무엇인가?
- `fsimage`는 NameNode가 관리하는 **파일 시스템 네임스페이스 전체의 스냅샷**
- 저장 내용: 디렉터리 구조, 파일 이름, 권한, 소유자, 블록 매핑 등
- NameNode 부팅 과정
  1. 디스크에서 `fsimage`와 `editlog`를 읽어 들임
  2. `editlog`에 기록된 모든 트랜잭션을 `fsimage`에 적용
  3. 새로운 `fsimage` 파일을 디스크에 저장
- `fsimage`는 읽기에는 효율적이나, 직접 수정에는 비효율적
- 파일 시스템 변경사항은 **editlog**에 기록하고, **Checkpoint** 과정에서 `fsimage`로 반영

### editlog가 커질 때 발생하는 문제
- NameNode 부팅 시, `fsimage`와 `editlog` 전체를 메모리에 로드 후, editlog를 순차 적용
- editlog가 수십만 ~ 수백만 건이면 **부팅 시간 지연** 및 **복구 실패 위험**이 급격히 증가

### Checkpoint를 통한 editlog 관리
- **Secondary NameNode** 또는 **Checkpoint Node**가 주기적으로 다음을 수행
  1. 기존 `fsimage`를 메모리에 로드
  2. `editlog`의 모든 트랜잭션을 반영
  3. 최신 `fsimage`를 생성하여 디스크에 저장
  4. editlog를 초기화(비움)
  - 이 과정을 **Checkpoint**라고 함
  - 안되는 경우?
    ```bash
    # 수동으로 먼저 확인해 본다.
    su - hdfs
    hdfs dfsadmin -safemode enter
    hdfs dfsadmin -saveNamespace
    hdfs dfsadmin -safemode leave
    ```

### HDFS에서 x 권한의 의미
- HDFS는 파일 실행을 지원하지 않는다. 
- 파일에 x 권한이 있어도 **실행 권한이 아니라 디렉터리 접근 권한**이다.
- 디렉터리에서 x 권한이 있는 경우
  - 디렉터리 안으로 진입 가능하고 내부 조회가 가능하다.
- 디렉터리에 x 권한이 없는 경우
  - 디렉터리 내부 탐색 및 파일 목록 조회가 불가
  - r(읽기) 권한만 있어도 x 권한이 없으면 디렉터리 접근이 차단된다.

---

### 2. YARN (Yet Another Resource Negotiator)
- 클러스터 리소스를 **관리 및 할당**  
- 다양한 컴퓨팅 프레임워크와 연동하여 **리소스 효율성**을 극대화  

#### YARN 구성 요소

| 구성 요소             | 설명                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------|
| **ResourceManager**  | 클러스터 전체 리소스 관리 및 스케줄링                                                    |
| **NodeManager**      | 각 노드의 리소스를 관리하며, 컨테이너(Container)를 실행                                      |
| **ApplicationMaster**| 애플리케이션 별로 실행되며, 작업을 계획하고 관리                                         |

![yarn_architecture.png](yarn_architecture.png)
#### YARN 동작 흐름
1. 애플리케이션 제출 -> **ResourceManager**가 **ApplicationMaster**를 할당  
2. **ApplicationMaster**가 작업을 분할하여 **NodeManager**에게 실행 요청  
3. 작업 수행 후 결과를 **ApplicationMaster**에게 전달  
4. **ApplicationMaster**가 작업 완료 상태를 **ResourceManager**에 보고  

---

### 3. MapReduce
- 대용량 데이터 처리를 위한 **병렬 처리 모델**  
- **Map 단계**: 입력 데이터를 Key-Value 형태로 변환  
- **Shuffle 단계**: 같은 Key를 가진 데이터를 모아서 정렬  
- **Reduce 단계**: 모인 데이터를 처리하여 최종 결과 생성  

#### MapReduce 작업 흐름
1. **Input Split**: 입력 데이터를 여러 청크로 분할  
2. **Map 단계**: 각 청크를 Key-Value 형태로 변환  
3. **Shuffle 단계**: 동일한 Key를 가진 데이터를 모아 정렬  
4. **Reduce 단계**: 모인 데이터를 처리하여 결과 출력  
5. **Output**: 처리된 데이터를 HDFS에 저장  

---

### Hadoop과 Spark의 비교

| 항목         | Hadoop                                      | Spark                                                     |
|-------------|---------------------------------------------|-----------------------------------------------------------|
| 데이터 처리  | 디스크 기반                                   | 메모리 기반                                                |
| 처리 속도    | 느림 (디스크 I/O 발생)                        | 빠름 (메모리 캐싱 활용)                                     |
| 처리 방식    | 배치 처리 (Batch Processing)                  | 배치 + 스트리밍 + 실시간 처리 가능                           |
| 구성 요소    | HDFS, YARN, MapReduce                         | Spark Core, Spark SQL, Spark Streaming, MLlib 등             |
| 개발 언어    | Java 중심                                    | Scala, Python, Java, R 등 다양한 언어 지원                   |
| 작업 유형    | 주로 배치 처리                                | 실시간 분석, 머신러닝, 스트리밍 처리 등 다양한 활용 가능       |
| 데이터 형식  | Key-Value 기반 비정형 데이터 처리에 적합        | 구조화 데이터(DataFrame), 비정형 데이터(RDD) 모두 처리 가능   |
| 데이터 복구  | 복제본 기반의 데이터 복구                     | RDD 계보를 통한 복구                                         |

### Hadoop의 주요 단점 및 Spark 대비 개선점

1. **디스크 기반 처리 속도 저하**  
   - Hadoop: 디스크 기반 처리로 I/O 병목  
   - Spark: 메모리 기반 처리로 속도 향상  

2. **실시간 처리 한계**  
   - Hadoop: 배치 처리 전용  
   - Spark: Spark Streaming을 통해 실시간 처리 지원  

3. **복잡한 개발 환경**  
   - Hadoop: MapReduce 기반 코드가 복잡하고 장황  
   - Spark: 고수준 API로 코드 간결성 증가  
   