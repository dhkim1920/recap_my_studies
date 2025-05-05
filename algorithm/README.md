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

### 수학
- 절댓값: `abs(x)`
- 최대공약수: `math.gcd(a, b)`
- 최소공배수: `math.lcm(a, b)`
- 제곱근: `math.sqrt(x)`
- 조합: `math.comb(n, r)`
  - 조합 = 선택만, 무작위
- 순열: `math.perm(n, r)`
  - 선택 + 나열
- 소인수 분해
  - 2, 3, 5, 7, 11, 13 등 소수로 먼저 나누어 본다.
  - A의 약수: `A = a^m * b^n`
  - A약수의 개수: `(m+1) * (n+1)`

### 양방향 큐 (Deque)
- `from collections import deque`
- DFS, BFS에서 사용하기 좋음

### 한번에 선언하기
- [] * N 개인 리스트 생성: `[False] * N`
- 2차원 배열:`[[False] * N for _ in range(N)]`

### 한번에 선언하기 주의 사항
- tuple: tuple은 불변 객체라 변경이 안됨 리스트를 사용할 것
- list 사용 시 주의 사항
  - 아래와 같이 사용할 경우 얕은 복사가 이루어 짐
  - ```dp = [[0, 0]] * (n + 1)```
  - 즉 이럴 경우 한개의 값만 바뀌어도 전체가 바뀌게 됨
  - 따라서 아래와 같이 깊은 복사랄 이용해 복사해야 함
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
---
### DP
- 수행 시간을 단축할 때 사용한다.
- DFS, BFS로 풀다 경우의 수가 너무 많은 경우 사용
- 중복 연산이 많은 경우 사용한다.
- 두 가지 방식이 있다.
  - Top-Down: 재귀/메모이제이션
  - Bottom-Up: 반복문/테이블 구성

#### <u>1차원 압축 (Knapsack 최적화)</u>

#### 언제 사용하나
- 배낭 문제(0-1 Knapsack) 계열에서 사용
- DP[i][w] 형태에서 이전 줄만 사용하는 경우, 따라서 공간을 절약 가능

#### 왜 가능한가
점화식이 아래와 같은 구조일 때
```commandline
dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight[i]] + value[i])
# dp[i]는 dp[i-1]만 참조하므로, 1차원 배열로 압축 가능
```

#### 구현 방법
역순 루프를 이용하여 같은 아이템이 중복 선택되지 않도록 함

예시 코드)
```python
for weight, value in items:
    for w in range(W, weight - 1, -1):
        dp[w] = max(dp[w], dp[w - weight] + value)
```

#### 시간과 공간 복잡도
시간 복잡도: O(NW)
공간 복잡도: O(W)


#### <u>모노톤 큐 최적화</u>

#### 언제 사용하나
- 슬라이딩 윈도우에서 최솟값 혹은 최댓값을 빠르게 찾을 때
- 또는 dp[i] = min(dp[j] + cost[j][i]) 구조이고 cost가 단조성을 가질 때

#### 아이디어
- deque을 사용하여 슬라이딩 범위 내에서 쓸모없는 값 제거
- 항상 deque의 앞에는 최솟값이 위치하도록 유지

#### 슬라이딩 윈도우 최소값 예시
```python
from collections import deque

a = [3, 1, 2, 4, 6, 2, 1]
k = 3
dq = deque()

for i in range(len(a)):
    while dq and dq[0] <= i - k:
        dq.popleft()
    while dq and a[dq[-1]] >= a[i]:
        dq.pop()
    dq.append(i)
    if i >= k - 1:
        print(a[dq[0]])
```

#### 시간 복잡도
O(n), 각 원소는 deque에 최대 1번 삽입, 1번 제거


#### <u>크누스 최적화 (Knuth Optimization)</u>
**※ 누적합 문제에서 사용 가능, 항상 사용가능한건 아니니 확인 필요**<br>
크누스 최적화는 시간복잡도 O(n^3)의 DP 문제를 O(n^2)으로 줄여줄 수 있는 DP 최적화 방법

#### 조건
아래의 조건이 만족해야만 사용 가능
1. 점화식 형태
```commandline
DP[i][j] = min(DP[i][k] + DP[k+1][j] + C[i][j])  
# 단, i ≤ k < j
```
2. C[i][j]가 Monge Array일 것

#### Monge Array란?
n x m 크기의 행렬 C에 대해, 모든 1 ≤ a < b ≤ n, 1 ≤ c < d ≤ m에 대해 아래의 조건이 성립해야함
```commandline
C[a][c] + C[b][d] ≤ C[a][d] + C[b][c]
# 또한 다음 조건도 함께 만족해야 한다.
C[a][d] ≥ C[b][c]  (단, a ≤ b ≤ c ≤ d)
# 여기서 C[i][j]는 i번째 행, j번째 열의 원소를 의미한다.
```

#### 본론

DP[i][j]를 계산할 때 최적의 k를 저장하는 배열을 opt[i][j]라고 하고  
최적 k가 여러 개 존재할 경우, 가장 왼쪽 값을 저장

opt[i][j]는 다음 관계를 만족한다.
```commandline
opt[i][j-1] ≤ opt[i][j] ≤ opt[i+1][j]
```
이때 opt[i+1][j] - opt[i][j-1]의 범위가 매우 작기 때문에  
점화식 k를 선택하는 과정이 상수 시간에 처리며 시간복잡도는 O(n^2)가 됨

