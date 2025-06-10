# Semaphore

## 개념

**Semaphore**는 **제한된 수의 리소스에 대한 동시 접근을 제어**하는 동시성 제어 두기앋.

- **Counting Semaphore**: N개의 permit를 가지고 있음
- **Binary Semaphore**: 1개의 permit만 가진 특별한 경우 (mutex와 유사)

## 주요 특징

| 특징 | 설명                             |
|:-----|:-------------------------------|
| **허가 기반** | N개의 permit를 관리                 |
| **공유 리소스** | 여러 스레드가 동시에 접근 가능 (허가 수만큼)     |
| **재진입 불가** | 같은 스레드라도 매번 acquire/release 필요 |
| **공정성** | fair/unfair 모드 지원              |
| **인터럽트 지원** | 대기 중 인터럽트 가능                   |

## 동작 원리

```
초기 허가 수: 3

스레드1 → acquire() → 허가 2개 남음
스레드2 → acquire() → 허가 1개 남음  
스레드3 → acquire() → 허가 0개 남음
스레드4 → acquire() → 대기 (허가 없음)

스레드1 → release() → 허가 1개 증가
스레드4 → 대기 해제 → 실행
```

## 주요 메서드

### 기본 메서드
```java
// 허가 획득
acquire()           // 1개 획득 (블로킹)
acquire(int permits) // N개 획득 (블로킹)

// 허가 해제  
release()           // 1개 해제
release(int permits) // N개 해제

// 즉시 시도
tryAcquire()        // 즉시 1개 시도
tryAcquire(int permits) // 즉시 N개 시도

// 타임아웃
tryAcquire(long timeout, TimeUnit unit)
tryAcquire(int permits, long timeout, TimeUnit unit)

// 인터럽트 가능
acquireInterruptibly()
acquireInterruptibly(int permits)
```

### 상태 확인 메서드
```java
availablePermits()  // 사용 가능한 허가 수
hasQueuedThreads()  // 대기 중인 스레드 존재 여부
getQueueLength()    // 대기 중인 스레드 수
```

## 사용 예시

### 1. 기본 사용법
```java
// 최대 3개 동시 접근 허용
Semaphore semaphore = new Semaphore(3);

public void accessResource() {
    try {
        semaphore.acquire(); // 허가 획득
        
        // 임계 영역 - 최대 3개 스레드만 동시 실행
        System.out.println("리소스 접근 중: " + Thread.currentThread().getName());
        Thread.sleep(2000); // 작업 시뮬레이션
        
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    } finally {
        semaphore.release(); // 반드시 허가 반납
    }
}
```

### 2. 타임아웃 사용
```java
public boolean accessResourceWithTimeout() {
    try {
        // 1초 내에 허가 획득 시도
        if (semaphore.tryAcquire(1, TimeUnit.SECONDS)) {
            try {
                // 리소스 사용
                doWork();
                return true;
            } finally {
                semaphore.release();
            }
        } else {
            System.out.println("타임아웃: 리소스 접근 실패");
            return false;
        }
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        return false;
    }
}
```

### 3. 복수 허가 사용
```java
// 대용량 작업용 - 허가 3개 필요
public void heavyWork() {
    try {
        semaphore.acquire(3); // 3개 허가 동시 획득
        
        // 리소스를 많이 사용하는 작업
        performHeavyOperation();
        
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    } finally {
        semaphore.release(3); // 3개 허가 동시 반납
    }
}
```
---

## 실제 사용 시나리오

### 1. 데이터베이스 커넥션 풀
```java
public class ConnectionPool {
    private final Semaphore semaphore;
    private final Queue<Connection> connections;
    
    public ConnectionPool(int maxConnections) {
        this.semaphore = new Semaphore(maxConnections);
        this.connections = new ConcurrentLinkedQueue<>();
        // 커넥션 초기화...
    }
    
    public Connection getConnection() throws InterruptedException {
        semaphore.acquire(); // 커넥션 허가 획득
        return connections.poll();
    }
    
    public void returnConnection(Connection conn) {
        connections.offer(conn);
        semaphore.release(); // 허가 반납
    }
}
```

