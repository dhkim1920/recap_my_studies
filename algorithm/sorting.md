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

# 길이 먼저 그다음 사전순
words = ['banana', 'apple', 'cherry']
sorted_words = sorted(words, key=lambda x: (len(x), x))
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

