## HBase 자동 리밸런싱

### 주기적 실행

- `hbase.balancer.period` 설정을 통해 주기적으로 Region 부하 불균형을 감지하여 자동 분산 수행
- 기본값은 `300000` (5분)이며, 단위는 밀리초
- 수행 주기는 설정값으로 조정 가능

### 활성화 여부

- `hbase.balancer.enabled = true` 시 자동 밸런싱 활성화됨
- 기본값은 true (활성화 상태)

### 동작 방식

- HMaster가 RegionServer 간 Region 개수 또는 Region 크기를 기준으로 불균형 여부를 평가
- 평가 결과에 따라 특정 Region을 다른 서버로 이동시킴

### 예시 설정

```properties
hbase.balancer.enabled = true
hbase.balancer.period = 300000          # 5분 주기
hbase.balancer.max.balancing = 0.1      # 이동 비율 제한 (10%)
```

- 위 설정은 RegionServer 간 Region 개수 또는 용량이 차이 날 경우 자동으로 재분배함
---
## HDFS 디스크 리밸런싱과의 동시 실행 금지 이유

HBase의 Region 밸런서와 HDFS의 블록 밸런서는 **호환되지 않음**으로 명시되어 있다.

### 공식 문서 내용
> HBase Balancer와 HDFS Balancer는 호환되지 않습니다.

- HDFS Balancer는 HDFS 블록을 DataNode 간에 고르게 분산시키려 합니다. 
- 반면, HBase는 region 분할이나 장애 발생 후 compaction을 통해 locality(지역성)를 복구하는 방식에 의존합니다. 
- 이 두 종류의 리밸런싱은 함께 사용하면 잘 작동하지 않습니다.

### 이유
1. **리소스 충돌**
   - 두 리밸런서가 동시에 네트워크, 디스크 IO를 사용할 경우 성능 저하 및 충돌 발생 가능

2. **Region 이동과 블록 복제의 충돌**
   - HBase Region 이동 중 해당 HFile의 블록이 HDFS balancer에 의해 동시에 이동되면, RegionServer가 해당 파일을 원격으로 읽게 되어 locality가 깨짐

3. **Compaction 등의 내부 처리와 충돌**
   - HBase는 compaction 중 HFile을 재작성하는데, 이 시점에 HDFS 블록도 이동되면 내부 오류나 성능 저하가 발생할 수 있음

### 공식 권장

- 두 리밸런서는 **동시에 실행하지 말 것**
- 순차적으로 실행하고, 리밸런싱 시점에 HBase 트래픽이 적을 때 수행 권장
