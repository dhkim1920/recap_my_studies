
# HDFS JournalNode Split-Brain 현상 정리

## Split-Brain이란?

**Split-brain**은 HDFS High Availability 환경에서 두 NameNode가 동시에 **Active 상태가 되는 심각한 오류 상황**이다.
<br> 이로 인해 editlog가 불일치하거나 데이터 손상이 발생할 수 있다.

## Split-Brain 발생 조건
- JournalNode가 3대 이상 구성된 Quorum Journal Manager 환경에서, **과반수 판단이 어긋나는 경우** 발생
- 예: 네트워크 단절, 일부 JournalNode 장애, ZooKeeper 오류 등으로 **각 NameNode가 자신이 유효하다고 착각**

## Split-Brain 발생 시 증상

- **두 Active NameNode 동시 존재**
  - 각각의 NameNode가 독립적으로 editlog를 JournalNode에 기록
- **메타데이터 불일치**
  - 서로 다른 editlog로 인해 metadata 정합성 붕괴
- **자동 Failover 실패**
  - ZooKeeper 감시가 정상 작동하지 못함
- **데이터 손상 가능**
  - 복구가 불가능한 log 분기점이 발생할 수 있음
  
## 예방 방법

- JournalNode는 **동시에 하나의 NameNode만 writer로 허용**
- ZooKeeper Quorum을 통한 NameNode 상태 감시
- 3대 이상의 JournalNode 구성 유지

## 복구 방법

1. 두 NameNode 중 **정상적인 메타데이터를 가진 쪽만 남기고 다른 하나는 종료**
2. **불일치한 JournalNode 포맷 후 재등록**
3. ZooKeeper와 JournalNode 상태 확인 후 HA 재구성

## 참고 문서

- [Apache HDFS - High Availability with QJM](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html)
- [Cloudera - Fault Tolerance in HDFS](https://docs.cloudera.com/runtime/7.2.0/fault-tolerance/hdfs-configuring-fault-tolerance.pdf)
