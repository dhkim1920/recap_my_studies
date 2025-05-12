
# HBase Block Cache 정리

## Block Cache란?

**Block Cache**는 HBase에서 디스크(HFile)에서 읽은 블록 단위 데이터를 메모리에 저장하여, 동일한 데이터를 반복해서 읽을 때 디스크 I/O를 줄이고 읽기 성능을 향상시키는 메커니즘

---

## Block Cache의 동작 방식

1. 클라이언트가 데이터를 조회하면, RegionServer는 먼저 Block Cache에서 해당 블록이 있는지 확인 (Memstore 다음임)
2. 블록이 캐시에 있으면, 캐시에서 바로 데이터를 반환
3. 블록이 캐시에 없으면, 디스크에서 블록을 읽은 후 캐시에 저장하고 데이터를 반환

**※ Block cache의 데이터는 꼭 최신 데이터가 아니다.**

## Block Cache의 구현체

### 1. LruBlockCache
- **특징**:
  - 기본 구현체로, JVM 힙 메모리 내에서 동작
  - LRU(Least Recently Used) 알고리즘 사용
  - 세 가지 우선순위 영역: single-access, multiple-access, in-memory

- **설정**:
  - `hfile.block.cache.size` 파라미터를 통해 전체 힙 메모리 중 Block Cache에 할당할 비율을 설정
  - 기본값은 0.40 (40%)

### 2. BucketCache
- **특징**:
  - JVM 힙 외부(off-heap)에서 동작
  - 대용량 메모리를 사용할 수 있고, GC(Garbage Collection) 영향이 적음
  - 보통 LruBlockCache와 함께 사용됨
    - Bloom 필터 및 인덱스 → LruBlockCache
    - 데이터 블록 → BucketCache

> 참고) off-heap이란 JVM Heap 메모리 바깥의 운영체제 메모리를 직접 사용하는 것
---

## Block Cache 비활성화

- **사용 시점**:
  - 일회성 대량 조회 작업 등에서는 Block Cache를 사용하면 캐시 오염 가능
  - `NO_CACHE` 힌트 또는 API에서 `setCacheBlocks(false)` 사용

- **설정 방법**:
  - 컬럼 패밀리 단위로 Block Cache 사용 여부를 설정 가능 (`BLOCKCACHE = false`)

---

## 주의사항

- Block Cache는 RegionServer 단위로 관리되며, 하나의 RegionServer 내 모든 Region이 동일한 Cache를 공유함
- Block Cache는 컬럼 패밀리 단위로 활성화/비활성화 가능
