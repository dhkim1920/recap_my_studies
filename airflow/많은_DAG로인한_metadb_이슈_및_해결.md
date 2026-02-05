# 많은 Dag로 인한 metadb 이슈 및 해결

## 1. 현상 파악
- **대량의 DAG 약 3천개 :** DAG 개수도 많은데 tag의 종료도 좀 되기 때문에 메타가 비대해짐
- **스테이트 미스매치:** DB 응답이 느려지니 스케줄러가 Task 상태를 제때 업데이트 못 함, 결국 실제 실행 상태와 DB 정보가 따로 노는 장애 발생

## 2. 긴급 조치
- metadb의 이슈이므로 airflow 워커 늘리는 건 의미 없음
- **유령 세션 강제 종료:** 점유율 90% 주범인 `idle` 세션들 정리.
```sql
-- 5분 이상 응답 없는 세션 종료 (Postgres 기준)
SELECT pg_terminate_backend(pid) FROM pg_stat_activity 
WHERE state = 'idle' AND query_start < now() - interval '5 minutes';
```

## 3. 구조적 개선

공식 문서 및 글로벌 기술 블로그에서 검증된 대규모 환경 설정법

### ① PGBouncer 도입 (Transaction Mode)

- **핵심:** 커넥션 개수 늘리기보다 **PGBouncer**를 앞단에 둬서 효율적으로 풀링해야 함
- **설정 주의:** `Transaction Mode` 사용 시, SQLAlchemy 연결 스트링에 `prepared_statements=false` 파라미터 필수 (안 그러면 Prepared Statement 에러 발생)

### ② 스케줄러 파싱 쓰로틀링 (Throttling)

- **설정:** DB 쓰기 빈도를 의도적으로 낮춤
- `AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL`: 300 (5분 주기로 파싱)
- `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL`: 600 (10분 주기로 스캔)
- **효과:** 동일 DAG를 무한 반복 파싱하며 DB를 괴롭히는 현상 방지.

## 4. 고려해 봄직한 사항 들

- **동적 태그 생성 금지:** `tags=[datetime.now()]` 같은 로직은 메타 디비를 비대하게 한다.
 - 정해진 tag만 쓰게하자 enum 이라던지 static list를 제공해서 담당자가 제한을 둬야함
- **dag 개수 생성 줄이기:** 개발 편의를 위해 dag에서 dag를 호출하는 코드는 지양하고, task를 사용하여 한 dag에서 처리하는 것이 좋다.
- **너무 많은 connection 수:** PGBouncer가 없는 상태에서 너무 많은 connection을 설정할 경우 정해진 자원내에서 경합이 발생하여 느려질 수 있다.
 - 적절한 connection을 설정하거나 가급적이면 PGBouncer를 도입하는게 좋다.
 - 참고) *PostgreSQL Wiki*에서 제시하는 “최적 처리량을 위한 **active connection** 수” 시작점: `Connections ≈ (cores * 2) + effective_spindles`
   - cores는 HT 스레드 제외(물리 코어 기준)로 보며, effective\_spindles는 캐시가 충분하면 0에 수렴. SSD/NVMe 환경에서는 정확도 보장 어려움 → 부하테스트로 보정 필요.
   - 출처: `https://wiki.postgresql.org/wiki/Number_Of_Database_Connections`
   - 참고: Core: CPU 코어 수 (Thread 포함), Spindle: 디스크 드라이브 수 (보통 SSD 환경에서는 무시하거나 아주 작게 설정)

