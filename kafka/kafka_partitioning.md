# 카프카 파티션 분할 저장 방법

## 키 기반 (권장)
- 같은 키는 항상 같은 파티션에 저장된다. 프로듀서는 **머머2 (murmur) 해시**를 이용해 파티션을 결정한다.
- 특정 파티션을 명시적으로 지정할 수도 있다.

### 자바 예시

``` java
Properties p = new Properties();
p.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker:9092");
KafkaProducer<String,String> producer = new KafkaProducer<>(p, new StringSerializer(), new StringSerializer());

// 같은 key면 항상 같은 파티션
producer.send(new ProducerRecord<>("topicA", "user-42", "{"event":1}"));
producer.send(new ProducerRecord<>("topicA", "user-42", "{"event":2}"));

// 특정 파티션 강제 지정
producer.send(new ProducerRecord<>("topicA", 3, "key", "value"));
```

## 키가 없을 때
- 기본 동작: **스티키 파티셔너**가 적용된다. 한 파티션에 배치를 채운 뒤, 
배치가 가득 차거나 linger.ms가 만료되면 다음 파티션으로 전환한다. (Kafka 2.4+ 기본)
- 라운드로빈을 원할 경우 파티셔너를 교체할 수 있다.

### 라운드로빈 설정
``` java
p.put(ProducerConfig.PARTITIONER_CLASS_CONFIG,
      "org.apache.kafka.clients.producer.RoundRobinPartitioner");
```

## 스파크 구조적 스트리밍에서 카프카로 쓰기
- `key` 컬럼을 지정하면 카프카 기본 파티셔너가 키 해시 기반으로 파티션을 결정한다.
- 키가 없으면 카프카 클라이언트의 스티키 파티셔너 규칙이 적용된다.
- 라운드로빈이 필요하다면 프로듀서 옵션으로 파티셔너를 교체해야 한다.

### PySpark 예시

``` python
(df.selectExpr("CAST(key AS STRING) AS key", "CAST(value AS STRING) AS value")
   .writeStream
   .format("kafka")
   .option("kafka.bootstrap.servers", "broker:9092")
   .option("topic", "topicA")
   .start())
```

## 선택 가이드
- 세션/사용자 단위 정렬·순서 보장이 필요하면 키를 지정한다. (예:userId, orderId)
- 균등 분산이 더 중요하고 순서 제약이 약하면 키 없이 스티키 파티셔너를 사용한다.
- 라운드로빈이 반드시 필요할 경우 파티셔너를 명시적으로 설정한다.

## 요약
- 키 있음: 머머2 해시 → 같은 키는 같은 파티션
- 키 없음: 기본은 스티키, 라운드로빈 원하면 파티셔너 교체

---

## MurmurHash란?

### 정의
- MurmurHash 계열 해시 함수 중 하나이다.
- 빠른 연산 속도와 균등한 분포 특성 때문에 분산 시스템에서 널리 쓰인다.
- 암호학적 보안성은 없고, 균등 분산성이 핵심임 

### Kafka에서 역할
- Kafka 기본 파티셔너(DefaultPartitioner) 동작
  - 키가 있음
    - partition = (murmur2(serializedKey) & 0x7fffffff) % numPartitions 
    - 즉, 직렬화된 키에 Murmur2 해시를 적용 → 음수를 양수로 바꿔줌 → 파티션 개수로 나눈 나머지를 파티션 번호로 사용
    - 따라서, 같은 키는 항상 같은 파티션에 배치됨

## 키가 없을 때는 어떻게 될까?
### RoundRobinPartitioner
- 동작: 메시지를 보낼 때마다 라운드로빈으로 파티션을 바꾼다.
- 특징: 메시지 한 건 단위로 파티션이 분산됨
- 문제: 배치(RecordAccumulator) 효율이 낮아져 네트워크/스토리지 오버헤드가 커질 수 있다.
- Kafka 2.3 이하: 키가 없으면 기본이 라운드로빈이다.

### StickyPartitioner
- 동작: 한 배치 동안은 같은 파티션에 계속 쓰다가, 배치가 가득 차거나 linger.ms 타임아웃이 지나면 다른 파티션으로 전환한다.
- 특징: 메시지 배치 효율이 좋아서 라운드로빈보다 성능이 좋다.
- Kafka 2.4 이상 기본: 키가 없으면 StickyPartitioner를 사용한다.