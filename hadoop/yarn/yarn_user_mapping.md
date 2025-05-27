# Spark on YARN 제출 시 사용자 매핑 관계

## 1. YARN 사용자 (Application Owner)
- `spark-submit`을 실행한 **리눅스 사용자 계정**이 YARN에서의 application owner로 인식된다.
- YARN ResourceManager UI의 `User` 필드에 해당 계정명을 확인 할 수 있따.
- 즉, YARN은 리눅스 계정 기반으로 동작

## 2. HDFS 사용자 (권한 판별 기준)
- HDFS는 Hadoop Filesystem API 호출 시점의 **사용자 이름**을 기준으로 권한 판단한다.
- Spark application 내부에서 HDFS 접근 시, 현재 실행 중인 리눅스 사용자 이름이 Hadoop의 `UserGroupInformation`(UGI)에 등록되어 사용된다.

> 따라서 YARN과 HDFS 모두 리눅스 계정을 기반으로 동일하게 작동

### 참고
- Hadoop(HDFS 포함)은 기본적으로 리눅스 계정을 인증 없이 신뢰 (`Simple Authentication`)
- 내부적으로 `whoami` 값을 UGI 로그인 사용자로 사용한다.

---

## 예외 사항

### 1. Kerberos가 활성화된 경우
- UGI는 Kerberos principal에서 사용자 정보를 받아 동작
- 리눅스 계정과 다를 수 있다.

### 2. --proxy-user 사용 시
- 리눅스 계정은 `bob`, 실제 실행은 `alice`로 impersonation 가능
- 단, `core-site.xml` 설정 필요
  ```xml
  <property>
    <name>hadoop.proxyuser.yarn.groups</name>
    <value>*</value>
  </property>
  <property>
    <name>hadoop.proxyuser.yarn.hosts</name>
    <value>*</value>
  </property>
  ```

### 3. YARN 데몬의 슈퍼유저
- 일반적으로 `yarn` 리눅스 계정이 슈퍼 유저이다.
- Container 실행, 로그 저장, 디렉터리 생성 등의 권한을 가진다.

---

## 결론
- YARN, HDFS 모두 리눅스 사용자 계정을 기준으로 사용자 권한을 판단한다.
- HDFS는 별도의 Hadoop 계정 개념 없이 OS 사용자명을 기준으로 접근 권한을 적용한다.
