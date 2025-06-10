# synchronized
- **Critical Section**을 지정하여 하나의 스레드만 접근 가능하게 한다.
- **동기화**를 통해 데이터 일관성을 보장할 수 있다.

## 주요 특징
| 항목 | 설명 |
|:-----|:-----|
| 상호 배제(Mutual Exclusion) | 한 번에 하나의 스레드만 임계 영역 진입 가능 |
| 가시성(Visibility) | synchronized 블록 안/밖으로 메모리 동기화 보장 |
| 적용 대상 | 메서드 전체 또는 특정 코드 블록 |
| **재진입(Reentrant)** | **같은 스레드가 중첩해서 lock 획득 가능** |
| **성능** | **JVM 레벨 최적화 (bias locking 등)** |

## 동작 원리

- `synchronized`는 **monitor lock** 사용
- lock을 획득한 스레드만 synchronized 블록 실행
- 나머지 스레드는 lock 해제될 때까지 대기

## 사용 방법
```java
// 1. 메서드 전체 동기화
public synchronized void method() {
    // 전체 메서드가 임계영역
}

// 2. 특정 객체를 monitor로 사용
public void method() {
    synchronized(this) {
        // this 객체의 monitor lock 사용
    }
}

// 3. 별도 객체를 monitor로 사용
private final Object lock = new Object();
public void method() {
    synchronized(lock) {
        // lock 객체의 monitor 사용
    }
}
```

---

# ReentrantLock

- **수동(lock, unlock)으로 제어**하는 동기화 도구
- synchronized와 같은 기능 + 더 명확하게 제어 가능
- `try-finally`로 반드시 `unlock()` 보장 필요

## 고급 기능
| 기능 | 설명 | 메서드 |
|:-----|:-----|:-------|
| **타임아웃** | 지정 시간 내 lock 획득 시도 | tryLock(timeout) |
| **인터럽트** | 대기 중 인터럽트 가능 | lockInterruptibly() |
| **공정성** | 대기 순서대로 lock 획득 | ReentrantLock(true) |
| **조건 변수** | 복수 조건으로 대기/알림 | newCondition() |

## 사용 예시
```java
private final ReentrantLock lock = new ReentrantLock();

public void method() {
    lock.lock();
    try {
        // 임계 구역
    } finally {
        lock.unlock(); // 반드시 필요!
    }
}

// 타임아웃 예시
public boolean methodWithTimeout() {
    if (lock.tryLock(1, TimeUnit.SECONDS)) {
        try {
            // 임계 구역
            return true;
        } finally {
            lock.unlock();
        }
    }
    return false; // lock 획득 실패
}
```

## Condition (ReentrantLock 전용)

| synchronized 메서드 | ReentrantLock 대응 메서드 |
|:--------------------|:---------------------------|
| wait() | await() |
| notify() | signal() |
| notifyAll() | signalAll() |

- await(): 스레드를 대기 상태로
- signal(), signalAll(): 대기 중인 스레드를 깨움

**복수 조건 변수 예시:**
```java
private final ReentrantLock lock = new ReentrantLock();
private final Condition notFull = lock.newCondition();
private final Condition notEmpty = lock.newCondition();

// 생산자: 버퍼가 가득 찰 때까지 대기
while (count == capacity) {
    notFull.await();
}

// 소비자: 버퍼가 비어있을 때까지 대기  
while (count == 0) {
    notEmpty.await();
}
```

---

# synchronized vs ReentrantLock

| 항목 | synchronized | ReentrantLock |
|:-----|:--------------|:--------------|
| 락 획득 방식 | 자동 | 명시적 lock()/unlock() |
| 상태 제어 (대기/알림) | wait(), notify(), notifyAll() | await(), signal(), signalAll() |
| 유연성 | 낮음 | 높음 (타임아웃, 인터럽트 지원 등) |
| 예외 처리 필요성 | 없음 | 반드시 unlock() 보장해야 함 |
| **성능** | **일반적으로 더 빠름** | **고급 기능 사용 시 선택** |
| **코드 복잡도** | **낮음** | **높음 (try-finally 필수)** |
| **JVM 최적화** | **✅ 다양한 최적화 적용** | **제한적** |

---

# Semaphore 포함 비교

| 항목 | synchronized | ReentrantLock | Semaphore |
|:-----|:--------------|:--------------|:----------|
| **허용 개수** | 1개 (독점) | 1개 (독점) | **N개 (공유)** |
| **주 목적** | 임계영역 보호 | 임계영역 보호 | **리소스 풀 관리** |
| **재진입** | ✅ | ✅ | ❌ |
| **조건 대기** | wait/notify | Condition | ❌ |
| **사용 예** | 단일 자원 보호 | 고급 제어 필요 시 | **DB 커넥션, API 호출 제한** |

---

# 선택 가이드

## synchronized 사용 권장
- 단순한 임계영역 보호
- 짧은 락 보유 시간
- 코드 간결성이 중요한 경우

## ReentrantLock 사용 권장  
- 타임아웃이 필요한 경우
- 인터럽트 가능한 대기가 필요한 경우
- 복수 조건 변수가 필요한 경우
- 공정한 락 획득이 필요한 경우

## Semaphore 사용 권장
- 제한된 리소스 풀 관리 (DB 커넥션, API 호출 등)
- N개까지 동시 접근 허용이 필요한 경우

---

# 요약

- `synchronized`: 간단, 코드 짧음, 자동 관리, **일반적으로 첫 번째 선택**
- `ReentrantLock`: 유연성 높음, 수동 관리 필요, **고급 기능 필요 시 선택**
- `Semaphore`: **리소스 풀 관리**, N개 동시 접근 제어
