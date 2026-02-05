# JavaRDD

- Apache Spark의 Java용 RDD(Resilient Distributed Dataset) 클래스
- Spark Core의 가장 중요한 데이터 구조로 내부적으로 Scala의 RDD<T>를 Java-friendly하게 감쌈

## 주요 특징

| 항목 | 설명                                |
|:-----|:----------------------------------|
| 분산 데이터셋 | 클러스터의 여러 노드에 나누어 저장               |
| 불변성(Immutable) | RDD는 한번 생성하면 변경할 수 없음             |
| Lazy 연산 | 트랜스포메이션에서는 바로 실행되지 않고, 액션 호출 시 실행 |
| 타입 안정성 | 컴파일 시점에 타입 체크 가능 (JavaRDD<T>)     |
| 장애 복구 | 데이터 손실 시 lineage(변환 이력)을 따라 복구 가능 |

## 주요 연산

| 연산 종류 | 설명 | 예시 메서드 |
|:----------|:-----|:-----------|
| Transformation | 새로운 RDD 생성 | map, filter, flatMap, union, distinct |
| Action | 결과 반환 또는 저장 | collect, count, saveAsTextFile, reduce |

## 생성 예시

```java
List<Integer> data = Arrays.asList(1, 2, 3, 4, 5);
JavaRDD<Integer> rdd = jsc.parallelize(data);
```

```java
JavaRDD<String> fileRdd = jsc.textFile("hdfs://path/to/file.txt");
```

## 기본 사용 흐름

1. JavaRDD 생성 (parallelize, 파일 읽기 등)
2. Transformation 적용 (map, filter 등)
3. Action으로 결과 확인 또는 저장 (collect, saveAsTextFile 등)

```java
JavaRDD<Integer> rdd = jsc.parallelize(Arrays.asList(1, 2, 3, 4, 5));
JavaRDD<Integer> squared = rdd.map(x -> x * x);
List<Integer> result = squared.collect(); // [1, 4, 9, 16, 25]
```

## 요약

- JavaRDD는 분산 저장 + 불변성 + Lazy Evaluation을 가진 Java 전용 RDD 클래스
- 주로 RDD 연산(map, filter 등)을 Java 코드로 작성할 때 사용

---

## JavaRDD vs JavaPairRDD

| 항목 | JavaRDD | JavaPairRDD |
|:-----|:--------|:------------|
| 데이터 형태 | 단일 값 (T) | (키, 값) 쌍 (Tuple2<K, V>) |
| 사용 목적 | 일반 데이터 처리 | Key-Value 기반 데이터 처리 |
| 주요 메서드 | map, filter, flatMap, union 등 | groupByKey, reduceByKey, join, cogroup 등 |
| 변환 방법 | - | JavaRDD를 mapToPair()로 변환 가능 |

## JavaPairRDD 간단 예시

```java
JavaRDD<String> lines = jsc.textFile("hdfs://path/to/file.txt");

// 각 라인별 (단어, 1) 형태로 변환
JavaPairRDD<String, Integer> pairs = lines.flatMap(line -> Arrays.asList(line.split(" ")).iterator())
    .mapToPair(word -> new Tuple2<>(word, 1));

// 단어별 개수 세기
JavaPairRDD<String, Integer> counts = pairs.reduceByKey((a, b) -> a + b);
```

## 요약

- JavaRDD는 하나의 타입(T) 데이터를 다룸
- JavaPairRDD는 (K, V) 형태로 데이터를 다룸 (Key 중심 연산 가능)
- JavaRDD를 mapToPair()로 변환해 JavaPairRDD 생성 가능
