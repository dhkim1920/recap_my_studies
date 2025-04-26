
# HDFS 디스크 선택 정책 정리
Hadoop의 HDFS에서는 DataNode가 여러 디스크(볼륨)를 사용할 수 있으며, 새로운 블록을 어떤 디스크에 저장할지 결정하는 정책이 필요하다.

`dfs.datanode.fsdataset.volume.choosing.policy` 설정을 통해 지정

### RoundRobinVolumeChoosingPolicy (기본값, 권장)
- **동작 방식**: 새로운 블록을 순차적으로 각 디스크에 분산 저장한다.
- **장점**: 디스크 간 균등한 데이터 분포를 유지하여 특정 디스크에 과부하가 걸리는 것을 방지한다.

### AvailableSpaceVolumeChoosingPolicy (비추천)
- **동작 방식**: 가용 공간이 가장 많은 디스크를 우선적으로 선택하여 블록을 저장한다.
- **단점**: 일부 디스크에 쓰기 병목 현상이 발생할 수 있으며, 디스크 간 데이터 분포 불균형이 생길 수 있음한다.
- hadoop 2.x 대에는 정상 동작 하지 않았고 hadoop 3.x 대에서도 아직 개선 중인 것으로 보인다.
