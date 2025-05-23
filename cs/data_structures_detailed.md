## 자료구조

### 자료구조의 큰 그림
- **시간 복잡도**와 **공간 복잡도**를 기준으로 자료구조 선택
- 알고리즘 설계에서 핵심적인 역할 수행
- 데이터의 삽입, 삭제, 탐색, 순회 성능을 고려하여 선택

---

### 주요 자료구조

#### Array
- 고정 크기 메모리 블록, 인덱스를 통한 직접 접근 (O(1))
- 삽입/삭제는 중간 위치일 경우 O(n) 시간 소요
- 사용 예시: 정렬된 리스트, 인덱스 기반 조회

#### Linked List
- 각 노드가 다음 노드를 가리키는 포인터 구조
- 삽입/삭제는 O(1), 탐색은 O(n)
- 단일 연결 리스트, 이중 연결 리스트, 원형 연결 리스트 존재

#### Stack
- 후입선출 구조 (LIFO)
- push/pop 모두 O(1)
- 함수 호출 스택, 웹 브라우저 방문 기록 등에 사용

#### Queue
- 선입선출 구조 (FIFO)
- enqueue/dequeue 모두 O(1)
- 응용: 작업 대기열, BFS 탐색

- **변형 큐**: 
  - 원형 큐(Circular Queue)
  - 우선순위 큐(Priority Queue)
  - 덱(Deque: Double Ended Queue)

#### Hash Table
- 해시 함수를 이용한 키-값 저장 구조
- 평균 O(1), 최악의 경우 O(n) (충돌 시)
- 충돌 해결 방법:
  - **체이닝**: 같은 해시에 연결 리스트로 연결
  - **오픈 어드레싱**: 빈 공간 탐색 (선형/제곱/이중 해싱)

#### Tree
- 계층적 자료 표현 구조
- **이진 탐색 트리(BST)**: 정렬된 구조, 평균 탐색/삽입/삭제 O(log n)
- **AVL 트리**: BST + 균형 유지
- **힙(Heap)**: 우선순위 큐 구현용, 최대 힙/최소 힙
- **B-Tree, B+Tree**: 데이터베이스, 파일 시스템에서 활용

#### Graph
- 정점(Vertex)과 간선(Edge)으로 구성
- **인접 행렬** vs **인접 리스트** 표현
- **BFS, DFS**: 그래프 순회
- **최단 경로**: 다익스트라, 벨만포드
- **최소 신장 트리**: 크루스칼, 프림 알고리즘
