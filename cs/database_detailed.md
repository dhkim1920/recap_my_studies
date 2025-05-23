## 데이터베이스

### 데이터베이스의 큰 그림
- **DBMS (Database Management System)**: 데이터의 저장, 검색, 갱신, 삭제 등을 관리하는 시스템 소프트웨어
- 파일 시스템보다 효율적인 이유
  - 빠른 검색 (인덱스)
  - 동시성 제어 (Lock, MVCC)
  - 무결성 유지 및 장애 복구 기능
- **Transaction**
  - 데이터베이스의 상태를 변화시키는 작업의 단위
  - ACID 원칙:
    - **원자성 (Atomicity)**: 트랜잭션은 모두 수행되거나 전혀 수행되지 않아야 함
    - **일관성 (Consistency)**: 트랜잭션 수행 전후 데이터 무결성 유지
    - **고립성 (Isolation)**: 동시에 실행되는 트랜잭션 간 간섭 방지
    - **지속성 (Durability)**: 트랜잭션 완료 후 결과는 영구 저장됨

---

### RDBMS와 SQL

- **RDBMS (Relational Database Management System)**:
  - 관계형 모델 기반 테이블 구조
  - 각 테이블은 고유 키(PK)와 외래 키(FK) 등으로 관계를 표현
- **SQL (Structured Query Language)**:
  - DDL (CREATE, ALTER 등), DML (SELECT, INSERT 등), DCL (GRANT, REVOKE)
  - 주요 문법:
    - SELECT ... FROM ... WHERE ...
    - JOIN (INNER, OUTER, LEFT, RIGHT)
    - GROUP BY, HAVING, ORDER BY

---

### RDBMS의 기본

- **정규화(Normalization)**:
  - 중복 최소화, 무결성 유지
  - 1NF, 2NF, 3NF 등 단계별 분리
- **인덱스(Index)**:
  - 검색 성능 향상
  - B-Tree 기반 구조가 일반적
- **옵티마이저(Query Optimizer)**:
  - SQL 실행 계획 수립
  - 통계 정보 기반 비용 기반 최적화 수행

---

### NoSQL

- **NoSQL**:
  - Not Only SQL: 비정형 또는 반정형 데이터에 적합
  - 수평 확장성(Horizontal Scalability)에 강점
  - 스키마 유연성, 고가용성

#### 주요 유형 및 특징

- **Key-Value Store**:
  - 예: Redis, Riak
  - 빠른 읽기/쓰기 성능, 단순 구조
- **Document Store**:
  - 예: MongoDB, CouchDB
  - JSON, BSON 형식으로 저장, 유연한 구조
- **Column Store**:
  - 예: Cassandra, HBase
  - 대용량 분석용에 적합
- **Graph DB**:
  - 예: Neo4j
  - 노드-엣지 구조, 관계 탐색에 최적

#### 대표 NoSQL

- **MongoDB**:
  - 도큐먼트 기반, BSON 포맷
  - 복잡한 쿼리와 인덱스 지원
- **Redis**:
  - 인메모리 키-값 저장소
  - TTL, pub/sub, 캐시, 세션 저장 등에 활용
  