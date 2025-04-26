
# Java Garbage Collector

## 1. 가비지 컬렉터란?

- 사용하지 않는 객체의 메모리를 주기적으로 검사하여 청소하는 역할
- 개발자가 직접 메모리를 해제할 필요 없이 GC가 자동으로 관리
- 메모리 효율성을 높이고, 메모리 누수 방지

## 2. 가비지 컬렉터와 가비지 컬렉션 차이

- **가비지 컬렉터**: 메모리 관리 시스템 (사용되지 않는 객체를 찾아 제거)
- **가비지 컬렉션**: 가비지 컬렉터가 수행하는 프로세스 자체

## 3. JVM Heap 메모리 영역

### Young Generation

- 새로 생성된 객체가 저장
- 금방 사라지는 객체가 많음
- Minor GC 발생

### Old Generation

- Young Generation에서 살아남은 객체 저장
- 상대적으로 크며, Major GC 또는 Full GC 발생

### Permanent Generation (PermGen)

- 클래스 메타데이터 저장 (Java 7 이하)
- Java 8부터는 **Metaspace**로 대체

### Metaspace

- PermGen 대체
- Native Memory에 저장 (JVM 외부 메모리)
- 클래스 메타데이터, 리플렉션 관련 정보 저장

## 4. Reachable vs Unreachable

- **Reachable**: 유효한 참조가 있는 객체
- **Unreachable**: 참조가 끊긴 객체 (GC 대상)

## 5. Stop the World

- GC 실행을 위해 JVM 애플리케이션 실행이 일시 중지되는 현상
- GC 스레드 외 모든 스레드가 멈춤
- GC 튜닝 목표: Stop the World 시간 최소화

## 6. 가비지 컬렉션 과정

### Minor GC

- Eden 영역이 꽉 차면 발생
- 살아남은 객체를 Survivor 영역으로 이동
- Survivor 영역은 2개가 존재 (교대로 사용)

### Major GC

- Old 영역이 꽉 차면 발생
- Old 영역의 불필요한 객체를 제거
- 시스템 성능에 큰 영향을 줄 수 있음

# 요약

- GC는 메모리를 자동 관리하여 개발자가 신경 쓸 필요 줄여줌
- Young, Old, Metaspace로 나뉜 영역별로 관리
- Stop the World 최소화가 중요한 튜닝 목표
- Java 8 이후 PermGen이 사라지고 Metaspace 도입

---

## Java 가비지 컬렉터(GC) 종류

### 1. Serial GC
- 옵션: `-XX:+UseSerialGC`
- 특징: 단일 스레드로 GC 작업 수행
- 장점: 메모리 적게 사용, 코드 단순
- 단점: GC 중 모든 애플리케이션 스레드 멈춤
- 사용: 임베디드, 테스트 환경

### 2. Parallel GC (Throughput Collector)
- 옵션: `-XX:+UseParallelGC`
- 특징: GC를 여러 스레드로 병렬 수행
- 장점: Throughput 최적화
- 단점: Stop-the-World 발생
- 사용: 대규모 배치 처리

### 3. CMS (Concurrent Mark Sweep) GC
- 옵션: `-XX:+UseConcMarkSweepGC`
- 특징: Old 영역 동시 스캔
- 장점: 짧은 Stop-the-World
- 단점: CPU 많이 사용, 메모리 파편화
- 사용: 짧은 응답 시간 요구 시스템

### 4. G1 GC (Garbage-First)
- 옵션: `-XX:+UseG1GC`
- 특징: 힙을 작은 Region으로 나눠 관리
- 장점: 큰 힙에서도 짧은 Pause 목표 설정
- 단점: 초기 성능 불안정 → Java 11 이후 안정화
- 사용: 대규모 힙 시스템, Spark

### 5. ZGC (Z Garbage Collector)
- 옵션: `-XX:+UseZGC`
- 특징: 초저지연 (Pause < 10ms)
- 장점: 수 TB 힙 지원, 초저지연
- 단점: JDK 11 이상 필요, CPU 사용량 높음
- 사용: 초지연 시스템

