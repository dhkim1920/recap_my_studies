
### 1) 자주 나오는 CDC 문제 유형

- **소스 RDB → Kafka → Lakehouse 업서트 파이프라인 설계**
  - Debezium/binlog로 INSERT/UPDATE/DELETE를 이벤트화→Kafka→Spark로 머지 업서트
- **Exactly-once(중복 방지)**
  - Kafka 트랜잭션(EOS), idempotent write, 체크포인트, 오프셋 관리 전략
- **초기 스냅샷 + 라이브 변경 병행**
  - 부트스트랩 스냅샷 후 binlog LSN/GTID 이어받기(스냅샷 장시간, 락 이슈 대응)
- **순서, 지연, 역행 이벤트 처리**
  - 이벤트 타임, 워터마크, 버전/LSN 기반 최종상태 결정
- **DELETE/소프트딜리트/하드딜리트**
  - 테이블 정책에 맞춘 물리 삭제 vs `is_deleted` 플래그
- **스키마 변화(DDL), 진화**
  - Delta/Iceberg/Hudi의 MERGE & 스키마 진화 활용

> 참고) MySQL 관련 <br>
> binlog <br>
> MySQL 서버에서 발생한 데이터 변경 이벤트(INSERT, UPDATE, DELETE, DDL 등)를 이진 형식으로 기록해두는 로그 파일
>
> LSN (Log Sequence Number)
> - 로그 파일(binlog/WAL) 내 **물리적 위치(오프셋)**  
> - CDC 재시작 시 **어디까지 읽었는지** 추적 <br>
> 
> GTID (Global Transaction ID) 
> - 트랜잭션별 **전역 고유 ID** (`server_uuid:txn_no`)  
> - 복제/CDC 시 **트랜잭션 단위 이어받기, 중복 방지** 용도

---

### 2) 구조

```
[RDB] → [Debezium(옵로그/바이널로그)] → [Kafka topics(partition by pk)]
→ [Spark Structured Streaming: dedup + upsert(merge)] 
→ [Lakehouse(Iceberg): 서빙 테이블] → [BI/모델/마트]
메타: checkpoint/offset, schema registry, DLQ, 모니터링
```

- **키 설계**: `pk`(+`op_ts`/`lsn`)로 자연키 보장, 멱등 업서트
  - pk (Primary Key)
    - CDC 이벤트는 한 행의 변경을 나타내므로, 같은 행을 식별하려면 기본키가 필요 
    - Kafka 파티션을 pk로 나누면 같은 키의 이벤트 순서를 보장받을 수 있음
  - op_ts (operation timestamp)
    - 이벤트가 실제 DB에서 발생한 시각 또는 binlog에 기록된 시점 
    - 지연된 이벤트나 순서가 뒤섞인 이벤트가 들어와도 op_ts 비교로 최종 상태를 보장 가능 
  - lsn (log sequence number, 또는 GTID)
    - DB 트랜잭션 로그의 오프셋, 같은 op_ts라도 트랜잭션 순서를 명확히 하기 위해 사용 
    - CDC 재처리나 백필 시 특정 시점부터 정확히 이어받을 수 있게 한다.
  - 따라서 멱등성이 보장된다.
- **업서트 방식**
  - Iceberg: `MERGE INTO`(Spark 3)로 파일 단위 리라이트
- **정합성**: Kafka EOS(+ 트랜잭션) 또는 at-least-once + idempotent MERGE
- **재처리**: 특정 오프셋 구간 백필 DAG, 동일 MERGE 경로로 재적재

> 참고)
> 
> 멱등성 (Idempotency): 같은 작업을 여러 번 수행해도 결과가 한 번 수행한 것과 동일하게 유지되는 성질
> 
> 정합성 (Consistency): 시스템에 저장된 데이터가 제약조건·규칙에 맞게 항상 일관된 상태를 유지하는 것
---

### 3) 샘플 MERGE 스니펫

- **Iceberg (Spark SQL)**

```sql
MERGE INTO tgt t USING src s
ON t.pk = s.pk
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

---

### 4) 체크리스트
- **순서보장, 중복제거**: `pk + lsn/op_ts`로 최신 승자 결정, 멱등 MERGE
- **Exactly-once**: Kafka 트랜잭션/EOS + 체크포인트/오프셋 관리
- **스냅샷→스트림 전환**: 스냅샷 완료 커트오프 LSN 이후부터 스트림 연결
- **스키마 진화**: ADD COLUMN·NULL 허용, 다운스트림 스키마 호환
- **Lakehouse 선택**
  - Delta: 운영성 좋은 MERGE
  - Iceberg: 개방형·엔진 다양
  - Hudi: MOR로 고속 ingest

---

### 5) 빠른 연습 문제 2개

1. **주문/주문상품 2테이블 CDC 조인 업서트**
   - 문제: `orders(pk=order_id)`와 `order_items(pk=order_id,item_no)` 동시 변경
   - 요구: 상위/하위 이벤트 도착 순서 뒤섞임, 중복, 지연 처리
   - 핵심: 토픽 분리 + 키 설계, 조인 타임아웃, late event 보정, MERGE 2단계

2. **DELETE/상태역행 처리**
   - 문제: `DELIVERED` 후 과거 `UPDATE` 도착
   - 핵심: `op_ts/lsn` 최신 승자룰, 하드/소프트 삭제 정책, 감사 테이블 분리

