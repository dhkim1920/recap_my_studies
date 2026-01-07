
## 1. 정의

하둡 에코시스템을 위한 **오픈소스 컬럼 기반 스토리지 매니저**다. HDFS와 달리 자체적인 저장 엔진을 가진다.

## 2. 탄생 배경

기존 하둡 저장소들의 'Trade-off' 문제를 해결하기 위해 설계되었다.

- **HDFS (Parquet 등):** 분석 성능(Scan)은 우수하나, 데이터 갱신(Random Access)이 어렵다.
- **HBase:** 데이터 갱신(Random Access)은 빠르나, 대량 분석(Scan) 성능이 떨어진다.
- **Kudu:** 이 둘 사이의 간극을 메워 **"빠른 데이터 입력(Ingest/Update)과 고성능 분석(Analytics)을 동시에"** 지원한다.

## 3. 주요 특징

- **Mutable Data:** 데이터를 파일 단위로 덮어쓰는 것이 아니라, Row 단위의 **Insert, Update, Delete**가 가능하다.
- **Relational Model:** NoSQL 방식이 아닌, **스키마(Schema)가 정의된 테이블** 구조를 가지며 **Primary Key(PK)**를 필수적으로 사용한다.
- **Columnar Storage:** 분석 쿼리(OLAP)에 최적화된 컬럼 저장 방식을 사용하며, 벡터화된(Vectorized) 읽기를 지원한다.
- **High Integration:** Impala, Spark, MapReduce 등 기존 컴퓨팅 엔진과 긴밀하게 연동된다. (특히 Impala와의 조합이 가장 강력하다.)

## 4. 아키텍처 요약

- **Master Server:** 메타데이터 관리, 테이블 위치 추적, 시스템 조율을 담당한다.
- **Tablet Server:** 실제 데이터를 저장하고 클라이언트의 읽기/쓰기 요청을 처리한다.
- **Tablets:** 테이블은 'Tablet'이라는 파티션 단위로 나뉘어 저장된다.
- **Raft Consensus:** 데이터의 안정성과 복제(Replication)를 위해 Raft 합의 알고리즘을 사용한다. (장애 발생 시 빠른 복구가 가능하다.)
