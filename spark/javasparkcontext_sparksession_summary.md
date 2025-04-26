
## JavaSparkContext

- Apache Spark의 Java용 진입점(Entry Point) 클래스
- Spark 클러스터와 연결하고, RDD를 생성하거나 연산을 시작할 때 사용
- 내부적으로 Scala의 SparkContext를 감싼 Java Wrapper

## 주요 기능

| 기능 | 설명 |
|:-----|:-----|
| 클러스터 연결 | Master URL, Application Name 등을 설정하여 클러스터 연결 |
| RDD 생성 | `parallelize`, `textFile` 등으로 RDD 생성 |
| RDD 연산 시작 | 액션(`collect`, `count`, `saveAsTextFile`) 호출 가능 |
| 리소스 관리 | 작업 종료 시 `stop()` 호출 필요 |

## 생성 예시
```java
SparkConf conf = new SparkConf()
    .setAppName("ExampleApp")
    .setMaster("local[*]");

JavaSparkContext jsc = new JavaSparkContext(conf);
```

## 주요 메서드

| 메서드 | 설명 |
|:-------|:-----|
| `parallelize(List<T>)` | 리스트를 RDD로 변환 |
| `textFile(String path)` | 파일을 읽어 RDD로 변환 |
| `stop()` | SparkContext를 종료하고 리소스 해제 |
| `emptyRDD()` | 비어있는 RDD 생성 |

---

## 요약

- `JavaSparkContext`는 Spark에서 Java 애플리케이션이 클러스터를 제어하는 시작점
- RDD 생성, 작업 실행, 리소스 관리를 담당

---

## JavaSparkContext vs SparkSession

| 항목 | JavaSparkContext | SparkSession |
|:-----|:-----------------|:-------------|
| 도입 시기 | Spark 1.x | Spark 2.x 이후 (권장) |
| 목적 | RDD 기반 연산 진입점 | RDD + DataFrame + Dataset 모든 연산 통합 진입점 |
| API 스타일 | 저수준 (RDD 중심) | 고수준 (DataFrame, SQL 중심) |
| 생성 방법 | `new JavaSparkContext(SparkConf)` | `SparkSession.builder().getOrCreate()` |
| SQL 기능 | 별도 `SQLContext`, `HiveContext` 필요 | SparkSession 하나로 모두 지원 |
| 권장 사용 | RDD 작업만 필요할 때 | DataFrame, SQL, Structured Streaming 포함할 때 |

## 코드 비교

**JavaSparkContext 생성 예시**
```java
SparkConf conf = new SparkConf().setAppName("Example").setMaster("local[*]");
JavaSparkContext jsc = new JavaSparkContext(conf);
```

**SparkSession 생성 예시**
```java
SparkSession spark = SparkSession.builder()
    .appName("Example")
    .master("local[*]")
    .getOrCreate();
```

---

## 요약

- **JavaSparkContext**: Spark 1.x 스타일, RDD 작업 전용
- **SparkSession**: Spark 2.x 이후 통합된 API, RDD + DataFrame + SQL 모두 지원
- 현재는 SparkSession 사용이 표준
