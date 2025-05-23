
# volatile
- 변수를 **main memory**에 직접 읽고 쓰게 강제한다.
- 스레드 간 변수 값 동기화를 보장한다.

## 왜 사용할까??
- 기본적으로 스레드는 자신만의 CPU 캐시를 사용할 수 있다.
- 다른 스레드가 변수 값을 변경해도, 캐시 때문에 변경을 인식 못할 수 있다.
- `volatile`을 붙이면 항상 **main memory**에서 값을 읽고 쓴다.

## 주요 특징

| 항목 | 설명 |
|:-----|:-----|
| 가시성(Visibility) | 다른 스레드가 변경한 값을 즉시 볼 수 있음 |
| 순서 보장(Partial Ordering) | volatile 변수 읽기/쓰기 순서 보장 |
| 원자성(Atomicity) | 없음 (읽고 쓰기는 원자적이지만 복합 연산은 보장 안 함) |


## 예시
```java
public class Example {
    private volatile boolean running = true;

    public void stop() {
        running = false;
    }

    public void run() {
        while (running) {
            // do something
        }
    }
}
```
- `running`을 다른 스레드에서 `false`로 바꾸면, `while` 루프가 즉시 종료됨

## 요약

- `volatile`은 가시성 문제를 해결한다.
- 단, 복합적인 연산(증가, 감소 등)이 필요하면 `synchronized`나 Atomic 클래스 사용 필요

---

# 가시성 문제 (Visibility Problem)

- 하나의 스레드가 변수 값을 변경했을 때, 다른 스레드가 그 변경을 즉시 볼 수 없는 현상

## 왜 발생하는가?
- 각 스레드는 자신만의 CPU 캐시에 변수 값을 복사해서 사용
- 메인 메모리와 스레드 캐시 사이에 동기화가 바로 일어나지 않기 때문
- 한쪽 스레드가 값을 변경해도, 다른 스레드는 예전 값을 볼 수 있음

## 예시 (가시성 문제 발생)
```java
public class Example {
    private boolean running = true;

    public void stop() {
        running = false;
    }

    public void run() {
        while (running) {
            // 무한 루프에 빠질 수 있음
        }
    }
}
```
- `stop()` 메서드에서 `running = false`로 바꿔도,  
  `run()`을 돌고 있는 스레드는 예전 값을 계속 볼 수 있음

---

# 복합 연산에서는 왜 안될까?
먼저 예시를 보자
```java
volatile int count = 0;

Thread A: // 동시에 실행
count = count + 1;  // 1. 읽기(count=0), 2. 계산(1), 3. 쓰기(count=1)

Thread B:
count = count + 1;  // 1. 읽기(count=0), 2. 계산(1), 3. 쓰기(count=1)
```
- 여기서 값은 2가 될 것으로 기대하나 결과는 1이다.
- 두 쓰레드가 값을 덮어쓰기 때문이다.

### 복합 연산은 사실 이렇게 여러 단계를 거친다!
- 예제를 분석 하면 이렇다. 
  1. 현재 x 값을 메모리에서 읽는다.
  2. x + 1 연산을 한다.
  3. 새 값을 다시 메모리에 쓴다
  → 이 세 단계는 따로따로 일어나기 때문이다.