# Broadcast vs Accumulator 차이점

## 개요

| 항목         | Broadcast                         | Accumulator                        |
|--------------|-----------------------------------|------------------------------------|
| **목적**     | Driver → Executor로 데이터 전송  | Executor → Driver로 집계 데이터 전송 |
| **방향**     | 단방향 (Driver → Executors)       | 단방향 (Executors → Driver)        |
| **용도**     | 설정값, 룩업 테이블, 작은 데이터셋 공유 | 카운터, 합계, 로그 수집             |
| **특징**     | 모든 Executor에 복사본 캐싱       | 각 Executor에서 값 증가 후 Driver에서 합계 확인 |

---

## Broadcast

### 설명
- Driver가 모든 Executor에게 읽기 전용 데이터를 전달
- 모든 Executor가 동일한 데이터를 공유해야 할 때 사용
- 데이터는 각 Executor의 메모리에 캐시됨

### 사용 예시 (Java)
```java
Map<String, String> lookupTable = getLookupTable();
Broadcast<Map<String, String>> broadcastMap = sc.broadcast(lookupTable);

rdd.map(record -> {
    String value = broadcastMap.value().get(record.key); // 읽기만 가능
    return processRecord(record, value);
});
```

---

## Accumulator

### 설명
- 각 Executor가 집계할 데이터를 Driver로 보냄
- 값 추가만 가능 (쓰기 전용), Executor에서 직접 읽을 수 없음
- 예: 오류 카운트, 합계 계산 등

### 사용 예시 (Java)
```java
LongAccumulator errorCount = sc.longAccumulator("errors");

rdd.foreach(record -> {
    try {
        process(record);
    } catch (Exception e) {
        errorCount.add(1); // 쓰기만 가능
    }
});

System.out.println("Total errors: " + errorCount.value()); // Driver에서 읽기
```
