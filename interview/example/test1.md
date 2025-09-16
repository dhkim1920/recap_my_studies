

### 1) 자주 나오는 CDC 문제 유형

* **소스 RDB → Kafka → Lakehouse 업서트 파이프라인 설계**: Debezium/binlog로 INSERT/UPDATE/DELETE를 이벤트화→Kafka→Spark로 머지 업서트. ([Debezium][1])
* **Exactly-once/중복 방지**: Kafka 트랜잭션(EOS)·idempotent write·체크포인트·오프셋 관리 전략. ([Apache Kafka][2])
* **초기 스냅샷 + 라이브 변경 병행**: 부트스트랩 스냅샷 후 binlog LSN/GTID 이어받기(스냅샷 장시간·락 이슈 대응). ([Debezium][3])
* **순서·지연·역행 이벤트 처리**: 이벤트 타임, 워터마크, 버전/LSN 기반 최종상태 결정. ([Apache Kafka][2])
* **DELETE/소프트딜리트/하드딜리트**: 테이블 정책에 맞춘 물리 삭제 vs `is_deleted` 플래그.
* **스키마 변화(DDL)·진화**: Delta/Iceberg/Hudi의 MERGE & 스키마 진화 활용. ([iceberg.apache.org][4])

---

### 2) 화이트보드 답안 프레임(그림으로 5분 내 그리기)

```
[RDB] → [Debezium(옵로그/바이널로그)] → [Kafka topics(partition by pk)]
→ [Spark Structured Streaming: dedup + upsert(merge)] 
→ [Lakehouse(Delta/Iceberg/Hudi): 서빙 테이블] → [BI/모델/마트]
메타: checkpoint/offset, schema registry, DLQ, 모니터링
```

* **키 설계**: `pk`(+`op_ts`/`lsn`)로 자연키 보장, 멱등 업서트. ([Debezium][1])
* **업서트 방식**:

  * Delta: `foreachBatch + MERGE INTO`로 스트리밍 업서트/중복 제거. ([docs.databricks.com][5])
  * Iceberg: `MERGE INTO`(Spark 3)로 파일 단위 리라이트. ([iceberg.apache.org][4])
  * Hudi: Copy-on-write/Merge-on-read 선택, MOR는 빠른 적재+비동기 컴팩션. ([hudi.apache.org][6])
* **정합성**: Kafka EOS(+트랜잭션) 또는 at-least-once + idempotent MERGE. ([docs.confluent.io][7])
* **재처리**: 특정 오프셋 구간 백필 DAG, 동일 MERGE 경로로 재적재.

---

### 3) 샘플 MERGE 스니펫(핵심만)

* **Delta Lake (스트리밍 foreachBatch 내부)**

```sql
MERGE INTO tgt t
USING src s
ON t.pk = s.pk
WHEN MATCHED AND s.op IN ('U','D') THEN UPDATE SET *
WHEN NOT MATCHED AND s.op='I' THEN INSERT *
```

(스트리밍에서는 `foreachBatch`에서 MERGE 사용해 중복 제거/업서트 구현) ([docs.databricks.com][5])

* **Iceberg (Spark SQL)**

```sql
MERGE INTO tgt t USING src s
ON t.pk = s.pk
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

(Iceberg는 MERGE 시 필요한 파일만 교체하는 overwrite 커밋을 사용) ([iceberg.apache.org][4])

* **Hudi**: MOR/COW 선택, Spark SQL MERGE 또는 DataFrame upsert API 구성. ([hudi.apache.org][6])

---

### 4) 체크리스트(면접에서 꼭 말할 키워드)

* **순서보장/중복제거**: `pk + lsn/op_ts`로 최신 승자 결정, 멱등 MERGE. ([Debezium][1])
* **Exactly-once**: Kafka 트랜잭션/EOS + 체크포인트/오프셋 관리. ([docs.confluent.io][7])
* **스냅샷→스트림 전환**: 스냅샷 완료 커트오프 LSN 이후부터 스트림 연결. ([Debezium][3])
* **스키마 진화**: ADD COLUMN·NULL 허용, 다운스트림 스키마 호환. ([iceberg.apache.org][4])
* **Lakehouse 선택**: Delta(운영성 좋은 MERGE), Iceberg(개방형·엔진 다양), Hudi(MOR로 고속 ingest). ([docs.databricks.com][8])

---

### 5) 빠른 연습 문제 2개

1. **주문/주문상품 2테이블 CDC 조인 업서트**

   * 문제: `orders(pk=order_id)`와 `order_items(pk=order_id,item_no)` 동시 변경.
   * 요구: 상위/하위 이벤트 도착 순서 뒤섞임, 중복, 지연 처리.
   * 핵심: 토픽 분리+키 설계, 조인 타임아웃, late event 보정, MERGE 2단계.

2. **DELETE/상태역행 처리**

   * 문제: `DELIVERED` 후 과거 `UPDATE` 도착.
   * 핵심: `op_ts/lsn` 최신 승자룰, 하드/소프트 삭제 정책, 감사 테이블 분리.

