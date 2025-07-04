## Apache Iceberg 주요 활용 사례

### 1. 레코드 단위 삭제 및 개인정보 보호 (GDPR/CCPA 대응)
- 특정 사용자의 데이터 삭제 요청에 따라 개별 레코드 안전하게 삭제 가능
- HDFS나 Parquet 단독 사용 시 어려운 작업을 Iceberg는 **ACID 기반으로 안정 처리**

### 2. 레코드 수준 업데이트가 필요한 테이블
- 반품, 정정, 상태 갱신 등이 발생하는 거래/이벤트 로그 처리에 적합
- 전체 파일 재작성 없이 **특정 행만 빠르게 업데이트 가능**

### 3. Slowly Changing Dimension (SCD) 테이블 처리
- 고객 정보, 주소, 연락처 등 불규칙하게 바뀌는 데이터를 추적 가능
- 스냅샷 + 타임트래블 기능으로 변화 이력 관리에 최적화

### 4. ACID 트랜잭션 기반 데이터 레이크
- 데이터 품질과 일관성이 중요한 DWH형 작업에 적합
- 여러 사용자/프로세스의 동시 접근 환경에서도 안전하게 동작

### 5. 과거 버전 조회(Time Travel) 및 분석
- 추세 분석, 리포트 재생산, 문제 발생 전 상태 복구 등에 활용
- 특정 시점으로 정확한 롤백 가능

### 6. 증분 로딩 및 CDC 처리
- 마지막 실행 이후 변경된 데이터만 필터링하여 로딩 가능
- 효율적인 ETL, 데이터 웨어하우스 갱신 작업에 적합

### 7. 멀티 엔진 접근을 지원하는 공유 테이블
- Spark, Flink, Trino 등 다양한 처리 엔진에서 공통 테이블 사용 가능
- 하나의 Iceberg 테이블을 다양한 워크플로우에서 공유하여 활용