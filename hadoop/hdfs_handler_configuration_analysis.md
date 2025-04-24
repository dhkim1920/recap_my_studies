
# HDFS Handler 설정 불균형 영향 분석

## 문제 개요

HDFS에서는 클라이언트와의 통신을 처리하기 위해 NameNode와 DataNode 각각에 핸들러 스레드를 설정

이 값들이 불균형하게 설정되면 클러스터 성능 저하 및 병목 현상 발생

## 문제 발생 시나리오
### 1. NameNode 핸들러 수 과다 설정 (`dfs.namenode.handler.count`)
- 해당 값은 **NameNode의 RPC 요청 처리 스레드 수**를 결정
- 값을 과도하게 높이면 NameNode는 더 많은 요청을 동시에 처리하려고 시도
- 그러나 **DataNode가 충분히 응답하지 못할 경우**, 전체 시스템 병목 현상이 발생

### 2. DataNode 핸들러 수 부족 (`dfs.datanode.handler.count`)
- 해당 값은 **DataNode가 처리할 수 있는 요청 수**를 제한
- 값이 너무 낮으면, NameNode 또는 클라이언트의 요청을 제때 처리하지 못함
- **하트비트, 블록 리포트, 데이터 전송 등에 지연**이 생기고, 클러스터 성능 저하

## 권장 설정
### NameNode 핸들러 수 (`dfs.namenode.handler.count`)
- **권장 계산식**: `20 × log₂(노드 수)` (최대 200)
- **예시**: 250노드 클러스터 → 약 160

### DataNode 핸들러 수 (`dfs.datanode.handler.count`)
- **기본값**: 10
- **권장값**: 64 이상 (클러스터 I/O 부하에 따라 조정)

### DataNode 최대 전송 스레드 수 (`dfs.datanode.max.transfer.threads`)
- **권장값**: 4096 이상

## 모니터링 및 조정

### 모니터링 지표
- RPC 큐 길이
- RPC 처리 시간
- DataNode의 하트비트 및 블록 리포트 지연

### 조정 방법
- 클러스터 리소스와 부하 상태를 모니터링한 후, 핸들러 수를 **균형 있게 설정**
- 불균형 발견 시, **NameNode와 DataNode의 설정을 함께 조정**
