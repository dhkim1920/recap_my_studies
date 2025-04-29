# HBase Region Split 중 Meta Table 업데이트 실패 하면 어떻게 될까?

### Region Split은 어떻게 되나?
  - hfile이 설정한 크기를 넘어서면 hbase에서 자동으로 hfile을 나누게된다. 이때`hbase:meta` 테이블에 새로 만들어진 두 개 Region의 정보(시작 키, 끝 키, 위치 등)가 등록된다.

### 이때 Meta Table 업데이트 실패한다면?
  - Split이 "완료되지 않은 상태"로 남는다. 즉 Region은 "split in-progress" 상태가 됨
  
### 어떻게 되나 그럼?
- Master나 다른 Region Server가 해당 Region을 정확히 인식하지 못할 수 있다.

### 장애 리스크
- Region이 오프라인 상태로 변경될 수 있다.
- 클라이언트 요청 실패 (예: `RegionUnavailableException` 등등)
- 물리적으로 meta가 깨지면 심각한 경우 해당 Table 조회 자체가 안된다!

## 복구해 보자!
### 1. 상태 점검
- HMaster Web UI (기본 포트 16010) 접속.
- "In Transition" 상태에 걸린 Region 확인해보자
  - SPLITTING, SPLIT, FAILED_OPEN, OFFLINE 같은 상태 여부 확인

### 2. 로그 확인
- HMaster 및 문제 발생한 Region Server 로그 확인해본다.
- 에러 내용 확인, Region Split 도중 실패했는지 파악한다.

### 3. hbck2 도구 사용 (HBase 2.x 기준)
> ※ 주의 잘못하면 meta 테이블이 더 망가 질수 있다.

> ※ 보통 HBase는 부팅할 때 hbase:meta 테이블을 기반으로 전체 Region 상태를 다시 로딩하기 때문에
> Region 할당하므로 일단 전체 재시작 부터 하자!

#### hbck2 명령어
※ 그래도 hbck2는 프로시저 등록해서 master가 실행하니 좀 안전하다.

※ hbck는 HBase 자체를 바꿔버리기 때문에 아주 위험하다!!
```bash
hbck2 fixMeta # 메타 테이블과 실제 Region 상태 불일치 자동 수정
hbck2 assign <region-name> # Region을 강제로 할당하거나 해제
hbck2 bypass <proc-id> -f # stuck된 상태 무시하고 강제 처리
```

### 4. Region 재배치 (필요 시)
```bash
echo "disable 'table_name'" | hbase shell
echo "enable 'table_name'" | hbase shell
```
- 테이블을 disable 후 다시 활성화enable하여 재정렬

### 5. 최악의 경우: 수동 Meta 수정
- `hbase:meta` 직접 수정 가능 (매우 위험!!!!!)
- HBase Shell이나 내부 API 이용
- 수정 전 **전체 백업 필수**
- 이건 진짜 최악의 수니까 하지 말자

### 주의사항
- Meta Table 복구 작업은 매우 민감하다.
- 복구 전에 반드시 HBase 전체 메타데이터 백업은 필수, 잘못 수정 시 테이블 전체가 열리지 않는 심각한 장애 발생 가능

