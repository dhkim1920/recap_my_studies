
# HDFS Handler 설정 불균형 영향 분석

## 문제 개요
HDFS에서는 클라이언트와의 통신을 처리하기 위해 NameNode와 DataNode 각각에 handler thread를 설정할 수 있다.

이 값들이 불균형하게 설정되면 클러스터 성능 저하 및 병목 현상 발생한다.

## 문제 발생 시나리오
### 1. NameNode handler 과다 설정 
(`dfs.namenode.handler.count`)
- 해당 값은 **NameNode의 RPC 요청 처리 스레드 수**를 결정한다.
- 다라서 과도하게 높이면 NameNode는 더 많은 요청을 동시에 처리하려고 시도한다.
- 그러나 **DataNode가 충분히 응답하지 못할 경우**, 전체 시스템 병목 현상이 발생한다.

### 2. NameNode handler 부족
- 클라이언트의 HDFS 명령어(ls, get, put) 실행이 느려짐
- NameNode RPC queue가 쌓임 (RPC 요청이 대기)
- 심하면 NameNode GC 증가 → OutOfMemoryError로 NameNode 다운

### 3. DataNode handler 부족 
(`dfs.datanode.handler.count`)
- 해당 값은 **DataNode가 처리할 수 있는 요청 수**를 결정한다.
- 값이 너무 낮으면, NameNode 또는 클라이언트의 요청을 제때 처리하지 못하게된다.
- 이에 따라**heartbeat, 블록 리포트, 데이터 전송 등에 지연**이 생기고, 클러스터 성능 저하된다.

## 권장 설정
### NameNode handler count
- **권장 계산식**: `20 × log₂(노드 수)` (최대 200)
- **예시**: 250노드 클러스터 → 약 160

### DataNode handler count
- **기본값**: 10
- **권장값**: 64 이상 (클러스터 I/O 부하에 따라 조정)

### DataNode 최대 전송 스레드 수 
(`dfs.datanode.max.transfer.threads`)
- **권장값**: 4096 이상
- 부족하면? 
  - 블록 복제 (replication) 작업이 느려진다.
  - 클러스터 상태에 Under-Replication 경고 발생한다.

## 어떻게 확인할까?

### 모니터링 지표
- RPC 큐 길이를 확인 한다.
- RPC 처리 시간을 확인 한다.
- DataNode의 heart beat 과 블록 리포트 지연이 없는지 본다.

### 조정 방법
- 클러스터 리소스와 부하 상태를 모니터링한 후, 핸들러 수를 **균형 있게 설정**
- 불균형 발견 시, **NameNode와 DataNode의 설정을 함께 조정**
