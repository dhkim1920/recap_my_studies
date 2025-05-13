
## ExecutorService

- Java에서 스레드를 관리하는 인터페이스
- 직접 스레드를 생성하지 않고, **작업 단위(Runnable, Callable)** 를 제출하면 실행
- `java.util.concurrent.ExecutorService` 패키지에 있다.

### 주요 특징

| 항목 | 설명                                           |
|:-----|:---------------------------------------------|
| 스레드 관리 | 스레드를 직접 만들고 종료하지 않아도 됨                       |
| 작업 제출 | Runnable, Callable 제출 가능                     |
| 비동기 실행 | 작업을 비동기로 실행하고 Future로 결과 받음                  |
| 작업 종료 제어 | shutdown(), shutdownNow()로 graceful/강제 종료 지원 |
| 리소스 최적화 | 스레드 pooling으로 성능 향상                          |

### 주요 메서드

| 메서드 | 설명 |
|:--------|:-----|
| submit(Runnable) | 비동기로 실행하고 Future<?> 반환 |
| submit(Callable<T>) | 결과값을 반환하는 작업을 제출, Future<T> 반환 |
| invokeAll(Collection<Callable>) | 여러 Callable을 동시에 실행, 모든 작업이 끝날 때까지 대기 |
| shutdown() | 더 이상 새로운 작업을 받지 않고, 현재 작업 완료 후 종료 |
| shutdownNow() | 현재 실행 중인 작업을 모두 중단 시도 후 종료 |
| awaitTermination(timeout, unit) | 지정한 시간 동안 종료될 때까지 대기 |

## 예제

**Runnable 제출**
```java
ExecutorService executorService = Executors.newFixedThreadPool(3);
executorService.submit(() -> {
    System.out.println("비동기 작업 실행");
});
executorService.shutdown();
```

**Callable 제출**
```java
Future<Integer> future = executorService.submit(() -> {
    return 10 + 20;
});
Integer result = future.get(); // 결과 30
```

## 정리

- ExecutorService는 **비동기 작업 실행을 표준화한 인터페이스**
- 직접 스레드를 만들 필요 없이 **작업 단위만 제출**
- 스레드 풀을 효율적으로 관리하고, 애플리케이션의 **성능, 안정성** 향상

---

## newFixedThreadPool 동작 방식

- 최대 nThreads 개수만큼 스레드 생성
- 요청이 오면 가능한 스레드에 작업 할당
- 남는 스레드 없으면 queue에 쌓음
- 스레드가 작업 끝내면 큐에서 다음 작업 처리

## newCachedThreadPool()

- 필요한 만큼 새로운 스레드를 생성
- idle 상태 스레드는 재사용
- 스레드 개수 제한 없음

## FixedThreadPool vs CachedThreadPool

| 구분 | FixedThreadPool | CachedThreadPool |
|:-----|:----------------|:-----------------|
| 스레드 수 | 고정 | 무제한 (필요할 때 생성) |
| 초과 작업 처리 | 큐에 대기 | 새 스레드 생성 |
| 스레드 유지 | 계속 유지 | 60초 이상 idle이면 제거 |
| 특징 | 안정적, 예측 가능 | 빠른 대응, 자원 과다 사용 위험 |


## 요약

- **FixedThreadPool**: 정해진 스레드 수로 처리, 큐 사용
- **CachedThreadPool**: 스레드를 필요할 때마다 생성, 대기 스레드 재사용
