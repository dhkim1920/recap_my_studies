# Oracle CDC: Supplemental Logging

## 1. 개요
Oracle 데이터베이스의 기본 로그(Redo Log)는 주로 장애 복구를 목적으로 설계되었다. 따라서 CDC 환경에서는 변경된 행을 고유하게 식별하기 위한 정보가 부족할 수 있는데, 이를 보완하기 위해 로그에 추가 정보를 기록하는 것이 **Supplemental Logging**이다.

## 2. 왜 필요한가? 
기본 Redo Log는 변경된 컬럼의 데이터만 기록하는 경우가 많습니다. 하지만 CDC 툴이 데이터를 정확히 추출하려면 다음 정보가 필요다.

- **PK:** 어떤 행이 바뀌었는지 식별하기 위한 정보
- **Before Image:** 수정 전의 값 (Update 시 비교를 위함),
Oracle은 효율성을 위해 기본 로그에서 이를 생략하므로, CDC를 하려면 "추가로 더 기록해라"라는 명령이 필수적

## 3. 설정 단계

### 3.1 Database Level (Minimal Supplemental Logging)
가장 먼저 데이터베이스 수준에서 최소한의 보충 로깅을 활성화해야 한다. 이 설정이 없으면 테이블 단위 설정이 무시된다.

```sql
-- 활성화 여부 확인
SELECT supplemental_log_data_min FROM v$database;

-- 활성화 명령어
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;

```

### 3.2 Table Level
특정 테이블의 데이터를 CDC 하려면 해당 테이블에 어떤 컬럼 정보를 로그에 남길지 지정

- **Primary Key Logging:** 모든 행 변경 시 PK 값을 로그에 남김 (가장 일반적)
```sql
ALTER TABLE [테이블명] ADD SUPPLEMENTAL LOG DATA (PRIMARY KEY) COLUMNS;

```

- **All Column Logging:** 모든 컬럼의 전/후 값을 로그에 남김 (로그 발생량이 많아지므로 주의)
```sql
ALTER TABLE [테이블명] ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;

```

> 보통 DBA 또는 DB 담당자가 설정하기 때문에 데이터 엔지니어가 직접 설정하는 경우는 잘 없다. 

## 4. 작동 방식

1. **Redo Log 생성:** 사용자가 DML을 수행하면, Supplemental Logging 설정에 따라 추가 데이터가 포함된 Redo Log가 생성
2. **Archive Log 전환:** Redo Log가 가득 차면 Archive Log로 저장
3. **LogMiner / CDC Extract:** CDC 툴(예: Oracle GoldenGate, Debezium)이 LogMiner 인터페이스를 통해 이 로그들을 분석하여 변경 사항을 추출


## 5. MySQL과의 주요 차이점

| 특징 | MySQL (Binlog) | Oracle (Supplemental Logging) |
| --- | --- | --- |
| **설정 단위** | 서버/세션 단위 중심 | **데이터베이스/테이블 단위 세분화** |
| **기록 방식** | 행 데이터 전체(ROW format) | 변경 데이터 + **지정한 추가 컬럼** |
| **유연성** | 설정 시 모든 테이블 적용 | **필요한 테이블만 골라서 설정 가능** |


## 6. 주의사항
- **부하 고려:** `ALL COLUMNS` 로깅은 데이터베이스 성능과 디스크 공간에 부담을 줄 수 있다.
- **로그 보관:** CDC 툴이 로그를 읽기 전에 Archive Log가 지워지지 않도록 충분한 Retention을 확보하자.
