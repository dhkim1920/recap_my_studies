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
- 절댓값: `abs(x)`
- 최대공약수: `math.gcd(a, b)`
- 최소공배수: `math.lcm(a, b)`
- 제곱근: `math.sqrt(x)`

### 양방향 큐 (Deque)
- `from collections import deque`
- DFS, BFS에서 사용하기 좋음

### 한번에 선언하기
- [] * N 개인 리스트 생성: `[False] * N`
- 2차원 배열:`[[False] * N for _ in range(N)]`


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

### Greedy
- 현재의 선택만 고려한다. (미래 선택에 영향을 주지 않음)
- 현재의 최적해를 선택, 따라서 항상 최적의 해를 보장하지 않음
- 주로 문제의 제약이 있다.
- 최적 부분 구조 조건을 갖는다.
- 보통 정렬을 잘하면 해결된다.

### DFS, BFS
- 특정 개체 찾기에 적합하다.
- 경로 탐색, 네트워크 유형, 조합 유형
- DFS: 재귀/스택 사용, 검증이 쉽고 빠름
- BFS: 큐/링크드리스트 사용

### DP
- 수행 시간을 단축할 때 사용한다.
- DFS, BFS로 풀다 경우의 수가 너무 많은 경우 사용
- 중복 연산이 많은 경우 사용한다.
- 두 가지 방식이 있다.
  - Top-Down: 재귀/메모이제이션
  - Bottom-Up: 반복문/테이블 구성


### Hash
- `key=value` 형식을 갖는다.

### 문자열 처리
- 문자열 단순 구현 (ASCII 순서, 대문자, 소문자 변환)

### Brute Force
- 반복문이나 재귀를 사용하여 가능한 모든 경우를 탐색한다.

