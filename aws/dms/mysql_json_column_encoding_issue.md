# MySQL JSON Column Issue

## 1. 현상 정의
- **증상:** DMS에서 MySQL Endpoint를 사용할 때, **JSON 컬럼** 데이터가 `?`로 변환되어 적재되는 현상 발생
- **참고:** [AWS DMS Troubleshooting Guide - MySQL Character Replacement](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Troubleshooting.html#CHAP_Troubleshooting.MySQL.CharacterReplacement)

## 2. 발생 원인
- **메타데이터 설정과 실제 데이터 인코딩의 불일치**
  - 공식 문서에 따르면, MySQL 테이블의 메타데이터와 실제 저장된 데이터의 인코딩이 일치하지 않는 경우 발생한다고 한다.

### 의문점: DMS가 자동으로 대상 DB를 통해 판단하는게 아닌가??
- DMS는 별도의 매핑 설정이 없을 경우, 기본적으로 소스 DB의 메타데이터를 참조하여 문자셋을 결정한다고 한다. (이것도 공식문서에 명확히 나온 것은 아님)
- 이론적으로는 문제가 없어야 하나, 실제로는 데이터에 `?`가 들어가는 현상이 발생한다.
- DMS 내부 로직이 구체적으로 공개되지는 않았으나, **JSON 타입 처리 시 메타데이터만으로는 올바른 인코딩 변환을 수행하지 못하는 내부 이슈**가 있는 것으로 추정된다.

## 3. 해결 방법
- DMS의 자동 판단에 맡기지 않고, 문자셋 매핑 규칙을 강제로 지정하여 해결한다.
- **적용 방법** 
  - DMS Console > Endpoints > Source Endpoint 선택 > **추가 연결 속성 (Extra Connection Attributes)**
  - 아래 내용을 추가 및 저장
    ```text
    CharsetMapping=utf8,65001;
    ```
    *(참고: UTF-8(Code Page 65001)로 해석하도록 강제함)*