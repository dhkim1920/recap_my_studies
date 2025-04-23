
## Python 일급 객체, 데코레이터, 클로저 정리

### First-Class Function (일급 객체)

파이썬은 함수도 객체로 다루는 언어로, 함수는 일급 객체임

1. 변수에 할당 가능
2. 다른 함수의 인자로 전달 가능
3. 다른 함수의 반환값으로 사용 가능
4. 리스트, 딕셔너리 등의 데이터 구조에 저장 가능

예시:
```python
def add(x, y):
    return x + y

f = add
print(f(2, 3))  # 5

def apply(func, x, y):
    return func(x, y)

print(apply(add, 2, 3))  # 5

def outer():
    def inner():
        return "Hello"
    return inner

greet = outer()
print(greet())  # Hello

func_list = [add, max, min]
print(func_list[0](10, 5))  # 15
```

이러한 일급 함수 성질 때문에 데코레이터와 클로저 같은 기능이 가능해짐

### Decorator (데코레이터)

함수를 인자로 받아서, 기능을 감싼 새로운 함수를 반환하는 함수, 
기존 함수의 코드를 수정하지 않고 기능을 확장할 수 있게 해줌

예시:
```python
def decorator(func):
    def wrapper():
        print("before")
        func()
        print("after")
    return wrapper

@decorator
def say_hello():
    print("Hello!")

say_hello()
```

설명:
- `@decorator`는 `say_hello = decorator(say_hello)`와 동일
- `decorator`는 `func`를 인자로 받아 `wrapper`라는 감싸는 함수를 반환
- 원래 함수가 감싸진(wrapper) 함수로 치환됨

### Closures (클로저)

외부 함수의 지역 변수(자유 변수)를 참조하는 내부 함수. 외부 함수가 종료된 이후에도 내부 함수가 해당 변수의 값을 유지하고 사용 가능

예시:
```python
def outer_func():
    message = 'Hi'
    def inner_func():
        print(message)
    return inner_func

my_func = outer_func()
my_func()  # 출력: Hi
```

`my_func.__closure__` 속성으로 클로저 내부 변수에 접근 가능:
```python
print(my_func.__closure__[0].cell_contents)  # Hi
```


> 클로저는 상태 유지, 데이터 은닉, 데코레이터 구현 등에 활용됨
