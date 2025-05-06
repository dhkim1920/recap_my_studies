# 탐색

## 순차 탐색 (Sequential Search)

* **설명**: 데이터를 앞에서부터 하나씩 차례로 확인
* **시간 복잡도**: O(n)

## 이진 탐색 (Binary Search)

* **설명**:

  * **데이터가 정렬**되어 있어야 사용 가능
  * 시작점, 끝점, 중간점을 이용해 **중간값과 비교**하며 탐색
  * 중간값보다 찾는 값이 작으면 왼쪽, 크면 오른쪽으로 탐색 범위 축소
* **시간 복잡도**: O(log n)
* **코딩 테스트**:

  * 매우 자주 출제됨 (필수 암기)
  * **탐색 범위가 2,000만 이상**이거나,
    **데이터 개수나 값이 1,000만 이상**이면 이진 탐색 고려

### 이진 탐색 코드

* **재귀형**

```python
def binary_search_recursive(arr, target, start, end):
    if start > end:
        return None
    mid = (start + end) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, start, mid - 1)
    else:
        return binary_search_recursive(arr, target, mid + 1, end)
```

* **반복문형**

```python
def binary_search_iterative(arr, target):
    start, end = 0, len(arr) - 1
    while start <= end:
        mid = (start + end) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            end = mid - 1
        else:
            start = mid + 1
    return None
```

---

## 이진 탐색 트리 (Binary Search Tree, BST)

* **규칙**:

  * 왼쪽 자식 < 부모 노드 < 오른쪽 자식
  * 왼쪽, 오른쪽 서브트리도 모두 이진 탐색 트리
* **특징**:

  * 각 노드는 최대 두 개의 자식 노드를 가짐
  * 탐색, 삽입, 삭제의 **평균 시간 복잡도**: O(log n)
  * 트리가 한쪽으로 치우치면 **최악의 경우 시간 복잡도**: O(n)
