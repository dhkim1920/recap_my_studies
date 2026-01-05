# MySQL CDC: Binary Log (Binlog)

## 1. 개요
**Binary Log**는 데이터베이스의 변경 사항(데이터 수정, 테이블 생성 등)에 대한 정보를 포함하는 일련의 로그 파일이다. CDC 도구는 이 로그를 읽어 타겟 시스템으로 데이터를 실시간 전송한다.

## 2. 필수 설정 요소
CDC 운영을 위해서는 `my.cnf` 또는 `my.ini` 설정 파일에서 아래 설정이 되어있어야 한다.

### 2.1 binlog_format = ROW
- **설명:** 로그 기록 방식을 결정
- **왜 ROW인가?**: `STATEMENT` 방식은 실행된 SQL 문만 기록하므로, `UUID()`나 `NOW()` 같은 비결정적 함수가 포함될 경우 소스와 타겟의 데이터가 달라질 수 있다.
- `ROW` 방식은 실제 변경된 **Row의 데이터 자체**를 기록하므로 데이터 무결성을 보장하며, CDC 툴이 변경 전/후 값을 정확히 파악할 수 있게 한다.

### 2.2 server_id
- **설명:** 복제 토폴로지 내에서 서버를 식별하는 고유 ID
- **주의:** CDC 툴(예: Debezium)은 스스로를 하나의 'Replica'로 등록하므로, 소스 DB와 겹치지 않는 고유한 ID를 가져야함

## 3. 작동 방식
Binary Log는 다음과 같은 이벤트를 기록합니다.

1. **DML (Data Manipulation Language):** `INSERT`, `UPDATE`, `DELETE`를 통한 행 변경 사항
2. **DDL (Data Definition Language):** `CREATE`, `ALTER`, `DROP` 등 스키마 구조 변경 사항
3. **트랜잭션 커밋:** 각 트랜잭션이 완료되는 시점에 로그에 기록되어 데이터 일관성을 유지

## 4. 운영 시 주의사항

### 4.1 로그 보존 기간 설정
CDC 툴이 일시적인 장애로 멈췄을 때, 그동안 쌓인 로그가 삭제되면 데이터를 복구할 수 없다.

- **설정값:** `binlog_expire_logs_seconds`
- **권장:** 비즈니스 요구사항에 따라 다르지만, 보통 **3일~7일(259200~604800초)** 정도의 보관 기간을 권장

### 4.2 binlog_row_image
- **Full (기본값):** 변경된 행의 모든 컬럼을 기록
* **Minimal:** 실제 변경된 컬럼만 기록, 로그 용량은 줄어들지만, CDC 툴에 따라 전체 정보가 필요할 경우가 있어서 적절하게 사용하는게 중요

## 5. 관련 주요 명령어

```sql
-- 현재 binlog 설정 확인
SHOW VARIABLES LIKE 'binlog_format';
SHOW VARIABLES LIKE 'log_bin';

-- 현재 기록 중인 binlog 파일 목록 확인
SHOW BINARY LOGS;

-- 특정 binlog 파일의 내용 이벤트 확인
SHOW BINLOG EVENTS IN 'mysql-bin.000001' LIMIT 10;

```