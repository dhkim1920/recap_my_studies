
## enable.auto.commit = true

- Kafka 기본 설정
- Kafka가 자동으로 주기적으로 offset을 커밋
- 주기 설정: `auto.commit.interval.ms` (기본 5000ms = 5초)
- 프로세스가 죽어도 최근 커밋된 위치부터 재시작 가능
- **단점**: 메시지 실제 처리 여부와 상관없이 커밋 → 중복 처리 위험 존재

## enable.auto.commit = false

- Kafka가 자동으로 커밋하지 않음
- 개발자가 직접 commitSync() 또는 commitAsync() 호출
- **장점**: 메시지 처리 성공 직후 커밋 가능 → Exactly-once 처리 가능
- **단점**: 커밋 누락이나 실패 시 처리 정확성 문제 발생 가능

## commitSync vs commitAsync

| 항목 | commitSync() | commitAsync() |
|:-----|:-------------|:--------------|
| 안정성 | 높음 (재시도 가능) | 낮음 (실패 감지 어려움) |
| 속도 | 느림 (동기 커밋) | 빠름 (비동기 커밋) |
| 실패 감지 | 가능 | 어려움 |
| 추천 상황 | 중요한 데이터 처리 시 | 빠른 응답 필요 시 |

### 참고 CanCommitOffsets

- Spark Streaming이나 Kafka Consumer 사용 시 offset 커밋을 제어하는 메커니즘
- Kafka Consumer에서는 직접 commitSync(), commitAsync() 호출로 수동 커밋 수행

## 주의사항

- 자동 커밋과 수동 커밋 혼용 금지
- 커밋 타이밍을 애매하게 하면 메시지 유실 또는 중복 처리 위험 발생
- 일관된 커밋 전략을 설정하고 유지할 것

## 요약

- `enable.auto.commit=true` ➔ 간편하지만 중복 처리 위험 있음
- `enable.auto.commit=false` ➔ 직접 커밋 관리 ➔ 높은 정확성 확보
