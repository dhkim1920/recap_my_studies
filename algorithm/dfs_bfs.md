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

---

## 2. DFS (스택 기반)

```python
def dfs_stack(graph, v, visited):
    stack = deque([v])
    visited[v] = True
    print(v, end=' ')

    while stack:
        current = stack[-1]
        for i in graph[current]:
            if not visited[i]:
                stack.append(i)
                visited[i] = True
                print(i, end=' ')
                break
        else:
            stack.pop()

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