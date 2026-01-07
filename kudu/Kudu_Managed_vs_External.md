
# Managed 테이블과 External 테이블의 차이

## 1. 주요 차이

- **Managed Table (내부 테이블):** Impala가 데이터의 수명 주기를 관리한다.
- **External Table (외부 테이블):** Impala는 메타데이터만 빌려 쓸 뿐, 데이터는 Kudu가 독자적으로 관리한다.

## 2. 상세 비교표

| 구분 | Managed Table | External Table |
| --- | --- | --- |
| **성격** | Impala와 Kudu가 '한 몸'처럼 동작 | 이미 존재하는 Kudu 테이블에 빨대를 꽂는 형태 |
| **생성 방식** | `CREATE TABLE ...` (기본값) | `CREATE EXTERNAL TABLE ...` |
| **DROP 시** | **Kudu 데이터까지 모두 삭제됨** (복구 불가) | **Impala 매핑만 삭제됨** (Kudu 데이터 생존) |
| **주 사용처** | 신규 테이블 생성, 분석 전용 샌드박스 | 다른 엔진(Spark 등)과 데이터 공유, 실수 방지용 |
| **필수 속성** | 별도 속성 불필요 | `kudu.table_name` 매핑 필수 |

## 3. 문법 및 설정 예시

### A. Managed Table (데이터 생성 시)

별다른 설정 없이 만들면 Managed가 된다.

```sql
CREATE TABLE my_kudu_table (
  id INT,
  name STRING,
  PRIMARY KEY(id)
)
PARTITION BY HASH PARTITIONS 4
STORED AS KUDU;

```

### B. External Table (기존 데이터 연결 시)

`EXTERNAL` 키워드와 `kudu.table_name` 속성이 필수다.

```sql
CREATE EXTERNAL TABLE my_external_table STORED AS KUDU
TBLPROPERTIES (
  'kudu.table_name' = 'impala::default.my_kudu_table' -- 원본 Kudu 테이블명
);

```
