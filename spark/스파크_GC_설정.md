
# Spark에서 Java GC 선택 및 설정 정리

---

## Spark에서 Java GC 선택 가능 여부

- Spark는 JVM 위에서 동작하므로, JVM 옵션으로 GC 종류를 직접 설정할 수 있음
- Executor, Driver 모두 별도로 GC 설정 가능
- 주로 사용하는 방법:
  - `spark.executor.extraJavaOptions`
  - `spark.driver.extraJavaOptions`

---

## GC 종류별 설정 예시

### G1GC 사용
```bash
spark-submit \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC" \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC" \
  --class your.main.Class \
  your-application.jar
```

### CMS GC 사용
```bash
spark-submit \
  --conf "spark.executor.extraJavaOptions=-XX:+UseConcMarkSweepGC" \
  --conf "spark.driver.extraJavaOptions=-XX:+UseConcMarkSweepGC" \
  ...
```

---

## Spark에서 주로 선택하는 GC 종류

| GC 종류 | 특징 | Spark 사용 시 고려사항 |
|:--------|:------|:----------------|
| Parallel GC | Throughput 최적화 | 짧은 GC 시간 필요할 때 |
| CMS GC | 응답시간 최적화 | 지연(latency) 민감한 작업 |
| G1 GC | 최신 GC, 메모리 압축 및 Pause 시간 균형 | 대규모 데이터 처리에 적합 |
| ZGC, Shenandoah | 매우 짧은 Pause 시간 | JDK 11+ 필요, 실험적 사용 가능 |

---

## Spark GC 종류별 추천 설정

| GC 종류 | 추천 JVM 옵션 | 특징 / 목적 |
|:--------|:--------------|:------------|
| Parallel GC | `-XX:+UseParallelGC` | Throughput 최대화 |
| CMS GC | `-XX:+UseConcMarkSweepGC` `-XX:+CMSParallelRemarkEnabled` | 짧은 Stop-the-World |
| G1 GC | `-XX:+UseG1GC` `-XX:MaxGCPauseMillis=200` `-XX:+ParallelRefProcEnabled` | 대규모 데이터 + 안정적 처리 |
| ZGC | `-XX:+UseZGC` | 초저지연, 실험적 사용 (JDK 11 이상) |

---

## G1GC 실전 적용 예제

```bash
spark-submit \
  --conf "spark.executor.memory=8g" \
  --conf "spark.driver.memory=4g" \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+ParallelRefProcEnabled" \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+ParallelRefProcEnabled" \
  --class your.main.Class \
  your-application.jar
```

---

## 추가 Spark 설정 팁 (메모리 관련)

| 설정 | 설명 |
|:-----|:-----|
| `spark.executor.memoryOverhead` | GC 및 네이티브 메모리용 추가 메모리 (권장: 10~20%) |
| `spark.memory.fraction` | Executor Heap 중 Spark 관리 영역 비율 (기본 0.6) |
| `spark.memory.storageFraction` | Spark 관리 메모리 중 Storage 용도 비율 (기본 0.5) |

---

## GC 튜닝할 때 주의사항

- GC 변경만으로 성능 향상 보장 안 됨 → Heap 크기, GC 튜닝 옵션 함께 조정 필요
- 대용량 Executor 사용 시 반드시 G1GC 고려
- CMS는 Old 영역 Full 비용 급증 주의
- ZGC는 Spark 최신버전 + 최신 JDK 필요

---

# 최종 요약

- Spark는 JVM 옵션으로 GC 자유롭게 설정 가능
- 대규모 작업이면 G1GC 추천
- Stop-the-World가 문제면 CMS
- 초저지연이 필요하면 ZGC 고려 (단, 실험적)

---

