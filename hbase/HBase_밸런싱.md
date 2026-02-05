## HBase 자동 리밸런싱

### 주기적 실행

- `hbase.balancer.period` 설정을 통해 주기적으로 Region 부하 불균형을 감지하여 자동 분산 수행
- 기본값은 `300000` (5분)이며, 단위는 밀리초
- 수행 주기는 설정값으로 조정 가능

### 활성화 여부

- `hbase.balancer.enabled = true` 시 자동 밸런싱 활성화된다.
- 기본값은 true (활성화 상태)

### 동작 방식

- HMaster가 RegionServer 간 Region 개수, 크기, locality를 기준으로 불균형 여부를 평가
- 평가 결과에 따라 특정 Region을 다른 서버로 이동시킨다.

### 예시 설정

```properties
hbase.balancer.enabled = true
hbase.balancer.period = 300000          # 5분 주기
hbase.balancer.max.balancing = 0.1      # 이동 비율 제한 (10%)
```

- 위 설정은 RegionServer 간 Region 개수 또는 용량이 차이 날 경우 자동으로 재분배시킨다.

---

## HDFS disk rebalancer와 같이 사용해도 될까?

결론부터 말하면, HBase의 Region Balancer와 HDFS의 블록 Balancer는 **호환되지 않음**으로 명시되어 있다.

## HDFS Balancer와 HBase Balancer의 차이

### HDFS Balancer의 동작 방식
- HDFS Balancer는 블록 단위로만 작동하며, HDFS 내부의 블록 분포를 평준화하기 위해 동작한다.

### HBase Balancer의 동작 방식
- Region 개수 또는 용량 차이, Locality 등을 기준으로 Region을 재분배한다.

## 결론
- 수행은 가능하나 **권장되지는 않는다**.

## 이유
- `hbase:meta`는 Region의 시작 키, 종료 키, 테이블 이름, 할당된 RegionServer 정보를 저장하며, HFile의 DataNode 위치는 저장하지 않는다.
- 따라서 HBase 데이터가 손상되지는 않는다.
- 그러나 두 Balancer의 목적이 다르며, 특히 HDFS Balancer 실행 시 HFile 블록이 이동하면서 HBase의 Locality가 깨진다.
- 이로 인해 RegionServer가 원격 DataNode에서 데이터를 읽게 되어 **성능 저하**가 발생할 수 있다.

## 그래도 돌려야 한다면?
- HDFS Balancer 수행 후, **HBase Major Compaction**을 통해 Locality를 회복하는 것이 필요하다.
  - 이럴경우 HFile이 병합되면서 다시 Block이 새로 기록되니 근본적인 원인은 아닐 듯?
