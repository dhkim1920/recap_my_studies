# Astro CLI 설치 및 Cursor MCP 연동 가이드

이 문서는 Astro CLI를 사용하여 Airflow 프로젝트를 구축하고, Cursor 에디터의 MCP 기능을 통해 AI Agent와 Airflow를 연동하는 방법을 정리한 문서이다.
**로컬 Windows(Cursor)에서 원격 서버(Mac, Airflow 구동)** 로 접속하는 환경을 기준으로 작성

## 1. Astro CLI 설치 (macOS)
Homebrew를 사용하여 Astro CLI를 설치하자
```bash
# Astronomer 탭 추가
brew tap astronomer/tap

# Astro CLI 설치
brew install astro

# 설치 확인
astro version
```

## 2. Airflow 프로젝트 생성 및 실행
테스트용 폴더를 생성하고 Airflow 프로젝트를 초기화한다.
```bash
# 프로젝트 폴더 생성 및 이동
mkdir airflow-test && cd airflow-test

# 프로젝트 초기화
astro dev init

# Airflow 실행 (Docker 기반)
astro dev start
```

## 3. Node.js 및 Agent Skills 설정
Astronomer 에이전트의 다양한 기능을 활용하기 위해 Node.js 환경에서 스킬을 추가
```bash
# Node.js 설치
brew install node

# Astronomer 에이전트 스킬 추가
npx skills add astronomer/agents
```

### 주요 Skills 설명

설치된 에이전트는 다음과 같은 능력을 가진다.

**1. 핵심 개발 및 관리**
-   `airflow`: Airflow 운영의 기본, DAG 리스트 확인, 태스크 테스트, 상태 조회 등을 담당
-   `authoring-dags`: **(핵심)** Airflow의 Best Practice를 적용해 DAG 코드를 직접 작성
-   `debugging-dags`: 태스크 실패 시 로그를 분석하고 원인을 찾아 수정 제안
-   `testing-dags`: 복잡한 DAG의 테스트 워크플로우를 구성하고 버그를 잡음
-   `managing-astro-local-env`: 현재 사용 중인 Astro CLI 로컬 환경을 AI가 제어

**2. 데이터 분석 및 리니지**
-   `analyzing-data`: 데이터 웨어하우스에 쿼리를 수행하여 비즈니스 질문에 답함
-   `tracing-downstream/upstream-lineage`: 데이터 문제 발생 시 그 데이터의 기원과 영향 범위를 추적
-   `profiling-tables`: 특정 테이블의 데이터 분포, 결측치 등을 심층 분석

**3. 마이그레이션 및 특수 기능**
-   `migrating-airflow-2-to-3`: 구버전 코드를 Airflow 3.x 문법으로 가이드
-  `cosmos-dbt-core/fusion`: dbt 프로젝트를 Airflow DAG로 변환/통합

## 4. Python 환경 구성 및 MCP 설치
Cursor와 연동하기 위해 `astro-airflow-mcp` 패키지를 설치, **Python 3.10**이상 환경 필요

```bash
# Python 3.10 설치
brew install python@3.10

# 가상 환경 생성
python3.10 -m venv .venv

# 가상 환경 활성화
source .venv/bin/activate

# pip 업그레이드 및 MCP 패키지 설치
pip install --upgrade pip
pip install astro-airflow-mcp

```

## 5. SSH 설정 (원격 서버 연동 시)
Cursor(로컬)가 Astro(원격 서버)에 접속하기 위해 SSH 키 설정이 필요하다.
```bash
# 1. SSH 키 생성 (이미 있다면 생략, 엔터만 입력하여 기본값 사용)
ssh-keygen -t ed25519

# 2. 원격 서버(예: Mac Mini)로 키 복사
# 맥/리눅스에서 실행 시
ssh-copy-id {원격서버_계정}@{원격서버_IP}
# 윈도우 wsl에서 만들고 복사하면 편하다.
```

## 6. Cursor 연동 설정 (mcpServers)
**설정 위치**: Cursor `Settings` -> `Tools & MCP`
> Cursor가 윈도우에 설치되어 있으므로 mcpServers 세팅은 powershell 기준
```json
{
  "mcpServers": {
    "astro-agent": {
      "command": "ssh",
      "args": [
        "-T",
        "-i",
        "C:\\Users\\{유저}\\.ssh\\id_ed25519",
        "-o",
        "IdentitiesOnly=yes",
        "{원격서버_계정}@{원격서버_주소}",
        "bash",
        "-lc",
        "export AIRFLOW_URL='http://127.0.0.1:8080'; exec /Users/{유저}/.venv/bin/astro-airflow-mcp --transport stdio"
      ]
    }
  }
}
```

### 설정 옵션 설명

1.  **SSH 접속 (Windows 측 명령)**
-   `-T`: **가상 터미널 비활성화**, 사람이 아닌 프로그램 간 통신이므로 불필요한 터미널 할당을 막음
-   `-i "C:\\..."`: **인증 키 지정**, 비밀번호 입력 없이 접속하기 위해 로컬에 있는 Private Key 경로를 지정
-   `-o IdentitiesOnly=yes`: **지정된 키만 사용**, SSH 에이전트의 다른 키를 시도하지 않고 지정한 키만 사용하여 인증 오류를 방지

2.  **원격 쉘 실행 (원격 서버 측 명령)**
-   `bash`: 원격 서버에서 실행할 쉘
-   `-lc`: **로그인 쉘로 명령 실행**.
    -   `-l` (login): `.bash_profile` 등을 로드하여 환경변수(PATH 등) 사용할 수 있게 함
    -   `-c`: 뒤따르는 문자열을 명령어로 실행

3.  **MCP 실행 명령**
-   `export AIRFLOW_URL='...'`: MCP가 Airflow와 통신할 주소를 환경변수로 지정
-   `exec`: 현재 쉘 프로세스를 MCP 프로세스로 **대체**하여 메모리를 절약
-   `--transport stdio`: MCP 서버를 HTTP가 아닌 **표준 입출력(stdio)** 모드로 실행하여, SSH 터널을 통해 Cursor와 데이터를 주고받는다.