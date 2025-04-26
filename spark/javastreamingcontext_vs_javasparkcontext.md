
# JavaStreamingContext vs JavaSparkContext

## JavaStreamingContext

- Spark Streaming 애플리케이션의 진입점
- StreamingContext(Scala)를 Java-friendly하게 감싼 클래스
- **실시간 스트리밍 데이터 처리(DStream) 전용**
- 배치 간격(Durations) 설정 필요
- 주요 메서드: start(), stop(), awaitTermination()

### foreachRDD

- Spark Streaming에서 DStream에 적용하는 Transformation 메서드
- 각 배치(batch)마다 생성된 RDD를 하나씩 가져와서 처리할 때 사용

### 주요 특징

| 항목 | 설명 |
|:-----|:-----|
| 동작 대상 | DStream 안에서 생성되는 매 배치의 RDD |
| 호출 시점 | 배치가 끝날 때마다 자동 호출 |
| 목적 | RDD 저장, DB 적재, 외부 시스템 전송 등 출력(Output)용 작업 수행 |
| 결과 | 반환값 없음 (void), 주로 사이드 이펙트 발생 |

### 기본 형태

```java
dstream.foreachRDD(rdd -> {
    // rdd에 대해 작업 수행
    rdd.foreach(record -> {
        System.out.println(record);
    });
});
```

### 주요 사용 예시

- RDD를 파일로 저장 (`saveAsTextFile`)
- Kafka, 데이터베이스, Redis 등에 결과 전송
- 통계 계산 후 외부 저장
- 다른 Spark Job 호출

```java
dstream.foreachRDD(rdd -> {
    if (!rdd.isEmpty()) {
        rdd.saveAsTextFile("hdfs://path/to/output");`
    }
});
```

### 주의사항

- RDD가 비어있을 수 있으므로 `isEmpty()` 체크하는 것이 좋음
- 외부 시스템에 전송할 때는 병렬성을 고려해서 적절히 batch 처리 필요
- 드라이버 프로그램에서 직접 작업하지 말고, RDD 안에서 worker들이 작업하게 해야 함

---

## JavaSparkContext

- 일반 Spark 애플리케이션의 진입점
- SparkContext(Scala)를 Java-friendly하게 감싼 클래스
- **정적 데이터 처리(RDD) 전용**
- 파일, 리스트 같은 고정 데이터 처리
- 주요 메서드: parallelize(), textFile(), collect()

## 비교

| 항목 | JavaStreamingContext | JavaSparkContext |
|:-----|:---------------------|:-----------------|
| 목적 | Streaming 데이터 처리 | RDD 정적 데이터 처리 |
| 기반 | StreamingContext | SparkContext |
| 다루는 데이터 | DStream | RDD |
| 생성 시 설정 | 배치 주기 설정 필요 | 없음 |
| 처리 방식 | 지속적으로 들어오는 데이터 처리 | 정해진 데이터만 한번 처리 |
| API 스타일 | 스트리밍 전용 API | 일반 RDD API |
| 주요 메서드 | start(), stop(), awaitTermination() | collect(), saveAsTextFile() |

## 포함 관계

- `JavaStreamingContext` 내부에는 `JavaSparkContext`가 포함되어 있음
- 즉, 스트리밍 작업 중 RDD 작업이 필요하면 `sparkContext()`로 `JavaSparkContext`를 꺼내서 사용 가능

```java
JavaStreamingContext jssc = new JavaStreamingContext(conf, Durations.seconds(5));
JavaSparkContext jsc = jssc.sparkContext(); // StreamingContext 안의 SparkContext 접근
```

- `JavaSparkContext`는 독립적으로 사용할 수 있지만
- `JavaStreamingContext`는 내부적으로 `JavaSparkContext`를 항상 가지고 있음

---

## 요약

- **JavaSparkContext** → RDD 처리용 (정적 데이터)
- **JavaStreamingContext** → DStream 처리용 (실시간 데이터)  
  (안에 **JavaSparkContext를 포함**하고 있음)
