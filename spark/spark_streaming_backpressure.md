
## Spark Streaming: `spark.streaming.backpressure.enabled` 설정

### 개요

`spark.streaming.backpressure.enabled`는 **Spark Streaming에서 backpressure 기능을 활성화**하는 설정

이 기능은 **수신 속도를 자동 조절**하여, 시스템이 처리할 수 있는 만큼만 데이터를 수신

이를 통해 **지연 최소화** 및 **리소스 과부하 방지**가 가능

---

### 설정 방법

#### SparkConf 사용 시

```scala
val conf = new SparkConf()
  .setAppName("YourApp")
  .set("spark.streaming.backpressure.enabled", "true")
```

#### spark-submit 명령어 사용 시

```bash
spark-submit \
  --conf spark.streaming.backpressure.enabled=true \
  --class YourMainClass \
  your-application.jar
```

---

### 작동 방식

- 백프레셔 기능은 **PID(Proportional-Integral-Derivative) 제어기**를 기반으로 동작합니다.
- 이전 배치의 **처리 시간** 및 **큐 대기 시간(지연)** 을 분석하여,
- **다음 배치의 수신 속도**를 자동으로 조절합니다.

이로 인해 **데이터 폭주 상황에서도 안정적 운영**이 가능하며, 처리 가능한 수준의 속도로 수신을 제한함으로써 시스템 과부하를 예방
