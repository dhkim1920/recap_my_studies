# Java 함수형 인터페이스 정리

## 1. Supplier<T>

- **정의**: `T get();`
- **특징**: 입력 매개변수 없이 결과를 반환하는 함수형 인터페이스
- **용도**: 객체 생성, lazy evaluation 등에 사용
- **예시**

```java
import java.util.*;
import java.util.function.Supplier;

public class ConfigCache {
    private static final Map<String, String> config = new HashMap<>();

    public static String getOrLoad(String key, Supplier<String> loader) {
        return config.computeIfAbsent(key, k -> loader.get());
    }

    public static void main(String[] args) {
        String value = getOrLoad("db.host", () -> loadFromDB("db.host"));
        System.out.println(value);
    }

    static String loadFromDB(String key) {
        return "localhost"; // DB 조회 가정
    }
}
```

---

## 2. Consumer<T>

- **정의**: `void accept(T t);`
- **특징**: 하나의 입력을 받아서 소비하고 반환값이 없는 함수형 인터페이스
- **용도**: 입력값에 대한 처리(예: 출력, 저장 등)에 사용, 주로 리스트 순회 처리, 콜백 처리에 사용
- **예시**

```java
import java.util.function.Consumer;

public class UserService {
    public void save(String user, Consumer<String> onSaved) {
        // 저장 로직 생략
        onSaved.accept(user); // 저장 후 콜백 실행
    }

    public static void main(String[] args) {
        new UserService().save("kim", user -> System.out.println("저장됨: " + user));
    }
}
```

---

## 3. Function<T, R>

- **정의**: `R apply(T t);`
- **특징**: 하나의 입력을 받아서 결과를 반환하는 함수형 인터페이스
- **용도**: 입력값을 변환하거나 계산하여 결과를 생성할 때 사용
- **예시**

```java
import java.util.function.Function;

class UserDto {
    String name;
    UserDto(String name) { this.name = name; }
}
class UserEntity {
    String username;
    UserEntity(String username) { this.username = username; }
}

public class Mapper {
    static Function<UserDto, UserEntity> dtoToEntity = dto -> new UserEntity(dto.name);

    public static void main(String[] args) {
        UserDto dto = new UserDto("kim");
        UserEntity entity = dtoToEntity.apply(dto);
        System.out.println("Entity 이름: " + entity.username);
    }
}

```

---

## 4. Predicate<T>

- **정의**: `boolean test(T t);`
- **특징**: 하나의 입력을 받아서 boolean 결과를 반환하는 함수형 인터페이스
- **용도**: 조건 검사나 필터링 등에 사용
- **예시**

```java
import java.util.function.Predicate;
import java.util.List;

public class EmailFilter {
    public static void main(String[] args) {
        Predicate<String> isValidEmail = email -> email.contains("@") && email.endsWith(".com");

        List<String> emails = List.of("test@a.com", "invalid", "user@site.org", "good@b.com");
        emails.stream()
              .filter(isValidEmail)
              .forEach(System.out::println); // test@a.com, good@b.com
    }
}
```
