# Java에서 클래스 이름으로 객체를 동적으로 생성하는 두 가지 방식

## 1. Factory 패턴 (Class.forName() 기반)

```java
interface Service {
    void run();
}

class ServiceA implements Service {
    public void run() { System.out.println("A"); }
}

class ServiceB implements Service {
    public void run() { System.out.println("B"); }
}
```

```java
public class ServiceFactory {
    public static Service create(String className) {
        try {
            Class<?> clazz = Class.forName(className);
            return (Service) clazz.getDeclaredConstructor().newInstance();
        } catch (Exception e) {
            throw new RuntimeException("Invalid class: " + className, e);
        }
    }
}
```

**사용 예:**
```java
Service service = ServiceFactory.create("com.example.ServiceA");
service.run();
```

- 리플렉션 사용: 클래스 이름을 문자열로 받아 동적으로 로딩
- 기본 생성자가 반드시 필요
- 형변환 오류 방지를 위해 공통 인터페이스 필요

## 2. Registry 기반 Supplier 패턴

```java
public class ServiceRegistry {
    private static final Map<String, Supplier<Service>> registry = new HashMap<>();

    static {
        registry.put("A", ServiceA::new);
        registry.put("B", ServiceB::new);
    }

    public static Service get(String name) {
        Supplier<Service> supplier = registry.get(name);
        if (supplier == null) {
            throw new IllegalArgumentException("No service: " + name);
        }
        return supplier.get();
    }
}
```

**사용 예:**
```java
Service service = ServiceRegistry.get("A");
service.run();
```

- 리플렉션 없이 안전하고 가볍게 객체 생성
- IDE 리팩토링, 타입 안전성, 테스트 편함
- 새로운 서비스 추가 시 registry에만 추가

### 왜 Supplier + static을 사용하는가?

- **Supplier**: 객체 생성 로직을 함수형으로 캡슐화 (`ServiceA::new`)
- **static registry**: 전역 공유, 싱글톤처럼 동작

## 리플렉션 없이 생성하면 좋은 이유는 뭘까?

| 항목               | 리플렉션 사용        | Supplier 사용     |
|--------------------|----------------------|-------------------|
| 성능               | 느림                 | 빠름              |
| 타입 안정성        | 낮음 (런타임 오류)   | 높음 (컴파일 시 검증) |
| IDE 리팩토링 지원  | 안 됨                | 잘 됨             |
| 보안 제한 우회     | 어려움               | 안전              |
| 가독성/유지보수    | 복잡                 | 간단              |

## 결론

- **동적으로 클래스 로딩** 필요 시 → `Class.forName()` 기반 Factory
- **미리 정의된 집합 중 선택** 시 → Supplier 기반 Registry 패턴 사용 권장