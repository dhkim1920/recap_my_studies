# DP
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
