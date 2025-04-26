
## Future vs CompletableFuture

| 구분 | Future | CompletableFuture |
|:-----|:------|:------------------|
| 기본 제공 | Java 5 | Java 8 |
| 비동기 실행 | 가능 | 가능 |
| 완료 알림 | 없음 (직접 get() 호출해야 함) | 완료 후 콜백(thenXxx) 등록 가능 |
| 예외 처리 | get() 호출 시 예외 던짐 | 예외 발생 시 별도로 처리 가능(exceptionally 등) |
| 체이닝(연속 작업) | 불가 | thenApply, thenCompose 등으로 연속 작업 가능 |
| 조합(여러 작업 합치기) | 불편함 | 매우 간단함 (allOf, anyOf 지원) |
| 취소 | 가능 | 가능 |
| 블로킹 | get() 호출 시 블로킹 | get()은 동일, 다만 thenXxx 사용 시 논블로킹 |

## 요약

- **Future**는 결과를 가져오려면 `get()`으로 직접 대기해야 합니다.
- **CompletableFuture**는 작업 완료 후 **자동으로 콜백** 처리할 수 있습니다.
- **CompletableFuture**는 **체이닝**, **예외처리**, **작업 조합**까지 쉽게 지원합니다.

---

## CompletableFuture 주요 메서드

### runAsync

- 리턴값 없이 비동기 작업 실행
```java
CompletableFuture<Void> future = CompletableFuture.runAsync(() -> {
    System.out.println("비동기 작업 실행");
});
```

---

### thenRun

- 이전 작업 완료 후 새 작업 실행 (리턴값 없음)
```java
CompletableFuture.runAsync(() -> {
    System.out.println("첫 번째 작업");
}).thenRun(() -> {
    System.out.println("두 번째 작업");
});
```

---

### supplyAsync

- 반환값을 가지는 비동기 작업 실행
```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "결과값";
});
```

---

### exceptionally

- 예외 발생 시 대체 로직 실행
```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    throw new RuntimeException("문제 발생");
}).exceptionally(throwable -> {
    System.out.println("예외 처리: " + throwable.getMessage());
    return "대체 결과";
});
```

