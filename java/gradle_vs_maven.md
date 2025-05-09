# Gradle vs Maven 비교 정리

Java 프로젝트에서 널리 사용되는 두 가지 빌드 도구: **Gradle**과 **Maven**에 대한 비교 및 개요

---

## Gradle vs Maven 비교표

| 항목              | Gradle                                              | Maven                                                  |
|-------------------|------------------------------------------------------|---------------------------------------------------------|
| 설정 방식         | Groovy/Kotlin 기반 DSL (스크립트형)                | XML 기반 선언적 설정 (pom.xml)                         |
| 유연성            | 높음 (사용자 정의 및 확장 용이)                    | 낮음 (표준화된 구조, 제한된 유연성)                   |
| 빌드 성능         | 빠름 (증분 빌드, 캐시, 병렬 처리 지원)             | 느림 (전체 재빌드, 병렬 처리 제한적)                  |
| 학습 곡선         | 상대적으로 가파름                                   | 완만함                                                  |
| 플러그인 생태계   | 다양하고 확장 가능                                  | 안정적이고 표준화된 플러그인 제공                      |
| 멀티모듈 지원     | 강력한 지원 (대규모 프로젝트에 적합)               | 있음 (복잡한 설정 필요)                                |
| 적합한 프로젝트   | Android, 복잡한 빌드 로직                          | 표준 Java 프로젝트, 안정성이 중요한 환경              |

## 선택 기준 요약

- **Gradle**: 빌드 속도, 유연성 중요 / Android 개발
- **Maven**: 안정성, 표준 구조 중시 / 팀 협업 용이

---

## Maven 정리

### 1. Maven이란?
- 자바 기반 **프로젝트 관리 및 빌드 도구**
- 의존성 관리, 빌드, 테스트, 배포 자동화

### 2. 핵심 개념

| 개념         | 설명 |
|--------------|------|
| POM          | `pom.xml`: 프로젝트 구조, 의존성, 플러그인 정의 |
| GAV 좌표     | `groupId:artifactId:version`으로 의존성 식별 |
| 라이프사이클 | compile, test, package, install, deploy 단계 |
| 리포지토리   | 중앙/사설 저장소에서 JAR 다운로드 |
| 플러그인     | Maven 동작 정의 도구 (예: maven-compiler-plugin) |

### 3. 기본 구조 예시 (pom.xml)
```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>demo</artifactId>
  <version>1.0.0</version>
  <dependencies>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>5.3.20</version>
    </dependency>
  </dependencies>
</project>
```

### 4. 주요 명령어

| 명령어        | 설명                         |
|---------------|------------------------------|
| `mvn compile` | 소스 컴파일                  |
| `mvn test`    | 테스트 실행                  |
| `mvn package` | JAR/WAR 생성                 |
| `mvn install` | 로컬 저장소에 설치           |
| `mvn clean`   | target 디렉토리 삭제          |

---

## Gradle 정리

### 1. Gradle이란?
- Groovy 또는 Kotlin DSL 기반 **빌드 자동화 도구**
- Java, Spring, Android 등 **다양한 언어 지원**
- 빠른 빌드 속도 + 높은 유연성

### 2. 핵심 개념

| 개념            | 설명                                           |
|-----------------|------------------------------------------------|
| `build.gradle`  | 빌드 설정, 의존성, 태스크 정의 스크립트       |
| Task            | 빌드 단위 동작 (compile, test 등)             |
| Plugin          | 빌드 구성 모듈 (`java`, `application` 등)     |
| Dependency      | 의존성 선언 (`implementation` 등)             |
| Gradle Wrapper  | 프로젝트 내 버전 고정 실행기 (`./gradlew`)     |

### 3. 기본 구조 예시 (Groovy DSL)
```groovy
plugins {
    id 'java'
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework:spring-core:5.3.20'
    testImplementation 'junit:junit:4.13.2'
}
```

### 4. 주요 명령어

| 명령어                  | 설명                           |
|--------------------------|--------------------------------|
| `./gradlew build`        | 전체 빌드 수행                  |
| `./gradlew clean`        | 빌드 결과 삭제                  |
| `./gradlew test`         | 테스트 실행                     |
| `./gradlew tasks`        | 사용 가능한 태스크 목록 확인   |
| `./gradlew dependencies` | 의존성 트리 확인                |