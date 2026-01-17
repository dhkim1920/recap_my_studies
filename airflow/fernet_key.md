
## Fernet key

Airflow의 **Fernet Key**는 메타데이터 데이터베이스에 저장되는 **민감한 정보(Connection의 비밀번호, Variable 등)를 암호화하고 복호화하는 데 사용되는 대칭키**다. 간단히 말해, 누군가 Airflow의 DB(PostgreSQL, MySQL 등)를 직접 열어보더라도 비밀번호가 평문으로 노출되지 않도록 막아주는 방패 역할을 한다.

### 1. 주요 역할

- **비밀번호 보호:** `Connections` 메뉴에 등록한 DB 비밀번호, API 키 등을 암호화한다.
- **변수 암호화:** `Variables` 설정 시 'Val' 항목이 암호화되어 저장되도록 한다.
- **데이터 무결성:** 대칭키 방식을 사용하여 동일한 키로 암호화와 복호화를 수행한다.

### 2. Fernet Key 생성 방법

터미널에서 Python을 이용해 간단히 생성할 수 있습다. (`cryptography` 패키지 설치 필요)
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

```
위 명령어를 실행하면 `7T512UXSSmBOkpWimFHIVb8jK6lfmSAvx4mO6Arehnc=`와 같은 형태의 문자열이 출력된다.

### 3. 적용 방법
생성한 키를 Airflow 설정 파일이나 환경 변수에 등록한다.

* **방법 1: airflow.cfg 수정**
```ini
[core]
fernet_key = <생성한_키_값>
```

* **방법 2: 환경 변수 사용 (권장)**
```bash
export AIRFLOW__CORE__FERNET_KEY=<생성한_키_값>
```

> [!CAUTION]
> **주의사항:** 한 번 설정된 Fernet Key를 분실하거나 변경하면, 기존에 암호화되어 저장된 Connections와 Variables를 복호화할 수 없게 되어 오류가 발생한다.. 키를 변경해야 할 때는 구 버전 키와 신 버전 키를 함께 설정하는 프로세스를 따라야 한다.

요청하신 **Airflow Fernet Key 분실 및 사고 사례** 내용을 마크다운(Markdown) 형식으로 정리해 드립니다.

---

## Fernet Key 분실 및 사고 사례

### 사례 1: 컨테이너(Docker/K8s) 재시작 시 자동 생성
- **상황:** `airflow.cfg`나 환경 변수에 Fernet Key를 고정하지 않고 Airflow를 실행하면, entrypoint 스크립트가 실행될 때마다 **임의의 키를 새로 생성**될 수 있다.
- **문제:** 컨테이너 재시작시 키도 재생성 되므로 암호화된 값들을 쓸수 없다. 따라서 모든 DAG들도 실패

### 사례 2: 메타데이터 DB 마이그레이션 및 복구
- **상황:** 운영 환경의 DB를 덤프하여 스테이징 환경으로 옮겼으나, Fernet Key는 옮기지 않은 경우
- **문제:** 데이터는 정상적으로 이전되었으나, 스테이징 서버의 Airflow가 운영 환경의 키를 알지 못해 모든 비밀번호 필드를 읽지 못하고 `InvalidToken` 에러가 발생

### 사례 3: 관리형 서비스(Cloud Composer, MWAA 등) 설정 오류
- **상황:** GCP Cloud Composer나 AWS MWAA에서 환경 변수를 수정하던 중, 실수로 Fernet Key가 포함된 secret 참조를 누락하거나 업데이트 과정에서 레이스 컨디션으로 키가 유실되는 사례
- **문제:** UI상에서는 변수 이름이 보이지만, 실제 값을 사용하려고 하면 "Can't decrypt" 에러가 발생하며 스케줄러가 정상적으로 동작하지 않게된다.
