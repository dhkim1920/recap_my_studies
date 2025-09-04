# Avro, Parquet, ORC 비교 

## Avro

- **저장 방식**: **Row-oriented 직렬화 포맷** (행 단위 저장, 컬럼 지향 아님)
- **특징**
  - 스키마(JSON) + 데이터(바이너리) 분리 → **스키마 진화(schema evolution)**에 강함
  - 작은 레코드 단위 직렬화/역직렬화에 최적 → 메시징, 로그 적재, 스트리밍에 적합
  - 압축 코덱: null, deflate(기본) + snappy, bzip2, xz, zstandard 등 선택 지원
- **장점**: 스키마 유연성, 빠른 직렬화/역직렬화
- **단점**: 특정 컬럼만 읽을 때 비효율적 (전체 행을 스캔해야 함)

---

## Parquet

- **저장 방식**: **Columnar**
- **특징**
  - 구글 Dremel 논문 기반, Hadoop/Spark/Hive/Presto 등 광범위한 엔진에서 표준처럼 사용
  - **Predicate Pushdown** 지원 → 컬럼 통계·사전·블룸필터 등을 활용해 불필요한 데이터 건너뜀
  - GZIP, Snappy, ZSTD 등 다양한 압축 코덱 지원
  - 복잡한 Nested 구조(JSON, struct, array) 표현 가능 (정의/반복 레벨 인코딩)
- **장점**: 범용성, 높은 호환성, 효율적인 압축 및 읽기 성능
- **단점**: 쓰기 비용이 Avro/ORC보다 높을 수 있음

---

## ORC (Optimized Row Columnar)

- **저장 방식**: **Columnar**
- **특징**
  - Hortonworks 주도로 개발, Hive 최적화에 특화
  - Predicate Pushdown + 인덱스(컬럼별 min/max, stripe 통계, Bloom filter) 제공
  - ZLIB, Snappy, ZSTD 등 다양한 압축 지원 (ORC 2.0 이후 기본 ZSTD)
  - Hive/Spark SQL 환경에서 집계·분석 쿼리에 강력
- **장점**: Hive/Spark 최적화, 높은 압축률, 인덱스 기반 빠른 쿼리
- **단점**: Parquet에 비해 다른 엔진과의 호환성이 낮음

---

## 비교 요약
| 포맷       | 저장 방식  | 장점                        | 단점              | 주 사용처 (일반적)     |
|------------|-----------|-----------------------------|-------------------|-----------------------|
| **Avro**   | Row-based | 스키마 진화, 직렬화 속도 빠름   | 컬럼 조회 비효율       | Kafka, 로그, 스트리밍   |
| **Parquet**| Columnar  | 범용성, 호환성, 성능 우수       | 쓰기 오버헤드         | 데이터 레이크, 분석 쿼리 |
| **ORC**    | Columnar  | Hive 최적화, 높은 압축률, 인덱스 | Hive 외 호환성 낮음   | Hive/Spark 분석        |

---

## 어디에 사용하면 좋을까?
- **스트리밍/로그 저장 → Avro**
- **범용 데이터 분석 → Parquet**
- **Hive 기반 집계 최적화 → ORC**