---

# 정렬 알고리즘 정리

## 선택 정렬 (Selection Sort)

- 가장 작은 데이터를 찾아 맨 앞 데이터와 교체
- 코드:

```python
for i in range(len(arr)):
    min_idx = i
    for j in range(i + 1, len(arr)):
        if arr[min_idx] > arr[j]:
            min_idx = j
    arr[i], arr[min_idx] = arr[min_idx], arr[i]
```

- **시간 복잡도:** O(n²)
- **특징:** 느리지만, "가장 작은 데이터 찾기"가 필요한 경우에 사용됨

## 삽입 정렬 (Insertion Sort)

- 적절한 위치에 삽입
- 첫 번째 원소는 정렬되어 있다고 가정, 두 번째 원소부터 시작
- 코드:

```python
for i in range(1, len(arr)):
    for j in range(i, 0, -1):
        if arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
        else:
            break
```

- **시간 복잡도:** 평균 O(n²), 최선(거의 정렬된 상태) O(n)
- **특징:** 거의 정렬된 상태라면 매우 빠름 → 퀵정렬보다 유리할 수 있음

## 퀵 정렬 (Quick Sort)

- 기준 데이터(피벗)를 정하고, 작은 값과 큰 값으로 분할하여 재귀적으로 정렬
- 피벗 선택 방법:

| 방법 | 장점 | 단점 |
|:----|:----|:----|
| 첫 번째 | 구현 쉬움 | 정렬된 데이터에 최악 |
| 마지막 | 구현 쉬움 | 정렬된 데이터에 최악 |
| 가운데 | 무난함 | 편향 가능성 |
| 랜덤 | 평균적 성능 우수 | 랜덤 호출 비용 발생 |
| Median-of-Three | 정렬된 데이터에도 강함 | 비교 연산 추가됨 |

- 기본 코드:

```python
def quick_sort(arr, start, end):
    if start >= end:
        return
    
    pivot = start
    left = start + 1
    right = end
    
    while left <= right:
        while left <= end and arr[left] <= arr[pivot]:
            left += 1
        while right > start and arr[right] > arr[pivot]:
            right -= 1
        if left > right:
            arr[right], arr[pivot] = arr[pivot], arr[right]
        else:
            arr[left], arr[right] = arr[right], arr[left]
    
    quick_sort(arr, start, right - 1)
    quick_sort(arr, right + 1, end)
```

- **시간 복잡도:** 평균 O(n log n), 최악 O(n²)
- **특징:** 이미 정렬된 데이터에 매우 취약

## 계수 정렬 (Counting Sort)

- 데이터 개수(N)와 최댓값(K)이 작을 때 사용
- 데이터 크기를 인덱스로 사용하는 리스트를 선언하고 개수만큼 카운트
- **시간 복잡도:** O(N + K)
- **공간 복잡도:** O(K)

- 특징:
  - 데이터 크기가 한정적이어야 함
  - 데이터가 많이 중복될 때 유리
  - 데이터가 희박하면 (ex: 0과 999999만 있음) 비효율적

## 파이썬 정렬 라이브러리

- `sort()`: 리스트 객체의 메서드, 원본 리스트를 직접 정렬
- `sorted()`: 정렬된 새 리스트를 반환, 원본은 유지

- 기본적으로 **Timsort 알고리즘** 사용  
  (삽입 정렬 + 병합 정렬을 합친 하이브리드)

### sorted() 사용 예시

```python
# 길이를 기준으로 정렬
words = ['banana', 'apple', 'cherry']
sorted_words = sorted(words, key=len)
print(sorted_words)  # ['apple', 'banana', 'cherry']

# 튜플 리스트를 두 번째 값 기준으로 정렬
arr = [(1, 3), (2, 2), (3, 1)]
sorted_arr = sorted(arr, key=lambda x: x[1])
print(sorted_arr)  # [(3, 1), (2, 2), (1, 3)]
```

### sort() 사용 예시

```python
# 길이를 기준으로 원본 리스트 정렬
words = ['banana', 'apple', 'cherry']
words.sort(key=len)
print(words)  # ['apple', 'banana', 'cherry']

# 튜플 리스트를 두 번째 값 기준으로 원본 리스트 정렬
arr = [(1, 3), (2, 2), (3, 1)]
arr.sort(key=lambda x: x[1])
print(arr)  # [(3, 1), (2, 2), (1, 3)]
```

### 정리 요약

| 함수 | 원본 변경 여부 | key 사용 가능 여부 |
|:----|:--------------|:------------------|
| `sort()` | 원본 변경 | 가능 |
| `sorted()` | 새 리스트 반환 | 가능 |

## 정렬 문제 접근법

1. **정렬 라이브러리로 풀 수 있는 문제**  
   → `sort()`, `sorted()` 사용

2. **정렬 알고리즘 원리를 물어보는 문제**  
   → 선택 정렬, 삽입 정렬, 퀵 정렬 개념 및 코드 숙지

3. **더 빠른 정렬이 필요한 문제**  
   → 계수 정렬 같은 특수 알고리즘 사용 고려


---

### Hash
- `key=value` 형식을 갖는다.

### 문자열 처리
- 문자열 단순 구현 (ASCII 순서, 대문자, 소문자 변환)

### Brute Force
- 반복문이나 재귀를 사용하여 가능한 모든 경우를 탐색한다.

