
## JavaInputDStream<ConsumerRecord<K, V>> stream

- Spark Streaming에서 Kafka 같은 외부 데이터 소스에서 스트리밍 데이터를 읽어오는 DStream
- JavaInputDStream은 RDD가 시간마다 생성되는 스트림 데이터 구조
- JavaInputDStream<ConsumerRecord<K, V>> 형태로 Kafka 메시지를 수신
- 각 배치마다 하나의 RDD 생성
- ConsumerRecord 안에 key(), value(), partition(), offset() 등의 정보 포함

## 예시
```java
JavaInputDStream<ConsumerRecord<String, String>> stream = 
    KafkaUtils.createDirectStream(...);
```
---

## KafkaUtils.createDirectStream

- Spark Streaming에서 Kafka 데이터를 읽어오는 Direct 방식 스트림 생성 메서드
- 내부적으로 KafkaConsumer API를 사용해 offset 관리와 fetch를 직접 수행
- Zookeeper 없이 Kafka 브로커와 직접 통신

### 주요 특징

- Exactly-once 처리 가능 (정확히 한번만 처리)
- 수동 offset 관리 가능 (commitAsync, commitSync)
- 복잡한 소비자 그룹/리밸런싱 문제를 줄일 수 있음---

### 주요 파라미터

- StreamingContext
- Kafka Consumer 설정(Map)
- 주제(Topic) 목록
- 위치 전략(LocationStrategies)
- 소비 전략(ConsumerStrategies)

### 예시
```java
JavaInputDStream<ConsumerRecord<String, String>> stream = 
    KafkaUtils.createDirectStream(
        streamingContext,
        LocationStrategies.PreferConsistent(),
        ConsumerStrategies.Subscribe(Arrays.asList("topic1"), kafkaParams)
    );
```

---
## LocationStrategies and ConsumerStrategies

### LocationStrategies

- Kafka Partition을 Spark Executor에 어떻게 배치할지 결정하는 전략
- 데이터 이동 최소화를 목표로 함

| 전략 | 설명 |
|:-----|:-----|
| PreferConsistent | 모든 Executor에 균등하게 파티션 분배 (일반적) |
| PreferBrokers | Kafka 브로커가 Executor와 함께 실행될 때 최적 |
| PreferFixed | 특정 Executor에 고정 분배 |

#### 예시
```java
LocationStrategies.PreferConsistent()
```

### ConsumerStrategies

- Kafka Consumer 설정을 기반으로 어떤 방식으로 토픽을 구독할지 결정하는 전략

| 전략 | 설명 |
|:-----|:-----|
| Subscribe(topics, kafkaParams) | 주어진 토픽 목록을 구독 (일반적) |
| SubscribePattern(pattern, kafkaParams) | 정규 표현식으로 토픽 구독 |
| Assign(partitions, kafkaParams) | 특정 파티션을 명시적으로 구독 |

#### 예시
```java
ConsumerStrategies.Subscribe(Arrays.asList("topic1", "topic2"), kafkaParams)
```

### 요약

| 항목 | LocationStrategies | ConsumerStrategies |
|:-----|:-------------------|:-------------------|
| 목적 | 파티션과 Executor 매칭 최적화 | 어떤 토픽(또는 파티션)을 읽을지 결정 |
| 대표 방식 | PreferConsistent | Subscribe |
