# Spark Catalyst Optimizer & Tungsten Execution Engine

## 1. Catalyst Optimizer

### 개념
- Spark SQL의 논리적/물리적 쿼리 최적화 엔진
- 트리 기반의 쿼리 계획 변환 시스템

### 작동 단계

1. **Unresolved Logical Plan 생성**
   - DataFrame, SQL 쿼리 등으로 작성된 쿼리 파싱

2. **Analysis**
   - 테이블/컬럼 이름을 확인하고 스키마 연결
   - → Resolved Logical Plan

3. **Logical Optimization**
   - 필터 푸시다운, 프로젝션 제거, 조건 병합 등 논리적 규칙 적용
   - → Optimized Logical Plan

4. **Physical Planning**
   - 다양한 실행 계획 후보 생성 (예: SortMergeJoin, BroadcastHashJoin)

5. **Cost-Based Optimization (선택적)**
   - 통계 정보가 있으면 비용 기반 최적화 수행

6. **Code Generation 준비**
   - 실행 가능한 plan 생성 → Tungsten 엔진이 실행

### 대표 최적화 예
- filter → join 순서 변경 (필터 푸시다운)
- 중복 column 제거 (project pruning)
- 불필요한 서브쿼리 제거

---

## 2. Tungsten Execution Engine

### 개념
- Spark의 실행 성능을 극대화하기 위한 물리적 실행 엔진
- Catalyst가 만든 쿼리 계획을 최저 레벨에서 실행 최적화

### 주요 기능

- **Whole-Stage Code Generation (WSCG)**  
  실행 계획을 Java 코드로 자동 생성 후 컴파일 → JVM 최적화 적용

- **Off-Heap Memory 관리**  
  GC 부담 줄이기 위해 JVM heap 외 메모리 직접 사용 (정렬, 집계 등)

- **Binary Format 사용**  
  내부 표현을 효율적인 바이너리 구조로 변환  
  튜플 대신 메모리 배열 기반 연산 수행

### 핵심 목표
- CPU 캐시 친화적 연산
- GC 오버헤드 최소화
- 명령어 수준 최적화

---

## 정리 비교

| 구분         | Catalyst Optimizer           | Tungsten Engine                          |
|--------------|-------------------------------|------------------------------------------|
| 계층         | 논리/물리 쿼리 최적화         | 물리 실행 엔진                           |
| 역할         | 쿼리 트리 분석 및 변환        | 실행 코드 생성 및 메모리 최적화         |
| 주 기능      | 필터 푸시다운, 조인 순서 최적화 등 | 코드 생성, 오프힙 메모리, 바이너리 처리 |
| 작동 시점    | 쿼리 작성 시                   | 쿼리 실행 시                             |
