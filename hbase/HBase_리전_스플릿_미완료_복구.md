# HBase Region Split 및 비정상 종료 시 복구 절차

## 리전 분할(Region Split) 개요

HBase에서 Region Split은 하나의 Region이 너무 커졌을 때 자동으로 두 개로 분할하는 것을 말한다.

### Split 진행 순서

1. **Split 준비**: 메모리 및 스토리지 상태 확인 → split point 결정
2. **Daughter Region 생성**: 자식 Region 디렉터리 생성 (`/hbase/table/region_a`, `region_b`)
3. **Split 상태 파일 생성**: `.splitting`, `.splita` 등 상태 파일을 HDFS에 기록하여 "분할 중" 표시
4. **WAL 리플레이 및 데이터 이동**: WAL을 기반으로 자식 Region에 데이터 복원
5. **Parent Region 오프라인 처리 및 메타데이터 갱신**
6. **.splitting 파일 삭제**: 정상 종료 시 자동 삭제됨

---

## 문제 상황: 비정상 종료로 인한 split-in-progress

- RegionServer가 split 도중 비정상 종료됨
- `.splitting` 파일이 남아 있고 Master는 여전히 해당 Region을 "분할 중"으로 인식
- 자식 Region도 완전하지 않음 → 메타데이터 정합성 문제 발생

---

## 대응 방법

### 1. HDFS 확인

- 해당 Region의 경로에서 `.splitting`, `.splita`, `.splitb` 등의 상태 파일 존재 여부 확인

### 2. WAL 로그 검토

- `/hbase/WALs/server/xxxx.log` 내 split 관련 엔트리 검토
- 분할이 완료되지 않은 경우, WAL replay가 필요

### 3. 수동 복구 절차

1. `.splitting` 상태 파일 직접 삭제
2. `hbck2` 또는 `hbase shell`을 사용해 Region 재할당 수행  
   - 예: `assign`, `offline`, `delete` 등 명령 사용

---

## 요약된 대응 절차

1. HDFS에서 Region 디렉터리 확인
2. `.splitting` 상태 파일 존재 여부 확인
3. WAL 로그에서 해당 Region의 상태 확인
4. 완료되지 않은 split 작업에 대해 판단 후 수동 조치
5. `.splitting` 파일 삭제
6. `hbck2` 또는 shell 명령으로 Region 재할당 시도

---

## 결론
- 이 문제는 **RegionServer failover 도중 분할이 완료되지 않아 발생한 split-in-progress 상태**로 인해 발생한다.
- `.splitting` 상태 파일이 정상 삭제되지 않은 경우, 메타 정합성 이슈로 이어질 수 있으며, **WAL 확인과 수동 조치를 통해 Region 복구가 필요하다.**
- 수동으로 assign 하는건 생각보다 쉽지 않으므로 failover 때 발생하는 건 어쩔수 없지만, scale in 할때 region server 제거 시 천천히 하자! 
