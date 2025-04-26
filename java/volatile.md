
# volatile

- **변수를 메인 메모리(main memory)**에 직접 읽고 쓰게 강제
- 스레드 간 변수 값 동기화를 보장

## 왜 사용할까??

- 기본적으로 스레드는 자신만의 CPU 캐시를 사용할 수 있음
- 다른 스레드가 변수 값을 변경해도, 캐시 때문에 변경을 인식 못할 수 있음
- `volatile`을 붙이면 항상 **공유 메모리(메인 메모리)**에서 값을 읽고 씀

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
- 단, **복합적인 연산(증가, 감소 등)**이 필요하면 `synchronized`나 Atomic 클래스 사용 필요

---

# 가시성 문제 (Visibility Problem)

- 하나의 스레드가 변수 값을 변경했을 때
- 다른 스레드가 그 변경을 즉시 볼 수 없는 현상

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

