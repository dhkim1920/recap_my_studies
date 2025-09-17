# CDC (Change Data Capture)

## 정의

CDC(Change Data Capture)는 데이터베이스나 시스템에서 발생하는 
변경 사항(Insert, Update, Delete)을 실시간 또는 근실시간으로 캡처하여 다른 시스템에 전달하는 기술

## 주요 특징

1.  **변경만 추적**: 전체 데이터를 복제하지 않고 변경된 부분만 추적하여 전달한다.
2.  **실시간성**: 이벤트 기반으로 동작하여 데이터 동기화가 빠르다.
3.  **데이터 파이프라인 핵심**: 소스 DB → 분석/저장 시스템 간 동기화를 위해 활용된다.

## 구현 방식
- -*로그 기반(Log-based CDC)**: DB 트랜잭션 로그(binlog, WAL 등)를 읽어 변경 사항을 추출한다.
- -*트리거 기반(Trigger-based CDC)**: DB 트리거를 이용해 변경 이벤트를 별도 테이블이나 큐에 기록한다.
- -*쿼리 기반(Query-based CDC)**: `updated_at` 컬럼 등으로 주기적으로 변경을 감지한다.

## 활용 사례
-   실시간 ETL 파이프라인
-   데이터 웨어하우스/레이크 최신화
-   마이크로서비스 간 데이터 동기화
-   Kafka Connect, Debezium 같은 CDC 도구 활용

## 주요 CDC 구현 도구

1. **Debezium**
 - Kafka Connect 기반의 오픈소스 CDC 프레임워크
 - MySQL binlog, PostgreSQL WAL, Oracle redo log 등 다양한 DB 로그를 읽어 이벤트로 변환
 - Kafka, Pulsar 같은 메시지 브로커로 이벤트를 전달 가능
 - 실시간 ETL/ELT 파이프라인에 많이 활용

2. **GoldenGate (Oracle)**
 - 오라클에서 제공하는 상용 CDC 솔루션
 - 이기종 DB 간 실시간 복제/동기화 지원
 - 대규모 금융, 통신사 환경에서 많이 사용됨

3. **AWS DMS (Database Migration Service)**
 - 클라우드 매니지드 CDC 서비스
 - 소스 DB → 타겟 DB, S3, Kinesis, Redshift 등 동기화 가능
 - 로그 기반 CDC 지원

4. **Flink CDC**
 - Apache Flink에 통합된 CDC 커넥터
 - Debezium처럼 DB 로그를 읽어 스트리밍 파이프라인에 직접 연결
 - Flink SQL로 바로 처리 가능

## 정리
* 오픈소스 커뮤니티 → **Debezium**
* 상용 엔터프라이즈 → **Oracle GoldenGate, IBM InfoSphere, HVR**
* 클라우드 매니지드 → **AWS DMS, Azure Data Factory, GCP Datastream**
