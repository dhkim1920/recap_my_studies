
# Python 메모리 관리 정리
## 1. 개요
파이썬은 자동 메모리 관리 기능을 제공함, 사용되지 않는 객체는 **Garbage Collector**를 통해 자동으로 제거됨

## 2. Reference Counting
파이썬 객체는 참조 카운트를 유지, 객체에 대한 참조가 생성될 때 카운트가 증가하고, 참조가 제거되면 감소,
참조 수가 0이 되면 메모리에서 해제됨

예제:
```python
import sys

a = []
print(sys.getrefcount(a))  # 기본 참조 포함
b = a
print(sys.getrefcount(a))  # 참조 증가
del b
print(sys.getrefcount(a))  # 참조 감소
```

> **주의**: 순환 참조가 발생하면 참조 수가 0이 되지 않아 수동 수집이 필요

---

## 3. Generational Garbage Collection
파이썬은 순환 참조 문제를 해결하기 위해 **Generational GC**를 사용, 객체는 생성 시 다음 세대 중 하나에 속하게 됨

- Generation 0: 새로 생성된 객체
- Generation 1: 0세대를 통과한 객체
- Generation 2: 가장 오래된 객체

GC는 보통 세대 0에서 자주 실행되며, 상위 세대로 갈수록 수집 빈도는 낮음

임계값 확인:
```python
import gc
print(gc.get_threshold())  # (700, 10, 10)
```

## 4. gc 모듈을 통한 수동 제어
### 수집 강제 실행
```python
gc.collect()
```

### GC 비활성화 및 재활성화

```python
gc.disable()
gc.enable()
```

### 임계값 설정
```python
gc.set_threshold(500, 5, 5)
```


## 5. 순환 참조 예제
```python
import gc

class Node:
    def __init__(self):
        self.ref = self

def create_cycle():
    node = Node()

create_cycle()
print(gc.collect())  # 수집된 객체 수 반환
```

## 6. 요약
- 참조 카운팅은 기본 메커니즘이며, 참조가 0이면 객체를 해제
- 순환 참조와 같이 참조 카운팅만으로는 수집되지 않는 객체는 Generational GC로 수집됨
- `gc` 모듈을 통해 GC 동작을 세밀하게 제어 가능
