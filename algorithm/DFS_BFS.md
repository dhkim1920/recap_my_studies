# DFS, BFS
- 특정 개체 찾기에 적합하다.
- 경로 탐색, 네트워크 유형, 조합 유형
- DFS: 재귀/스택 사용, 검증이 쉽고 빠름
- BFS: 큐/링크드리스트 사용
## 1. DFS (재귀 기반)

```python
def dfs(graph, v, visited):
    visited[v] = True
    print(v, end=' ')

    for i in graph[v]:
        if not visited[i]:
            dfs(graph, i, visited)

dfs(target_graph, 1, [False] * 9)
```

**특징**
- 코드 간결, 직관적
- 깊이 제한 이슈 (`RecursionError`) 발생 가능 (약 1000번 호출 시)
- 재귀 호출 스택에 의해 스택 오버플로우 위험
- 백트래킹 문제도 dfs로 풀수 있다. 조건이 안맞으면 더 깊게 탐색 안하고 다른 경로로 넘어감

---

## 2. DFS (스택 기반)

```python
def dfs_stack(graph, v, visited):
    stack = deque([v])
    
    while stack:
        current = stack.pop()
        
        if not visited[current]:
            visited[current] = True
            print(current, end=' ')
            
            for i in reversed(graph[current]):
                if not visited[i]:
                    stack.append(i)

dfs_stack(target_graph, 1, [False] * 9)
```

**특징**
- 스택을 직접 사용해 반복문으로 구현
- 재귀 없이 깊이 우선 탐색 가능
- 스택 오버플로우 문제 없음

---

## 3. BFS (큐 기반)

```python
def bfs(graph, start, visited):
    queue = deque([start])
    visited[start] = True

    while queue:
        v = queue.popleft()
        print(v, end=' ')
        for i in graph[v]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True

bfs(target_graph, 1, [False] * 9)
```

**특징**
- 큐를 사용하여 너비 우선 탐색
- 가까운 노드부터 차례대로 탐색
- 최단 경로 탐색에 주로 사용 
  - 시작점에서부터 가까운 노드들을 순서대로 탐색하기 때문에, 목적지에 도착했을 때의 거리가 항상 최단 거리이기 때문
  - 모든 이동 비용이 동일한 경우(예: 백준 1697 숨바꼭질) BFS가 최단 거리를 보장

---

## 팁
- 노드 값이 작은거 부터 처리하는 방법
  - ```python
    for i in range(1, N + 1):
        graph[i].sort()
    ```
    위와 같이 대상 그래프를 정렬하면된다.

---

## BFS 기반 감염 전파 알고리즘

### 기본 BFS
- 무가중치 그래프에서 전파 시간이 **1단계마다 동일할 때** 사용한다.
- Queue 자료구조를 활용하여 레벨 단위로 탐색한다. (BFS 기반이니까)
- 감염 전파 문제에서는 “초기 감염자(시작점)”을 큐에 넣고, 한 단계씩 감염을 확산시키며 **최단 감염 시간**을 구하는 방식이다.

### 다중 시작점 BFS
- 여러 개의 초기 감염자가 있을 경우, 이들을 모두 큐에 넣고 시작하면 된다.
- 전파는 동시에 일어나므로 레벨 단위로 퍼져나가는 과정에서 거리 배열(감염 시간)을 갱신한다.

```python
from collections import deque

def bfs_multi_source(n, adj, sources):
    INF = 10**9
    dist = [INF] * n
    dq = deque()
    for s in sources:
        dist[s] = 0
        dq.append(s)
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if dist[v] == INF:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist
```

### 참고) BFS 외 다른 전파 모델
- 아래 케이스들은 기본 감염전파보다 어려운 케이스다.
- **다익스트라 (가중치 전파)**: 간선마다 감염 지연 시간이 다를 때 사용하며, BFS 대신 최소 힙 기반 우선순위 큐를 활용한다.
- **임계값 모델 (부트스트랩 퍼콜레이션, 소문 문제)**: 일정 수 이상의 이웃이 감염되었을 때만 감염시킨다. BFS 변형으로 카운트 관리가 필요하다.
- **확률 기반 모델 (Independent Cascade, Linear Threshold)**: 간선마다 전파 확률이 있거나, 이웃의 영향 합이 임계값을 넘으면 감염시킨다. 주로 시뮬레이션