### 6. Shenandoah GC
- 옵션: `-XX:+UseShenandoahGC`
- 특징: GC 자체도 병렬
- 장점: 낮은 Pause, 대형 힙 지원
- 단점: 튜닝 복잡
- 사용: 지연 민감 시스템

## GC 요약 표

| GC 종류 | 특징 | 주 사용 환경 |
|:--------|:-----|:--------------|
| Serial GC | 단일 스레드, 단순 | 저사양, 테스트 |
| Parallel GC | Throughput 높음 | 대용량 배치 처리 |
| CMS GC | 지연 시간 최소화 | 대화형 서비스 |
| G1 GC | Region 기반, Pause 예측 가능 | 대규모 서버, Spark |
| ZGC | 초저지연 | 초대형 실시간 시스템 |
| Shenandoah GC | 병렬, 짧은 Pause | 대규모 지연 민감 시스템 |

---

# Java 버전 별 GC 지원 변화

### Java 7
- 기본 GC: Parallel GC
- 주요 지원: Serial GC, Parallel GC, CMS GC
- 특징: PermGen 존재, G1GC 실험적

### Java 8
- 기본 GC: Parallel GC
- 주요 지원: Serial, Parallel, CMS, G1GC (정식 지원)
- 특징: PermGen 제거, Metaspace 도입

### Java 9 ~ 10
- Parallel GC 기본
- G1GC 개선 (Full GC 최적화)
- CMS Deprecation 경고 추가

### Java 11
- 기본 GC: G1GC
- 주요 지원: Serial, Parallel, G1GC, ZGC (초기 버전)
- 특징: 기본 G1GC 변경, ZGC 추가

### Java 14
- CMS 완전 제거
- ZGC 기능 강화
- Shenandoah GC 추가

### Java 17
- 주요 지원: Serial, Parallel, G1GC, ZGC, Shenandoah
- 특징: ZGC, Shenandoah 안정화

## 버전별 요약 표

| Java 버전 | 주요 지원 GC | 비고 |
|:----------|:-------------|:-----|
| Java 7 | Serial, Parallel, CMS | G1GC 실험적 |
| Java 8 | Serial, Parallel, CMS, G1GC | G1GC 정식 도입 |
| Java 9~10 | Serial, Parallel, CMS, G1GC | G1GC 개선 |
| Java 11 | Serial, Parallel, G1GC, ZGC | 기본 G1GC, ZGC 추가 |
| Java 14 | Serial, Parallel, G1GC, ZGC, Shenandoah | CMS 삭제 |
| Java 17 | Serial, Parallel, G1GC, ZGC, Shenandoah | 안정화 |

---

# G1GC 구조 설명

- Heap 전체를 작은 **Region** 단위로 쪼갬
- Region별 역할:
  - Young Region: Eden, Survivor
  - Old Region: 살아남은 객체 저장
  - Humongous Region: 큰 객체 저장
- G1GC는 Young/Old 구분 없이 필요한 Region만 선택적 청소

# G1GC 주요 동작 단계

### 1. Young GC
- Eden Region 가득 차면 발생
- Eden 객체 중 살아남은 것만 Survivor로 이동
- 빠르고 자주 발생

### 2. Mixed GC
- Old 영역 사용량이 일정 임계치 넘으면 발생
- Young + 일부 Old Region 함께 수집
- Full GC를 예방하기 위한 전략

### 3. Full GC
- 최악의 경우 전체 Heap 청소
- Humongous 객체가 많거나 Old가 꽉 찼을 때 발생
- Stop-the-World로 전체 압축(Compaction)

# G1GC Region 수집 우선순위

- 각 Region마다 **Garbage Ratio**(죽은 객체 비율) 계산
- Garbage Ratio 높은 Region부터 선택적으로 수집
- "저비용/고효율" 방식으로 Pause 최소화

# 최종 요약

- Young GC → Eden만 청소 (빠름)
- Mixed GC → Young + Old 일부 청소 (Full GC 예방)
- Full GC → 전체 Heap 청소 (최악의 경우)
- G1GC는 **Region 단위로 최적화된, 예측 가능한 GC 시스템**
