# HDFS 파일 삭제 시 동작 원리

HDFS에서 파일을 삭제할 때 원본과 복제본이 어떻게 삭제되는지 알아보자

## 1. 파일 삭제 → 메타데이터 제거
- 사용자가 파일을 삭제하면, NameNode는 해당 파일의 **블록에 대한 참조를 메타데이터에서 제거**한다.
- 이때 삭제 대상은 파일 경로와 블록 정보이다.

## 2. 복제본 포함 블록 삭제 절차
- HDFS는 각 블록을 replication factor만큼 여러 DataNode에 저장한다.
- 삭제된 파일의 블록은 더 이상 참조되지 않으므로, **NameNode는 해당 블록을 “쓸모없음”으로 판단**한다.

#### "쓸모없음"으로 판단은 어떻게 할까?
```text
→ DataNode들은 주기적으로 Heartbeat + BlockReport를 통해 자신이 보유한 블록 목록을 NameNode에 보고
→ NameNode는 "이 블록은 이제 필요 없다"고 판단하면 해당 블록에 대해 block invalidation 명령을 내려
  각 DataNode에서 블록을 삭제하도록 지시함
```
- 이에 따라 결과적으로 **복제본이 모두 삭제**된다.

> 참고: hdfs는 원본과 복제본을 구분하지 않는다.

## 3. Trash 및 스냅샷

### Trash 사용 시
- 기본적으로 삭제된 파일은 `.Trash` 디렉토리로 **이동**되며, **NameNode 메타데이터는 유지되고**, 블록도 **DataNode에 그대로 존재**한다.
- 일정 시간이 지나 Trash가 비워지면, 그제서야 **NameNode 메타데이터 삭제 + block invalidation 발생**

> 즉, Trash는 실제 삭제가 아니라 **논리적 경로 이동**이며, 데이터는 그대로 유지

### 스냅샷 존재 시
- 삭제된 파일이 포함된 디렉토리에 스냅샷이 존재하면, **해당 파일 블록은 스냅샷이 유지되는 한 삭제되지 않음**
- 스냅샷이 삭제되어야 블록도 제거됨

## 4. 즉시 삭제: `-skipTrash` 사용

```bash
hdfs dfs -rm -skipTrash /경로/파일
```

- 이 명령어는 Trash를 거치지 않고 즉시 삭제 수행 NameNode 메타데이터도 바로 제거
→ DataNode에서도 곧바로 block invalidation 명령이 내려가 **복제본 포함 모두 삭제**

---

## 요약

| 조건             | NameNode 메타데이터 | 블록 및 복제본 |
|------------------|----------------------|-----------------|
| 일반 삭제        | 유지 (.Trash 이동)   | 유지됨          |
| Trash 비우기 후  | 제거됨               | 제거됨          |
| `-skipTrash` 사용 | 즉시 제거됨          | 즉시 제거됨     |
| 스냅샷 존재       | 유지됨               | 유지됨          |

--- 

## 관련 설정

### dfs.block.invalidate.limit

- **설명**:  
  DataNode가 NameNode와 Heartbeat를 주고받을 때, NameNode가 **"삭제해야 할 블록 목록"을 전달**한다.  
  이때 한 번에 전달 가능한 **최대 블록 수**를 이 설정으로 제한할 수 있따.
- **기본값**: `1000`  
  → 한 DataNode당 한 번의 Heartbeat에 **최대 1000개 블록 삭제 명령 전송**
- **의도**:  
  대량 파일 삭제 시 대규모 block invalidation이 발생하면 NameNode가 과부하될 수 있음 → **삭제를 분산 처리하기 위한 제한**
- 너무 크게 하면 Heartbeat 전송 지연 위험 존재
  
### dfs.namenode.invalidate.work.pct.per.iteration

- **설명**:  
  NameNode는 block invalidation 작업을 내부적으로 반복 처리한다.
  이 설정은 전체 작업 중 한 번에 처리할 **비율**을 지정한다.
- **기본값**: `0.32`  
  → 한 iteration마다 전체 블록 무효화 작업의 **32%만 처리**
- **목적**:  
  NameNode가 block invalidation 작업으로 인해 과도한 리소스를 소모하지 않도록 제어
- 빠른 삭제가 필요한 운영 환경에서는 `0.5 ~ 0.75`로 상향 가능  
- NameNode CPU 부하를 고려하여 조절 필요