
# StreamingJobProgressListener

- Spark Streaming 전용 내부 모니터링 클래스
- DStream 작업의 진행 상황(progress)을 실시간으로 모니터링하고 기록

## 주요 역할

| 항목 | 설명 |
|:-----|:-----|
| Batch 모니터링 | 각 배치(batch)의 상태(Started, Completed, Failed 등) 추적 |
| Job 상태 기록 | Job이 성공했는지 실패했는지 저장 |
| 통계 제공 | Input rate, Processing time, Scheduling delay 등 계산 |
| UI 제공 | Spark Streaming Web UI (/streaming) 데이터 공급자 역할 |

## 주요 메서드

| 메서드 | 설명 |
|:-------|:-----|
| onBatchSubmitted() | 새로운 배치가 생성될 때 호출 |
| onBatchStarted() | 배치 처리가 시작될 때 호출 |
| onBatchCompleted() | 배치 처리가 끝났을 때 호출 |
| onOutputOperationStarted() | Output 연산 시작 시 호출 |
| onOutputOperationCompleted() | Output 연산 완료 시 호출 |
| numUnprocessedBatches() | 아직 처리되지 않은 배치 수 반환 |

## 내부 구조 흐름

1. Spark Streaming 애플리케이션이 실행되면
2. 각 배치가 생성될 때마다 StreamingJobProgressListener가 이벤트를 감지
3. 상태 정보를 업데이트하고 Spark UI /streaming 탭에 반영
