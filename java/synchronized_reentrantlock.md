
# synchronized

- **임계 영역(Critical Section)**을 지정하여 하나의 스레드만 접근 가능
- **동기화**를 통해 데이터 일관성을 보장

## 주요 특징

| 항목 | 설명 |
|:-----|:-----|
| 상호 배제(Mutual Exclusion) | 한 번에 하나의 스레드만 임계 영역 진입 가능 |
| 가시성(Visibility) | synchronized 블록 안/밖으로 메모리 동기화 보장 |
| 적용 대상 | 메서드 전체 또는 특정 코드 블록 |

## 동작 원리

- `synchronized`는 **모니터 락(monitor lock)** 사용
- lock을 획득한 스레드만 synchronized 블록 실행
- 나머지 스레드는 lock 해제될 때까지 대기

---

## ReentrantLock

- **수동(lock, unlock)으로 제어**하는 동기화 도구
- synchronized와 같은 기능 + 더 명확하게 제어 가능
- `try-finally`로 반드시 `unlock()` 보장 필요

### 사용 예시
```java
private final ReentrantLock lock = new ReentrantLock();

public void method() {
    lock.lock();
    try {
        // 임계 구역
    } finally {
        lock.unlock();
    }
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

---

## synchronized vs ReentrantLock

| 항목 | synchronized | ReentrantLock |
|:-----|:--------------|:--------------|
| 락 획득 방식 | 자동 | 명시적 lock()/unlock() |
| 상태 제어 (대기/알림) | wait(), notify(), notifyAll() | await(), signal(), signalAll() |
| 유연성 | 낮음 | 높음 (타임아웃, 인터럽트 지원 등) |
| 예외 처리 필요성 | 없음 | 반드시 unlock() 보장해야 함 |

---

## 요약

- `synchronized`: 간단, 코드 짧음, 자동 관리
- `ReentrantLock`: 유연성 높음, 수동 관리 필요
