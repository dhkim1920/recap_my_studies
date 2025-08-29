# 파이썬 알고리즘 개념 정리

## 파이썬 개념
### == 와 is 의 차이
- `==`: 두 객체의 값이 같은지 비교
- `is`: 두 객체의 메모리 주소가 같은지 비교

값 비교 시에는 `==`, 객체 동일성 확인 시에는 `is`를 사용

### False와 Falsy의 차이점
- `False`는 불리언 값 그 자체를 의미
- `Falsy`는 조건식에서 거짓으로 간주되는 값들의 모음

조건문에서 값의 존재 여부를 확인할 때는 `if not value:`처럼 `bool()` 평가를 이용하는 것이 좋다.

### None 비교: `==` vs `is`
- `is`: None 비교할 때 사용해야 함
- `==`: 가능은 하지만 권장하지 않음

None은 파이썬에서 하나의 객체로 취급되기 때문에 `is`를 사용하는 것이 안전

### 정수 나눗셈 연산자: `/` vs `//`
- `/`: 실수 나눗셈 (소수점 포함)
- `//`: 정수 나눗셈 (몫만 반환)

## 알아두면 좋은 모듈 및 함수

### 입력
- 입력: `input()`
- 입력 타입 변환: `int(input())`
- 여러개 띄어 입력`map(int, input().split())`
- 여러 줄 입력: `[map(int, input().split()) for _ in range(N)]`
- 그래프 만들기
  - ```python
    graph = [[] for _ in range(N + 1)]
    edges = []
  
    for _ in range(M):
        a, b = map(int, input().split())
        edges.append((a, b))
  
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    ```

### 문자열 처리
- 소문자 변환:`lower()`
- 대문자 변환: `upper()`
- 정렬 리스트 반환: `sorted(iterable, key=None, reverse=False)`
- 리스트 정렬: `list.sort(key=None, reverse=False)` (return 없음)
- 리스트를 문자열로 연결: `str.join(iterable)`
- 문자열을 리스트로 분리: `str.split(separator, maxsplit)`
- 공백제거 (양쪽, 왼쪽, 오른쪽):`str.strip()`, `str.lstrip()`, `str.rstrip()`
- 치환: `str.replace(old, new)`
- 합: `sum(iterable)`
- 최대, 최소: `max(iterable)`, `min(iterable)`
- 문자열 순회: `enumerate(str)`
  - ```python
    for idx, ch in enumerate(word):
        print(idx, ch)
    ```

### 수학
- 절댓값: `abs(x)`
- 최대공약수: `math.gcd(a, b)`
- 최소공배수: `math.lcm(a, b)`
- 제곱근: `math.sqrt(x)`
- 조합: `math.comb(n, r)`
  - 조합 = 선택만, 무작위
  - `n(n + 1)/2 = C(n + 1, 2)`
- 순열: `math.perm(n, r)`
  - 선택 + 나열
- 소인수 분해
  - 2, 3, 5, 7, 11, 13 등 소수로 먼저 나누어 본다.
  - A의 약수: `A = a^m * b^n`
  - A약수의 개수: `(m+1) * (n+1)`
- 올림
  - (x + y - 1) // y

### 양방향 큐 (Deque)
- `from collections import deque`
- DFS, BFS에서 사용하기 좋음
- 주요 함수
  - extend(iterable): 오른쪽에 iterable 원소들을 순차적으로 추가
  
    ```예: deque([1, 2]).extend([3, 4]) → deque([1, 2, 3, 4])```
  - extendleft(iterable): 왼쪽에 iterable 원소들을 **역순으로** 추가
  
    ```deque([3, 4]).extendleft([1, 2]) → deque([2, 1, 3, 4])```
  - rotate(n) 
    - `n > 0`: 오른쪽으로 n칸 회전  
    - `n < 0`: 왼쪽으로 n칸 회전  
    ```deque([1, 2, 3]).rotate(1) → deque([3, 1, 2])```
  - index(x): 왼쪽부터 찾아 `x`의 인덱스를 반환, 없으면 `ValueError` 발생
  - count(x): `x`의 등장 횟수를 반환
  - maxlen: deque 생성 시 최대 길이를 지정할 수 있으며, 초과할 경우 자동으로 가장 오래된 항목부터 제거  
    ```deque([1, 2, 3], maxlen=3).append(4) → deque([2, 3, 4], maxlen=3)```



### 한번에 선언하기
- [] * N 개인 리스트 생성: `[False] * N`
- 2차원 배열:`[[False] * N for _ in range(N)]`

### 한번에 선언하기 주의 사항
- tuple: tuple은 불변 객체라 변경이 안됨 리스트를 사용할 것
- list 사용 시 주의 사항
  - 아래와 같이 복사할 경우 주소를 복사하게된다.
  - ```dp = [[0, 0]] * (n + 1)```
  - 즉 이럴 경우 한개의 값만 바뀌어도 전체가 바뀌게 된다.
  - 따라서 아래와 같이 객체를 새로 생성해줘야 한다.
  - ```dp = [[0, 0] for _ in range(n + 1)]```
  
---

# 알고리즘 요약

### Big-O
#### N이 1000 일때 반봇 횟수 

| 번호 | 시간 복잡도 | 최대 반복 횟수 (n=1000)   |
|-----|-------------|---------------------|
| 1   | O(log n)    | 7                   |
| 2   | O(n)        | 1000                |
| 3   | O(n log n)  | 10,000 (약 만 이하)     |
| 4   | O(n^2)      | 1,000,000 (백만)      |
| 5   | O(n^3)      | 1,000,000,000 (10억) |

#### 시간 제한이 1초인 경우 적합한 예시

| N의 범위       | 시간 복잡도   | 비고                    |
|---------------|----------|-----------------------|
| 500           | O(N^3)   | N^3가 작은 경우에 적합        |
| 2,000         | O(N^2)   | N^2가 적절한 경우에 가능       |
| 100,000       | O(NlogN) | 정렬이나 우선순위 큐를 활용한 알고리즘 |
| 10,000,000    | O(N)     | 선형 탐색이나 누적 합 등이 적합    |

#### 공간 복잡도
- int a[1000]: 4KB
- int a[1000000]: 4MB
- int a[2000][2000]: 16MB

**천만이 넘어가면 다시 잘못된 것이 아닌지 확인**

---

### Hash
- `key=value` 형식을 갖는다.

### 문자열 처리
- 문자열 단순 구현 (ASCII 순서, 대문자, 소문자 변환)

### Brute Force
- 반복문이나 재귀를 사용하여 가능한 모든 경우를 탐색한다.

---

### 아스키코드 기준
- 숫자 0 ~ 9: 48 ~ 57
- 대문자: 65 ~ 90
- 소문자: 97 ~ 122