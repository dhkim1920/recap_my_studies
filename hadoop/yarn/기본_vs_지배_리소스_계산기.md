# DefaultResourceCalculator 와 DominantResourceCalculator의 차이

## DefaultResourceCalculator

- **계산 기준:** 메모리만 고려
- **특징:**
  - 컨테이너 할당 시 메모리 사용량만을 기준으로 스케줄링
  - CPU(vCore)는 고려하지 않음
  - CPU 리소스가 비효율적으로 사용될 수 있음
- **적합한 경우:**
  - 작업이 메모리 집약적이고 CPU 사용량이 낮은 경우
  - 단일 리소스(메모리)만 관리하는 간단한 클러스터 환경
- **문제점:**
  - Spark-submit에서 설정한 executor-cores, num-executors가 무시될 수 있음
  - Executor에 vCore가 비정상적으로 많이 할당되어 성능 저하 발생 가능

## DominantResourceCalculator

- **계산 기준:** 메모리와 CPU 모두 고려
- **특징:**
  - Dominant Resource Fairness(DRF) 모델을 기반으로, 사용자/애플리케이션의 주요 리소스 사용률을 공정하게 분배
  - CPU 집약적 작업과 메모리 집약적 작업이 공존하는 경우에도 효율적으로 리소스 분배
- **적합한 경우:**
  - 다양한 리소스 유형(CPU, 메모리 등)을 사용하는 복잡한 작업이 많은 환경
  - 리소스의 공정한 분배와 효율적인 사용이 중요한 경우
- **장점:**
  - Spark-submit에서 지정한 executor-cores, num-executors가 정상적으로 반영됨
  - 전체 클러스터 자원을 균형 있게 활용할 수 있음

## 요약 비교

| 항목 | DefaultResourceCalculator | DominantResourceCalculator |
|:---|:---|:---|
| 기준 | 메모리만 고려 | 메모리 + CPU 모두 고려 |
| 리소스 분배 모델 | 단순 메모리 기반 | Dominant Resource Fairness (DRF) |
| 적합 환경 | 메모리 위주 작업 | CPU, 메모리 혼재 작업 |
| Spark-submit 영향 | executor-cores 무시 가능성 있음 | executor-cores 정상 반영 |
| 리스크 | CPU 자원 낭비 가능성 | 다양한 리소스 공정 사용 |

## 설정 변경 방법 (예시)

```xml
<property>
  <name>yarn.scheduler.capacity.resource-calculator</name>
  <value>org.apache.hadoop.yarn.util.resource.DominantResourceCalculator</value>
</property>
