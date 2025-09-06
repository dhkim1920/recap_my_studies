
## fsimage와 editlog

HDFS에서 **fsimage**와 **editlog**는 NameNode가 파일 시스템의 메타데이터를 관리하기 위해 사용하는 핵심적인 데이터 구조이다.

### fsimage란? (Filesystem Image)
**fsimage**는 특정 시점의 파일 시스템 메타데이터 전체에 대한 **snapshot**이다.
즉, 파일과 디렉터리의 모든 정보(예: 파일명, 복제 수, 생성 시간, 권한 등)를 담고 있는 파일이다.
- **역할**: HDFS가 시작될 때 Namenode는 이 fsimage 파일을 메모리에 로드하여 파일 시스템의 상태를 빠르게 복원한다.

### editlog란?
**editlog**는 fsimage가 생성된 이후 파일 시스템에 발생한 **모든 변경 사항에 대한 기록**이다.
파일 생성, 삭제, 이름 변경 등 메타데이터에 변화가 생길 때마다 해당 내용이 transaction 형태로 editlog에 순차적으로 기록된다.
- **역할**: 네임노드에 장애가 발생했을 경우, 가장 최신 fsimage를 로드한 뒤 editlog에 기록된 변경 사항들을 순서대로 적용하여 파일 시스템의 최종 상태를 복구한다.

### 저장 경로(설정 키)

- **fsimage (각 NameNode 로컬)**: `dfs.namenode.name.dir`
- **edit log (각 NameNode 로컬)**: `dfs.namenode.edits.dir`
- **shared edits(QJM, JournalNode 집합)**: `dfs.namenode.shared.edits.dir`
- **JournalNode 로컬 디렉터리**: 각 JN 호스트의 `dfs.journalnode.edits.dir` 경로에 edit 세그먼트 저장

### 기록/동기화 동작(HA, QJM 사용 시)
- **Active NameNode**
  - 클라이언트 메타데이터 변경 발생 → 로컬 `edits.dir`에 기록 + **JournalNode 다수**에 동시 커밋(Quorum)
  - fsimage는 Active가 직접 체크포인트하지 않으며, 운영 중 스냅샷 파일은 최신이 아닐 수 있음
- **Standby NameNode**
  - JournalNode의 edit log를 지속적으로 읽어(tail) 자기 네임스페이스에 적용해 Active와 상태 동기화
  - **주기적으로 체크포인트**를 수행해 새로운 fsimage를 만들고, **Active로 업로드** 하여 Active의 on-disk fsimage도 최신화한다.
- **Secondary/Checkpoint/Backup 노드**
  - **HA 클러스터에서는 필요 없음**, 따로 띄우면 **오류 구성**으로 명시

### editlog가 커질 때 발생하는 문제
- NameNode 부팅 시, `fsimage`와 `editlog` 전체를 메모리에 로드 후, editlog를 순차 적용
- editlog가 수십만 ~ 수백만 건이면 **부팅 시간 지연** 및 **복구 실패 위험**이 급격히 증가

### Checkpoint를 통한 editlog 관리
- Standby Node에서 아래를 주기적으로 실행 (Non-HA라면 **Checkpoint Node**가 주기적으로 다음을 수행)
  1. 기존 `fsimage`를 메모리에 로드
  2. `editlog`의 모든 트랜잭션을 반영
  3. 최신 `fsimage`를 생성하여 디스크에 저장
  4. editlog를 초기화(비움)
  - 이 과정을 **Checkpoint**라고 함
  - 안되는 경우?
    ```bash
    # 수동으로 먼저 확인해 본다.
    su - hdfs
    hdfs dfsadmin -safemode enter
    hdfs dfsadmin -saveNamespace
    hdfs dfsadmin -safemode leave
    ```