### 2. API 호출 제한
```java
public class APIRateLimiter {
    private final Semaphore semaphore;
    
    public APIRateLimiter(int maxCallsPerSecond) {
        this.semaphore = new Semaphore(maxCallsPerSecond);
        
        // 1초마다 허가 복원
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
        scheduler.scheduleAtFixedRate(() -> {
            semaphore.release(maxCallsPerSecond - semaphore.availablePermits());
        }, 1, 1, TimeUnit.SECONDS);
    }
    
    public boolean callAPI() {
        if (semaphore.tryAcquire()) {
            try {
                // API 호출
                return makeAPICall();
            } finally {
                // 여기서는 release하지 않음 (시간 기반 복원)
            }
        }
        return false; // 호출 제한 초과
    }
}
```

### 3. 파일 다운로드 제한
```java
public class DownloadManager {
    private final Semaphore downloadSemaphore = new Semaphore(5); // 최대 5개 동시 다운로드
    
    public CompletableFuture<Void> downloadFile(String url) {
        return CompletableFuture.runAsync(() -> {
            try {
                downloadSemaphore.acquire();
                
                System.out.println("다운로드 시작: " + url);
                // 파일 다운로드 로직
                Thread.sleep(3000); // 다운로드 시뮬레이션
                System.out.println("다운로드 완료: " + url);
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                downloadSemaphore.release();
            }
        });
    }
}
```

## 공정성 (Fairness)

```java
// 비공정 (기본값) - 성능이 더 좋음
Semaphore unfairSemaphore = new Semaphore(3);

// 공정 - 대기 순서대로 허가 부여
Semaphore fairSemaphore = new Semaphore(3, true);
```

| 구분 | 비공정 (false) | 공정 (true) |
|:-----|:---------------|:------------|
| **성능** | 더 빠름 | 상대적으로 느림 |
| **순서** | 순서 보장 안됨 | FIFO 순서 보장 |
| **기아 현상** | 발생 가능 | 방지됨 |
| **사용 권장** | 일반적인 경우 | 순서가 중요한 경우 |

## 다른 동시성 도구와 비교

| 도구 | 허용 개수 | 재진입 | 주 용도 |
|:-----|:----------|:-------|:-------|
| **Semaphore** | **N개** | ❌ | **리소스 풀 관리** |
| synchronized | 1개 | ✅ | 임계영역 보호 |
| ReentrantLock | 1개 | ✅ | 고급 잠금 제어 |
| CountDownLatch | 1회성 | ❌ | 완료 대기 |

## 주의사항 및 Best Practices

### 잘못된 사용법
```java
// 1. release() 누락
semaphore.acquire();
doWork(); // 예외 발생 시 release() 호출 안됨

// 2. 과도한 release()
semaphore.release();
semaphore.release(); // 허가 수가 의도치 않게 증가

// 3. 재진입 가정
semaphore.acquire();
methodThatAlsoAcquires(); // 데드락 위험
```

### 올바른 사용법
```java
// 1. try-finally 사용
try {
    semaphore.acquire();
    doWork();
} finally {
    semaphore.release(); // 반드시 실행됨
}

// 2. 허가 수 추적
int permits = 2;
try {
    semaphore.acquire(permits);
    doWork();
} finally {
    semaphore.release(permits); // 동일한 수만큼 반납
}

// 3. 상태 확인 후 사용
if (semaphore.availablePermits() > 0) {
    // 즉시 사용 가능한 경우에만
}
```

## 성능 고려사항

- **공정성 vs 성능**: 공정 모드는 성능이 떨어짐
- **허가 수**: 너무 많은 허가는 메모리 오버헤드 증가
- **대기 스레드**: 많은 대기 스레드는 컨텍스트 스위칭 비용 증가

## 요약

**Semaphore는 제한된 리소스 풀을 관리할 때 사용하자**
- **DB 커넥션 풀 관리**
- **API 호출 수 제한** 
- **동시 다운로드/업로드 제한**
- **스레드풀과 독립적인 리소스 제어**

**핵심 원칙**: acquire()와 release()를 쌍으로 사용하고, 반드시 try-finally로 허가 반납할 것!
