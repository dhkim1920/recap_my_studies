# Spark SQL / DataFrame 주요 연산 정리

## 1. join

- 두 개 이상의 DataFrame을 조인
- 조건 없이 join하면 Cross Join (Cartesian Product) 발생할 수 있음 → 항상 조인 조건 명시
  - 3.1 이상 부터는 끄고 켤수 있음 

**사용법**
```python
df1.join(df2, df1["id"] == df2["id"], "inner")
```

### 1. Inner Join (이너 조인)
- 양쪽 테이블 모두에 일치하는 데이터만 결과에 포함

**사용법**
```python
df1.join(df2, df1["id"] == df2["id"], "inner")
```

### 2. Left Outer Join (레프트 아우터 조인)

- 왼쪽 테이블(df1)의 모든 데이터를 결과에 포함
- 오른쪽 테이블에 매칭이 없으면 NULL로 채움

**사용법**
```python
df1.join(df2, df1["id"] == df2["id"], "left_outer")
df1.join(df2, df1["id"] == df2["id"], "left")
```

### 3. Right Outer Join (라이트 아우터 조인)

- 오른쪽 테이블(df2)의 모든 데이터를 결과에 포함
- 왼쪽 테이블에 매칭이 없으면 NULL로 채움

**사용법**
```python
df1.join(df2, df1["id"] == df2["id"], "right_outer")
df1.join(df2, df1["id"] == df2["id"], "right")
```

### 4. Full Outer Join (풀 아우터 조인)

- 양쪽 테이블 모두를 결과에 포함
- 어느 한쪽이 없으면 NULL로 채움

**사용법**
```python
df1.join(df2, df1["id"] == df2["id"], "full_outer")
df1.join(df2, df1["id"] == df2["id"], "full")
```

### 5. Self Join (셀프 조인)

- 하나의 테이블을 자기 자신과 조인
- 주로 계층 구조나 자기 비교에 사용

**사용법**
```python
df1.alias("a").join(df1.alias("b"), col("a.manager_id") == col("b.employee_id"))
```

### 6. Cross Join (크로스 조인)

- 모든 레코드 조합을 생성하는 조인
- A 테이블과 B 테이블의 모든 경우를 곱
- spark.sql.crossJoin.enabled=true 설정 필요

**사용법**
```python
df1.crossJoin(df2)
df1.join(df2) # Spark 3.1 이상
```

### 조인 종류 요약

| 조인 종류 | 설명 | 특징 |
|:----------|:-----|:-----|
| inner join | 양쪽 일치하는 데이터만 결과 포함 | 가장 일반적 |
| left outer join | 왼쪽 데이터는 모두 포함 | 오른쪽 없으면 NULL |
| right outer join | 오른쪽 데이터는 모두 포함 | 왼쪽 없으면 NULL |
| full outer join | 양쪽 모두 결과 포함 | 없는 쪽은 NULL |
| self join | 자기 자신과 조인 | 계층형 데이터 조회 |
| cross join | 모든 조합 생성 | 데이터 폭발 주의 |

---

## 2. select

- 컬럼 추출 또는 변형

**사용법**
```python
df.select("name", "age")
df.selectExpr("age + 10 as age_plus_10")
```

---

## 3. withColumn

- 컬럼 추가 또는 수정

**사용법**
```python
df.withColumn("new_age", col("age") + 1)
```

**주의사항**
- 여러 번 호출 시 성능 저하 가능 → select로 대체 고려

---

## 4. when

- 조건부 컬럼 생성 (CASE WHEN)

**사용법**
```python
df.withColumn(
    "age_group",
    when(col("age") < 20, "Teenager")
    .when(col("age") < 40, "Adult")
    .otherwise("Senior")
)
```

---

## 5. filter / where

- 행(row) 필터링

**사용법**
```python
df.filter(col("age") > 20)
df.where(col("age") > 20)
```

---

## 6. groupBy + agg

- 그룹별 집계 연산

**사용법**
```python
df.groupBy("department").agg(
    avg("salary").alias("avg_salary"),
    max("salary").alias("max_salary")
)
```

---

## 7. orderBy / sort

- 결과 정렬

**사용법**
```python
df.orderBy(col("age").desc())
df.sort("name", "age")
```

---

# Spark SQL 최적화 

## Shuffle Join vs Broadcast Join

| 항목 | Shuffle Join | Broadcast Join |
|:-----|:-------------|:---------------|
| 작동 방식 | 양쪽 데이터 셔플 발생 | 작은 테이블을 Executor에 복제 |
| 성능 | 느림 (네트워크 비용 큼) | 빠름 (네트워크 이동 없음) |
| 추천 상황 | 양쪽 테이블 모두 클 때 | 한쪽 테이블이 충분히 작을 때 |
| 메모리 부담 | 적음 | 브로드캐스트 테이블 만큼 부담 |

**Broadcast Join 예시**
```python
from pyspark.sql.functions import broadcast
df_large.join(broadcast(df_small), "id")
```

---

## Partitioning (partitionBy)

- 파일 저장 시 특정 컬럼 기준으로 분할 저장

**사용법**
```python
df.write.partitionBy("year", "month").parquet("path/to/output")
```

**효과**
- WHERE 조건에 Partition 컬럼을 사용하면 필요한 파일만 읽어 성능 향상

---

## Bucketing (bucketBy)

- 해시 기반으로 버킷 나누기 → 조인, 그룹 성능 최적화

**사용법**
```python
df.write.bucketBy(100, "user_id").saveAsTable("bucketed_table")
```

**효과**
- 동일 버킷끼리 조인하면 shuffle 없이 처리

---
