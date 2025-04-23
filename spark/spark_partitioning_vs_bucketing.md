
# Apache Spark에서 Partitioning과 Bucketing 정리 

## 1. Partitioning in Spark

### 정의
- 데이터를 하나 이상의 컬럼 값 기준으로 디렉토리 단위로 분할하여 저장
- `.partitionBy("col1", "col2")` 형태로 사용

### 특징
- 각 파티션은 별도의 디렉토리로 구성
- 필터 조건이 파티션 컬럼에 적용되면 해당 디렉토리만 스캔하는 **Partition Pruning**이 가능
- 낮은 카디널리티 컬럼(예: 날짜, 국가)에 적합

### 예시
```python
df.write.partitionBy("year", "month").parquet("path")
```

## 2. Bucketing in Spark

### 정의
- 지정한 컬럼 값을 해시하여 고정된 수의 파일(bucket)로 나누는 방식
- `.bucketBy(n, "col")`와 `.saveAsTable()`을 함께 사용해야 동작

### 특징
- 조인 성능 최적화에 유리
- 정렬은 보장되지 않음
- 버킷 수는 고정이며 변경 시 테이블을 재생성
- 높은 카디널리티 컬럼(예: user_id, device_id)에 적합

### 예시
```python
df.write.bucketBy(8, "user_id").saveAsTable("bucketed_table")
```

## 3. Partitioning vs Bucketing 비교

| 항목            | Partitioning                            | Bucketing                                 |
|-----------------|------------------------------------------|--------------------------------------------|
| 저장 단위        | 디렉토리                                 | 파일                                        |
| 기준 컬럼        | 1개 이상, 보통 낮은 카디널리티             | 일반적으로 1개, 높은 카디널리티             |
| 필터 최적화      | O (Partition Pruning)                    | X (Spark 2.4 이상에서 Bucket Pruning 지원)  |
| 조인 최적화      | X                                         | O                                          |
| 정렬 여부        | 정렬 없음                                 | 정렬 보장되지 않음                         |
| 사용 메서드      | `.partitionBy()`                         | `.bucketBy()` + `.saveAsTable()` 필요      |

## 4. 최적 사용 전략

- **단일 필터 기반 조회가 많으면**: Partitioning 사용
- **복잡한 조인/샘플링이 많으면**: Bucketing 사용
- **두 개 조합도 가능**:
```python
df.write.partitionBy("date").bucketBy(8, "user_id").saveAsTable("table")
```

> 단, Spark에서는 Bucketing이 `.saveAsTable()`일 때만 유효
