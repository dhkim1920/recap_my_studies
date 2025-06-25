
# HBase RegionServer Compaction 시 성능은 어떻게 될까?
- 여기서는 Compaction이 발생했을 때 읽기와 쓰기의 성능을 알아본다.
- 또한 Compaction 전, 중, 후 어떻게 성능이 변화하는지도 알아보자

---

## 1. Read 성능

### Compaction 전
- 데이터가 여러 HFile에 흩어져 있다.
- 조회할 때 여러 파일을 찾아야 하므로 **읽기 비용 증가, 지연이 커진**다.

### Compaction 중
- 디스크를 많이 읽고/쓰므로 **읽기 요청 처리에 사용 가능한 I/O가 감소**
- **읽기 성능 일시적 저하**

### Compaction 후
- HFile 수가 줄어듦 조회할 파일 수가 줄어 **읽기 성능 장기적으로 향상**

---

## 2. Write 성능
- 쓰기는 Flush가 발생하면 Memstore의 데이터가 HFile로 생성된다. 

### Compaction 중
- 새 HFile을 만들면서 대량 디스크 쓰기 발생**디스크 사용으로 Flush, WAL Sync 속도 느려질 수 있다.**

### Compaction 후
- 디스크 정리 완료 및 쓰기 공간 확보 **Flush/Sync 성능 정상화**

---

# 요약

| 구분 | Compaction 중 | Compaction 후 |
|:---|:---|:---|
| Read(읽기) | 성능 저하 (I/O 충돌) | 성능 향상 (HFile 수 감소) |
| Write(쓰기) | 성능 저하 (디스크 대역폭 소모) | 정상화 |
