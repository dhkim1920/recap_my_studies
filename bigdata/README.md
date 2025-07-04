## 데이터 저장 및 관리

### 데이터 레이크
**원시 데이터를 기본 형식 그대로 저장하는 방대한 저장소**  
가장 큰 장점은 **정형, 반정형, 비정형 데이터를 모두 저장 가능**

### 데이터 웨어하우스
정형 데이터 위주로 사용되며, **사전 정제된 데이터**가 저장되므로 고속의 정형 분석에 적합

### 비교
| 항목               | 데이터 레이크                     | 데이터 웨어하우스               |
|--------------------|-----------------------------------|----------------------------------|
| 데이터 형태         | 정형, 반정형, 비정형 모두 가능     | 정형 위주                         |
| 스키마 적용 시점    | 읽을 때 (Schema-on-Read)          | 쓸 때 (Schema-on-Write)          |
| 분석 대상          | 데이터 과학, 머신러닝, 저장 중심   | BI 분석, 정형 보고 중심           |
| 저장 비용           | 상대적으로 저렴                   | 상대적으로 비쌈                   |

### 스키마 적용 시점 자세히
#### 데이터 레이크: Schema-on-Read
- 저장할 때 가공하지 않고 원시 데이터(raw data)를 그대로 저장
- 나중에 데이터를 읽을 때 해석(schema parsing) 해서 분석에 사용
- 왜?
  - 유연한 데이터 수용 (정형, 비정형 모두 저장 가능)
  - 다양한 목적에 따라 여러 방식으로 해석 가능 (재가공 유리)
  - 비용 효율적 저장 (저장소만 확보하면 됨)

#### 데이터 웨어하우스: Schema-on-Write
- 데이터를 저장하기 전에 정제하고 스키마를 맞춘 후 저장
- 쿼리 성능과 일관된 데이터 품질 보장
- 왜?
  - 정형화된 데이터 분석에 초점 (BI, 리포팅 등)
  - 쿼리 시 성능 최적화 (사전 정제로 빠름)
  - 데이터 일관성/정합성 중요

---

## 데이터 파이프라인

### ETL과 ELT
데이터를 추출, 변환, 적재하는 방식으로, 데이터 파이프라인 구축의 핵심 개념

일반적으로 다음 단계를 포함합니다:
1. **Extract (추출)** – 데이터 소스에서 가져오기 (예: DB, API, 로그)
2. **Transform (변환)** – 정제, 형 변환, 결합 등 처리
3. **Load (적재)** – 데이터 웨어하우스, 데이터 레이크 등 저장소로 저장

- **ETL (Extract, Transform, Load)**: 데이터 변환 후 적재  
- **ELT (Extract, Load, Transform)**: 데이터 적재 후 변환

---

## 데이터 카탈로그란
데이터 카탈로그는 조직 내 모든 데이터를 인벤토리 형태로 정리한 메타데이터 저장소로, 
데이터 검색, 분류, 거버넌스, 보안 등을 지원하는 시스템이다.
각 데이터의 위치, 출처, 변환 과정 등을 포함한 정보를 통해 조직 내 데이터 자산을 효율적으로 관리할 수 있다.

### 데이터 카탈로그의 주요 이점

1. 신속한 데이터 검색
- 설명 태그, 출처, 변환 이력 기반으로 필요한 데이터를 빠르게 찾을 수 있음
- 분석가가 IT 의존 없이 직접 인사이트 확보 가능

2. 데이터 품질 향상
- 메타데이터 자동 수집 및 관리
- 출처, 편집 이력 등으로 신뢰도 확보 및 거버넌스 강화

3. 운영 효율성 증가
- 명명 규칙 및 지표 정의 일관성 유지
- 데이터 중복 방지 및 저장 비용 절감

4. 보안 및 규제 대응 강화
- 민감 정보 위치 파악 및 접근 이력 추적
- 개인정보 보호 및 규제 준수 지원

---

## TPC-DS

### 정의
**TPC-DS**는 의사결정 지원 시스템(DSS)의 성능을 평가하기 위한 산업 표준 벤치마크다. 
TPC(Transaction Processing Performance Council)에서 개발한 벤치마크로, 데이터 웨어하우징 환경의 다양한 워크로드를 시뮬레이션합니다.

### 목적
- 데이터 웨어하우스 시스템, 데이터베이스, 분석 엔진 등의 성능 평가 및 비교
- 복잡한 쿼리 처리 성능 측정
- 실제 비즈니스 분석 환경을 반영한 테스트

### 구성 요소
| 항목        | 내용 |
|-------------|------|
| 테이블 수    | 총 24개 테이블 (7개 팩트/정보 테이블 + 17개 차원 테이블) |
| 스키마 구조 | 스타 스키마 기반, 일부 스노우플레이크 구조 포함 |
| 쿼리 수     | 총 99개 복잡한 SQL 쿼리 |
| 쿼리 유형   | 조인, 집계, 서브쿼리, 윈도우 함수 등 다양한 OLAP 연산 |

### 특징
- 다양한 데이터 스캔 범위와 복잡성을 포함
- 실제 업무에 유사한 쿼리 시나리오 제공
- 데이터 마이닝, 리포팅 등 의사결정 지원 작업 반영
- 다양한 스케일 팩터(1GB ~ 수십 TB) 지원

### 활용
- Spark, Hive, Presto, Trino, Snowflake 등 분석 엔진 성능 테스트
- Iceberg, Delta, Hudi 등 데이터 레이크 포맷 비교
- 쿼리 최적화, 파티션 전략, 캐시 전략 검증

### 다운로드 및 사용
- TPC-DS는 공홈에서 다운로드 가능
- 데이터 생성기(toolkit) 및 스펙 문서 제공
- 다양한 데이터베이스 및 분석 플랫폼에서 사용 가능

### 요약
TPC-DS는 데이터 웨어하우징 시스템의 성능을 평가하기 위한 표준화된 벤치마크다.
실제 사용 환경을 반영한 99개의 복잡한 쿼리 세트를 통해 분석 성능을 비교할 수 있다.
