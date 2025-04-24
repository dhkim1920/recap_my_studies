
# Apache Phoenix Query Hints

## Hint?

**Hint** 는 SQL 주석 형식으로 작성되며, 쿼리 실행 계획에 영향을 주도록 **옵티마이저에 지시**하는 수단 

Phoenix에서는 특정 쿼리의 실행 방식이 기본 옵티마이저 판단보다 비효율적일 경우, 힌트를 통해 명시적으로 **원하는 실행 방식**을 강제할 수 있음

**주요 목적**:
- 비효율적인 쿼리 실행 방지
- 성능 저하 요소 회피 (ex. Full Scan)
- 메모리/리소스 낭비 방지

---

## 주요 힌트 5가지

### 1. `RANGE_SCAN`

- **설명**: 옵티마이저에게 **rowkey 범위 조건을 이용한 range scan**을 명시적으로 사용하라고 지시  
- **용도**: 범위 조건이 명확히 있음에도 옵티마이저가 full scan을 선택하는 경우 강제 조정
- **예시**:
  ```sql
  SELECT /*+ RANGE_SCAN */ * 
  FROM sales_data 
  WHERE ts >= '2024-01-01' AND ts < '2024-02-01';
  ```

---

### 2. `NO_CACHE`

- **설명**: 해당 쿼리의 결과 데이터를 HBase block cache에 **올리지 않도록** 설정  
- **용도**: 일회성 쿼리, 분석 쿼리 등에서 **hot data 캐시 오염 방지**
- **예시**:
  ```sql
  SELECT /*+ NO_CACHE */ * 
  FROM logs 
  WHERE category = 'tmp';
  ```
> 참고: hot data란? 자주 조회되는 데이터를 말함, 여기서 hot date 캐시 오염은 일회성 데이터임에도 불구하고
> 조회 결과량이 많은 경우 hot data가 block cache에서 밀려나는 현상을 말함
---

### 3. `SKIP_SCAN`

- **설명**: 복합 rowkey의 **후행 컬럼에만 조건이 있을 때**, 스킵 스캔(skip scan) 방식으로 처리  
- **용도**: 선행 키가 누락된 조건에서, 전체 테이블 스캔을 피하고 효율적으로 접근하도록 유도  
- **예시**:
  ```sql
  SELECT /*+ SKIP_SCAN */ * 
  FROM user_activity 
  WHERE user_type = 'admin';
  ```
  *(rowkey가 (region, user_type) 구조일 경우)*

---

### 4. `NO_INDEX`

- **설명**: 존재하는 인덱스가 있어도 **사용하지 말고 원본 테이블만** 사용하도록 강제  
- **용도**: 인덱스가 잘못 선택되어 성능이 나쁠 때 강제로 배제
- **예시**:
  ```sql
  SELECT /*+ NO_INDEX */ * 
  FROM customer 
  WHERE age > 30;
  ```

---

### 5. `USE_DATA_OVER_INDEX_TABLE`

- **설명**: 옵티마이저가 인덱스 테이블을 선택하더라도, **데이터 테이블 사용을 강제**  
- **용도**: 인덱스가 효율적이지 않거나 인덱스 조회 후 다시 테이블 조회가 필요한 상황 방지
- **예시**:
  ```sql
  SELECT /*+ USE_DATA_OVER_INDEX_TABLE */ name 
  FROM product 
  WHERE price > 1000;
  ```

