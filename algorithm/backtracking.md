
# Backtracking

모든 경우의 수를 확인해야 할 때
- for로는 확인 불가한 경우 (깊이가 달라질 때)

```
def backtrack(상태):
    if 종료조건(상태):
        답 저장/출력
        return
    
    for 선택 in 가능한_모든_선택지:
        if 유망한지(조건검사):   # (Pruning)
            상태에 선택 추가
            backtrack(갱신된 상태)
            상태에서 선택 원복   # undo
```