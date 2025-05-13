
# Broker Tuning

## 1. JVM 및 가비지 컬렉션 튜닝

- Kafka는 JVM에서 실행되므로 **GC** 설정이 성능에 영향을 준다.
- Kafka 서버 프로세스는 대량의 오브젝트를 빠르게 생성하고 폐기하는 특성을 가진다.
- **권장 GC 설정**
  - JDK 8 사용 시, `G1GC` 권장
  - 긴 GC 중단을 피하고 예측 가능한 latency 제공
- **메모리 크기 추천**
  - Kafka 브로커는 일반적으로 6GB ~ 8GB heap 메모리 설정을 권장
- **GC 튜닝 주의사항**
  - 너무 큰 힙은 Full GC 유발
  - 너무 작은 힙은 잦은 GC로 성능 저하

## 2. 네트워크 및 I/O 스레드 튜닝

- Kafka는 네트워크 I/O와 디스크 I/O를 통해 데이터를 처리한다. 따라서 해당 값을 적절하게 설정하는게 중요
- `num.network.threads`: 브로커가 요청을 처리하기 위해 사용하는 네트워크 스레드 수 (3 ~ 8개 권장) 
- `num.io.threads`: 디스크 작업을 처리하는 스레드 수 (8 ~ 16개 권장) 
- 기본 원칙: 스레드 수를 늘리면 병렬 처리량 증가, 과도하면 컨텍스트 전환 오버헤드 발생 
- 대량 트래픽/느린 디스크 환경에서는 I/O 스레드 추가 고려 


## 3. ISR 관리 튜닝

- **ISR (In-Sync Replica)** 는 리더와 동기화된 팔로워 복제본 집합
- 장애 복구 및 데이터 무결성 보장을 위해 관리 필요

### 주요 설정
| 항목 | 설명 |
|:---|:---|
| `replica.lag.time.max.ms` | 팔로워가 리더를 따라가지 못할 때 ISR에서 제외하는 최대 지연 시간 |
| `num.replica.fetchers` | 복제를 처리하는 fetcher 스레드 수 (병렬성 증가) |
| `replica.fetch.min.bytes` | 가져올 최소 데이터 크기 |
| `replica.fetch.wait.max.ms` | 데이터 대기 최대 시간 (짧게 유지) |
| `unclean.leader.election.enable` | 비정상 리더 선출 허용 여부 (기본 false) |

- `replica.fetch.wait.max.ms`는 `replica.lag.time.max.ms`보다 짧게 설정
- ISR 상태는 kafka-topics 명령어로 확인 가능
- 브로커 장애 시 ISR 복제본이 자동으로 리더 승격

## 요약
- JVM 튜닝: G1GC 사용, 6 ~ 8GB 힙 메모리 권장, GC 모니터링 필수
- 네트워크/I/O 스레드 튜닝: 적절한 `num.network.threads`, `num.io.threads` 설정
- ISR 튜닝: latency 한계 설정, fetcher 스레드 최적화, unclean leader election 관리

---

## 왜 `replica.fetch.wait.max.ms`는 `replica.lag.time.max.ms`보다 짧게 설정되야 할까?

- Kafka 내부 로직상 팔로워가 리더로부터 데이터를 가져올 때, 데이터가 준비되지 않으면 replica.fetch.wait.max.ms 동안 기다리게 된다. 
그 후에도 데이터를 못가져오면 "지연(lagging)" 상태가 되버린다.
- replica.lag.time.max.ms는 리더가 판단하는 기준이며 "팔로워가 리더로부터 데이터를 얼마나 오래 따라오지 못하면 ISR에서 제외할지"를 결정 하는 시간 설정이다.

### 만약 replica.fetch.wait.max.ms가 replica.lag.time.max.ms보다 크면?
- 팔로워가 데이터를 기다리는 시간이 너무 길어지게된다. 리더는 실제로 느린건지 설정 때문에 느린건지 알수가 없다.
- 결과적으로 ISR 상태 감지가 지연되고 이는 장애 복구 지연을 야기한다.

### 설정의 예시
- `replica.fetch.wait.max.ms = 500ms` 충분히 짧게 주자
- `replica.lag.time.max.ms = 10000ms` 10초나 기달렸는데 안왔으니 제외

## 참고 문헌
- https://docs.cloudera.com/runtime/7.3.1/kafka-performance-tuning/topics/kafka-tune-broker-tuning-jvm.html
- https://docs.cloudera.com/runtime/7.3.1/kafka-performance-tuning/topics/kafka-tune-broker-tuning-network-io.html
- https://docs.cloudera.com/runtime/7.3.1/kafka-performance-tuning/topics/kafka-tune-broker-tuning-isr.html