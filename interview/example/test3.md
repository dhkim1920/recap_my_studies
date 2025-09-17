수치는 **50TB/일(≈579MB/s ≈4.63Gbps)*- 처리량을 기준으로

---

## Debezium 아키텍처 (대규모 MySQL CDC → Kafka) + 스펙

### 1. MySQL 소스 구조
- **binlog 활성화**: `ROW` 포맷, GTID 권장, `binlog_row_image=MINIMAL`
- **다중 샤딩/파티션**: 단일 인스턴스 한계 시 샤딩 고려
- **replica server 분리**: CDC는 replica에서 binlog 읽기

**권장 스펙(Replica 기준, )**

- CPU: 16–32 vCPU
- RAM: 64–128 GB
- 스토리지: NVMe SSD 4–8 TB (binlog 보존기간+버퍼 고려), RAID1/10
- 네트워크: 25 GbE 이상 (피크/리플레이 헤드룸)
- MySQL 설정: `sync_binlog=1`, `innodb_flush_log_at_trx_commit=1`, `binlog_expire_logs_seconds`는 소비 지연을 고려해 여유 설정

### 2. Debezium Connector (Kafka Connect)

- **Kafka Connect + Debezium MySQL Connector*- 다수

  - 테이블/샤드별로 분할 운영
- **병렬 처리**

  - 커넥터 인스턴스/태스크 다중화
  - Connect 클러스터 수평 확장

**권장 스펙(Connect Worker, )**

- 워커 노드: 6–12대 (처리량/테이블 분할도에 따라 가감)
- 각 노드: 8–16 vCPU, 32–64 GB RAM
- JVM Heap: 8–16 GB, GC는 G1GC
- 디스크: NVMe 500 GB+ (오프셋/디스크백업/로그), 고IOPS
- 네트워크: 25 GbE 이상
- 태스크 수: 워커/커넥터 당 4–16 태스크(스루풋/병목 보며 점증)
- 포맷/압축: Avro/Protobuf(+Schema Registry), Kafka 레벨 LZ4/Snappy

### 3. Kafka 구조

- **토픽 파티션 수 확장**: 수천 파티션 가능성, 파티션 키는 PK/샤드키
- **압축 사용**: Snappy/LZ4
- **Tiered Storage(선택)**: 장기 보관 S3 등으로 오프로드

**권장 스펙(브로커, )**

- 브로커: 9–15대(KRaft 사용 시 Controller 3–5대 별도 권장)
- 각 브로커: 16–32 vCPU, 64–128 GB RAM
- 디스크: NVMe 4–8 TB, 최소 2개 볼륨(로그/스냅 분리 가능), XFS
- 네트워크: 25–50 GbE
- 파티션 수: 소스 테이블/샤드 수 × 20\~50 범위에서 시작 후 모니터링 증설
- 리플리케이션 팩터: 3
- 배치/압축: `compression.type=producer`, `linger.ms=5–20`, `batch.size` 상향
- Tiered Storage: MSK/Redpanda/Confluent Platform 등 선택 시 오브젝트 스토리지 연계

### 4. 병목 관리

- **Snapshot 피하기**: 50TB급은 스냅샷 금지, **incremental only**
- **Throughput Scaling**: 태스크/커넥터/브로커 수평 확장
- **Schema Registry 연계**: 스키마 진화/호환성 관리

**권장 스펙(Schema Registry, )**

- 인스턴스: 3대
- 각 노드: 4–8 vCPU, 16–32 GB RAM
- 스토리지: 소규모 SSD(100–200 GB)
- 네트워크: 10–25 GbE
- 호환성: `BACKWARD` 또는 `FULL` 정책

---

## 예시 아키텍처 (텍스트)

```
   [MySQL Master] 
        │
   [MySQL Replica]  ← binlog 읽기 전용
        │  (25GbE)
 ┌─────────────────────┐
 │  Kafka Connect CL   │   (6–12 nodes, 8–16 vCPU / 32–64GB)
 │  + Debezium         │--- Connector 1 (Shard/테이블 A → Topic A, N partitions)
 │                     │--- Connector 2 (Shard/테이블 B → Topic B, N partitions)
 │                     │--- Connector 3 (Shard/테이블 C → Topic C, N partitions)
 └─────────────────────┘
        │  (25–50GbE)
     [Kafka Cluster]   (9–15 brokers, 16–32 vCPU / 64–128GB, NVMe 4–8TB)
        │
 [Schema Registry (3)] 
        │
 [Spark/Flink/DWH/DL]
```

---

## 추가 운영 권고

- **관측성**: Prometheus+Grafana, OpenTelemetry, Kafka Exporter, Connect/JMX 모니터링
- **백프레셔**: Connect `consumer.max.poll.interval.ms`, `max.poll.records` 조정, 다운스트림 처리량과 보폭 맞춤
- **신뢰성**: 토픽별 `min.insync.replicas=2`, 프로듀서 `acks=all`
- **보안**: TLS, mTLS, SASL/OAuth/OIDC, Secret 관리(KMS/HashiCorp Vault)
- **용량계획**: 50TB/일 원시 쓰기량 대비 **binlog 오버헤드**와 **메시지 포맷 압축률**을 감안해 ±30–100% 범위 시뮬레이션(리플레이/버스트 대비)
