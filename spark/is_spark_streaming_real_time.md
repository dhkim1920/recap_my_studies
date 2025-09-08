# Spark Streaming은 실시간일까?

## Spark Streaming (DStream 기반)
- Spark Streaming은 실시간 입력 데이터를 수신하여 **micro-batch**로 나눈 후 처리한다.
- 이로 인해 100ms 수준의 latency가 발생한다.

## Structured Streaming
- Structured Streaming은 Spark의 최신 스트리밍 엔진이다.
- Spark 2.3부터는 **Continuous Processing** 모드가 도입되어 약 **1ms의 낮은 지연 시간**과 **at-least-once** 내결함성을 제공한다.
  - 그러나 Continuous Processing 모드는 아직 **실험** 상태이다. (3.5.5 에서도 아직 실험 상태)
  - spark 공식 페이지 참고: https://spark.apache.org/docs/preview/streaming/performance-tips.html#continuous-processing

## 결론
- **micro-batch 기반의 빠른 처리**를 제공한다.
- 따라서 Spark Streaming은 **진정한 실시간(event-by-event) 처리라고는 볼수 없다.**

## 참고
- 실시간 처리 엔진은 Flink를 고려할 수 있다.


