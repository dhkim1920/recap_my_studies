# HDFS 블록 손실 시 HBase의 동작

## 1. 복제본 부분 손실

### HDFS 상태
- 블록의 일부 복제본 손실, 최소 1개 이상 복제본 존재할 때

### HBase 동작
- RegionServer는 HDFS Client를 통해 **정상 복제본 자동 선택**
- HFile 접근 가능 → Region 정상 작동
- 사용자 입장에서는 **영향 없음**
- HDFS는 백그라운드에서 **ReplicationMonitor**로 복제 자동 복구 수행

### 주의사항
- 복구가 지연되거나, 추가 손실 발생 시 → 전체 손실로 전환될 수 있음

---

## 2. 전체 손실

### HDFS 상태
- 블록의 **모든 복제본 소실** 또는 심각한 손상

### HBase 동작
- RegionServer는 HFile 접근 시 `BlockMissingException`, `IOException` 발생
- 해당 Region의 Get/Scan 등 **RPC 요청 실패**
- RegionServer는 해당 Region을 **비정상/폐기 상태로 전환**
- HMaster는 이를 감지하고 **다른 RegionServer로 재할당 시도**, 하지만 HFile 자체가 없기 때문에 실패한다.
- **결과적으로 Region은 복구 불가**

### 후속 조치 - 수동 복구 필요
- `hbck2`로 meta 수정
- secondary cluster가 있다면 복제(peer-to-peer replication)에서 복원한다.
- 백업 또는 외부 저장소에서 수동 복원
- WAL로 복원해도되자나?
  - WAL도 HDFS에 저장된다. WAL가 저장된 Datanode가 문제없다면 괜찮겠지만 이것도 전체 손실이라면 WAL를 통한 복원도 불가능하다. 

---

## 요약 비교

| 구분 | 복제본 일부 손실 | 복제본 전부 손실 |
|------|------------------|------------------|
| HFile 접근 가능 여부 | 가능 | 불가능 |
| Region 상태 | 정상 | 폐기 또는 비정상 |
| 사용자 영향 | 없음 | RPC 실패, 데이터 유실 가능 |
| 자동 복구 | HDFS가 복제 재생 | 불가능 (수동 조치 필요) |
| HMaster 재할당 | 필요 없음 | 시도하나 실패 |

---

**결론:**  
- 부분 손실은 자동 복구되며 사용자 영향도 없다.
- 전체 손실은 수동 개입 없이는 복구 불가, **백업 체계 필수**