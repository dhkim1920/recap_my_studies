# Spark SQL vs Apache Hive 비교

| 항목 | Spark SQL | Apache Hive |
|:-----|:----------|:------------|
| 실행 엔진 | Spark (In-memory) | MapReduce, Tez, Spark (선택) |
| 처리 속도 | 빠름 (메모리 기반 처리) | 상대적으로 느림 (디스크 기반 연산) |
| API 유연성 | SQL + DataFrame + RDD 혼용 가능 | HiveQL(SQL) 고정 |
| 복잡한 로직 처리 | 복잡한 연산, 로직 구현 가능 (DataFrame API, UDF 등) | SQL 기반 제한적 처리 |
| 트랜잭션 지원 | 기본 없음 (ACID 보장 안 함, Delta Lake 등 별도 필요) | 일부 테이블 포맷(ORC 등)에서 ACID 지원 |
| 운영 편의성 | 세션 기반, Notebook/CLI 모두 편리 | CLI 또는 Script 기반 전통적 배치 운영 |
| 최적 사용 사례 | 실험적 분석, 대화형 질의, 머신러닝 파이프라인 | 대규모 데이터 웨어하우스, 정기적 ETL 배치 처리 |

---

# 최종 요약

- **Spark SQL**
  - 메모리에 올려 빠르게 분석하고, 복잡한 로직도 쉽게 작성하는 **빠른 대화형 분석용**.

- **Apache Hive**
  - 대규모 정형 데이터(파일)를 안정적으로 **주기적으로 처리하는 대형 배치 시스템**.

---

# 한 줄 정리

- Spark SQL은 **빠른 분석과 실험**에 강하고,
- Hive는 **대규모 정형 데이터 배치 처리**에 강합니다.
