
# Spark 셔플 튜닝 가이드 (SQL/Scala 공통)

## 1) 핵심 원리
- 셔플은 **네트워크·디스크 IO 집중 구간**으로, 파티션 수/파일 수/압축/메모리·네트워크 버퍼가 병목을 좌우한다.
- Spark 3.x는 **Adaptive Query Execution(AQE)**로 런타임에 파티션을 **병합/분할**하고, 스큐 키를 **동적 분할**할 수 있다.

## 2) 기본 설정
```bash
# 필수
spark.sql.adaptive.enabled=true
spark.sql.shuffle.partitions=200            # 기본값. 데이터/클러스터에 맞춰 조정
spark.shuffle.compress=true
spark.shuffle.spill.compress=true
spark.reducer.maxSizeInFlight=48m           # 셔플 블록 페치 버퍼
spark.shuffle.file.buffer=32k               # 셔플 파일 write 버퍼
```

## 3) 데이터 규모별 파티션 가이드
- **소규모(≤10GB)**: `spark.sql.shuffle.partitions ≈ 50–200`
- **중간(10–200GB)**: `200–1000`
- **대규모(≥200GB~TB)**: `1000–5000+` (클러스터 코어 수·네트워크 대역 고려)
- 목표: **태스크당 입력 128–512MB** 수준으로 맞추기(스캔·셔플 모두)

## 4) AQE 세부 옵션
```bash
spark.sql.adaptive.coalescePartitions.enabled=true        # 작은 파티션 병합
spark.sql.adaptive.coalescePartitions.initialPartitionNum=
spark.sql.adaptive.coalescePartitions.minPartitionNum=
spark.sql.adaptive.skewJoin.enabled=true                  # 스키유 조인 자동 분할
spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes=256m
spark.sql.adaptive.skewJoin.skewedPartitionFactor=5
spark.sql.adaptive.localShuffleReader.enabled=true        # 로컬 리더로 네트워크 이동 최소화
spark.sql.adaptive.fetchShuffleBlocksInBatch=true
```

## 5) 스큐(키 쏠림) 대응
- **자동(AQE)**: skew join 활성화
- **수동**:
  - **Salting**: `concat(lit(rand_salt), key)` → reduce 후 원키로 재집계
  - **Partial agg**: map-side에서 `reduceByKey`/`map-side combine` 활용
  - **Range partitioning**: 정렬 키 분포를 기반으로 커스텀 파티셔너 적용
  - **대형 키 분리**: 상위 N개 헤비 키를 별도 경로로 처리 후 union

## 6) 조인 전략
- **Broadcast Hash Join(BHJ)**: 한쪽이 **broadcast 가능 크기**(기본 ~10MB, 조정 가능)일 때 최우선
  ```bash
  spark.sql.autoBroadcastJoinThreshold=256m
  ```
- **Shuffle Hash/Sort Merge Join(SMJ)**: 대용량 양측 조인. 정렬/셔플 비용 큼 → **필터·프루닝** 우선
- **조인 순서**: 작은 테이블부터 누적 조인, **카디널리티 폭증** 방지

## 7) 파일·포맷·압축
- **포맷**: Parquet/ORC + **Predicate pushdown** 활성. 필요한 컬럼만 읽기
- **파일 크기**: 출력 시 **128–512MB** 타겟으로 `coalesce`/`repartition` 조정
- **압축**: `spark.sql.parquet.compression.codec=zstd`(또는 snappy)  
  - CPU 여유가 있으면 zstd 권장, 네트워크·디스크 절감

## 8) 메모리·GC·spill
- `spark.memory.fraction`(기본 0.6), `spark.memory.storageFraction`(기본 0.5 of fraction)  
- 셔플 spill이 잦으면 **executor memory** 올리거나 혹은 파티션 수를 증가 시킨다. 이렇게하면 파티션 당 요구하는 메모리가 낮아진다.
- **GC**: G1GC/ZGC에서 대용량 객체·spill 파일 수 증가 시 stop-the-world 최소화

## 9) 네트워크·디스크
- **In-flight fetch**: `spark.reducer.maxSizeInFlight` 48m → 96m 증대 시 RTT 감소 가능(네트워크 여유 필요)
- **동시 페치**: `spark.reducer.maxReqsInFlight` 증가로 병렬성 증가 (과도하면 브로커/디스크 압박)
- **디스크**: 로컬 SSD, 충분한 IOPS/throughput. `spark.local.dir` RAID0/NVMe 권장

## 10) 실전 튜닝 절차(순차)
1. **프로파일링**: Stage DAG, 셔플 읽기/쓰기 바이트, spill, task time P95/P99 확인
2. **AQE 활성화** 후 기본값으로 1차 실행
3. **파티션 수 조정**: 태스크 입력 128–512MB로 수렴하도록 up/down
4. **스큐 탐지**: 특정 리듀서 장시간 실행/대용량 블록 → AQE 스키유 옵션↑ 또는 수동 salting
5. **조인 전략 변경**: broadcast 가능 여부 재평가, 필터·프루닝 강화
6. **네트워크·버퍼 확대**: `maxSizeInFlight`, fetch in batch, local shuffle reader
7. **파일 크기 정규화**: 출력 파일 수·크기 표준화, downstream 성능 안정
