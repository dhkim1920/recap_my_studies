
# 메타데이터 카탈로그와 데이터 디스커버리

## Data Catalog

- **정의**: 조직 내 모든 데이터 자산의 **메타데이터를 통합 관리**하고, 이를 기반으로 데이터 검색·탐색을 지원하는 시스템
- **역할**
  - 메타데이터를 수집·저장·관리(= 메타데이터 카탈로그 역할)  
  - 검색, 추천, 접근 제어, 품질 지표 제공(= 데이터 디스커버리와 연결)  
- **관계**: 데이터 카탈로그라는 큰 개념 안에 메타데이터 카탈로그와 디스커버리 기능이 포함됨

### 예시
1. **AWS Glue Data Catalog**  
   - AWS의 대표적인 데이터 카탈로그 서비스
   - S3/Hive/Hudi/Iceberg에 저장된 테이블 메타데이터를 수집하고, Athena·Redshift·EMR이 공통 스키마로 활용 가능
2. **Google Cloud Data Catalog (Dataplex 포함)**  
   - BigQuery, Pub/Sub, GCS 등 GCP 리소스의 메타데이터를 통합 관리
   - 태그 기반 검색과 데이터 계보(Lineage) 추적 제공

## Metadata Catalog

- **정의**: 조직 내 존재하는 데이터 자산(테이블, 파일, 컬럼, 스키마 등)의 메타데이터를 체계적으로 수집·저장·관리하는 시스템
- **역할**: 데이터에 대한 '사전(사람이 이해할 수 있는 정의)' 제공, 계보(Lineage) 추적, 표준화 지원

### 예시
1. **AWS Glue Data Catalog**  
   - S3에 저장된 데이터셋의 스키마와 위치를 자동으로 크롤링하여 저장
   - Athena, Redshift Spectrum, EMR 등이 동일 스키마로 데이터를 참조 가능
   - 예: `user_events` 테이블 → S3 `s3://datalake/events/` 경로, 컬럼 정보(`user_id`, `event_time`) 저장.
2. **Apache Atlas**  
   - Hadoop/Hive 환경에서 데이터 테이블의 계보(Lineage) 및 보안 태깅 제공
   - 예: `raw_logs` → `cleaned_logs` → `user_activity_summary` 변환 과정을 추적 가능

## Data Discovery

- **정의**: 사용자가 조직 내 수많은 데이터셋을 쉽게 탐색·검색할 수 있도록 지원하는 시스템
- **역할**: 검색·추천 기능 제공, 데이터 품질·활용도 기반 탐색, 담당자와 활용 예시 정보 확인

### 예시
1. **Amundsen (Lyft 오픈소스)**  
   - 검색창에 "user retention" 입력 시 관련 테이블(`user_retention_daily`) 및 소유자, 조회 빈도 노출
   - 분석가가 신뢰할 수 있는 데이터셋을 빠르게 탐색 가능
2. **LinkedIn DataHub**  
   - 테이블, Kafka 토픽, ETL 파이프라인까지 포함한 전체 데이터 계보 제공 
   - 예: "payments" 검색 시 `payments_transaction` 테이블, 파생 ETL 잡, 대시보드까지 연결 관계 확인

---

## 차이점 요약

- **데이터 카탈로그**: 가장 큰 개념. 메타데이터 관리 + 검색/탐색 기능 모두 포함
- **메타데이터 카탈로그**: 데이터 정의/구조를 체계적으로 저장·관리 → 데이터 사전
- **데이터 디스커버리**: 저장된 메타데이터를 활용해 사용자가 데이터를 검색·탐색 → 데이터 검색엔진
