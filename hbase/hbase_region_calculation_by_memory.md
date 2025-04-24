
# HBase Region 적정 수 계산 공식

## 계산 공식

```
(regionserver_memory_size) × (memstore_fraction)
÷ ((memstore_flush_size) × (num_column_families))
```

이 공식은 **RegionServer의 메모리 자원과 MemStore 설정**을 기반으로,  
**하나의 RegionServer가 안정적으로 관리할 수 있는 Region 수**를 추정하기 위한 가이드

## 용어 설명

- **regionserver_memory_size**: RegionServer에 할당된 전체 메모리 크기 (단위: MB)  
- **memstore_fraction**: 전체 메모리 중 MemStore에 할당된 비율  
  - 설정: `hbase.regionserver.global.memstore.size` (기본값: 0.4)  
- **memstore_flush_size**: 하나의 컬럼 패밀리당 MemStore가 flush 되는 임계값  
  - 설정: `hbase.hregion.memstore.flush.size` (기본값: 128MB)  
- **num_column_families**: 테이블의 컬럼 패밀리 수  

---

## 예시 계산

설정:
- RegionServer 메모리: 16GB (16,384MB)
- MemStore 비율: 0.4
- MemStore flush 크기: 128MB
- 컬럼 패밀리 수: 1

계산:
```
(16,384 × 0.4) ÷ (128 × 1) = 51.2
```

→ **약 51개의 Region을 안정적으로 관리 가능**

---

## 주의사항

- 위 공식은 **가이드라인**일 뿐이며, 실제 적정 Region 수는 아래의 내용에 따라 잘라 질 수 있음
  - 워크로드 특성 (읽기/쓰기 비율, 크기)
  - 데이터 분포 균형
  - Compaction/Flush 빈도

- Region 수가 **과도하게 많아지면**:
  - GC 오버헤드 증가
  - Compaction 및 flush 부하 증가
  - 시스템 전반의 성능 저하

- 일반적으로 권장되는 Region 수는:
  - **RegionServer당 100~200개** 수준 (이건 서버가 엄청 많아도 사실상 힘듦)

---

## 설정 조정 팁

- `hbase.regionserver.global.memstore.size`:  
  - 쓰기 부하가 높은 경우 값을 늘려 MemStore를 더 수용 가능

- `hbase.hregion.memstore.flush.size`:  
  - 값을 높이면 Region 수가 줄어들지만, flush 주기가 길어짐

- **컬럼 패밀리 수 최소화**:  
  - 컬럼 패밀리 수가 많을수록 하나의 Region 내에 여러 MemStore가 생기며,  
    Region 수가 간접적으로 증가하므로 **불필요한 CF는 피하는 것이 바람직**
