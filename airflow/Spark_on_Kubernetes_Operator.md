## Spark on Kubernetes Operator란?

기존의 `spark-submit` 방식은 일회성 명령에 의존하며 Kubernetes의 선언적(Declarative) 관리 방식을 따르기 어렵다.
**Spark Operator**는 Spark 애플리케이션을 Kubernetes의 **커스텀 리소스(CRD)**로 정의하여, 일반적인 Pod나 Deployment처럼 YAML 파일로 관리하고 모니터링할 수 있게 해주는 도구이다.


### 아키텍처 및 동작 원리

Spark Operator는 Kubernetes의 제어 루프 패턴을 따른다.

1. **사용자 정의**: 사용자가 `SparkApplication` 객체를 YAML로 작성하여 `kubectl apply` 한다.
2. **감지(Watch)**: **Spark Operator Controller**가 신규 리소스 생성을 감지
3. **제출(Submit)**: 컨트롤러 내부의 **Submission Runner**가 `spark-submit` 명령을 대신 실행
4. **실행**: Kubernetes API를 통해 **Driver Pod**가 생성되고, 이후 Driver가 **Executor Pod**들을 직접 요청하여 생성
5. **모니터링**: **Spark Pod Monitor**가 각 Pod의 상태를 감시하며, 그 결과를 `SparkApplication` 객체의 `status` 필드에 업데이트

### 핵심 구성 요소
- **SparkApplication**: 단일 Spark 작업을 실행할 때 사용
- **ScheduledSparkApplication**: Cron 스타일의 스케줄링이 필요한 주기적 작업에 사용

### 주요 기능 및 설정 항목

- **Restart Policy**: 작업 실패 시 재시작 전략을 설정할 수 있습니다 (`Never`, `OnFailure`, `Always`).
- **Mutating Admission Webhook**: (옵션) Pod가 생성될 때 설정을 주입합니다. 예를 들어 ConfigMap 마운트, 볼륨 설정, 환경 변수 주입 등을 자동화합니다.
- **Dynamic Allocation**: 리소스 사용량을 최적화하기 위해 실행 중 Executor 수를 동적으로 조절할 수 있습니다.
- **Monitoring**: Prometheus와 연동하여 메트릭을 수집하는 기능을 내장하고 있습니다.

### YAML 예시

기본적인 `SparkApplication` 구조

```yaml
apiVersion: "sparkoperator.k8s.io/v1beta2"
kind: SparkApplication
metadata:
  name: spark-pi
  namespace: default
spec:
  type: Scala
  mode: cluster
  image: "gcr.io/spark-operator/spark:v3.1.1"
  mainClass: org.apache.spark.examples.SparkPi
  mainApplicationFile: "local:///opt/spark/examples/jars/spark-examples_2.12-3.1.1.jar"
  sparkVersion: "3.1.1"
  restartPolicy:
    type: OnFailure
    onFailureRetries: 3
    onFailureRetryInterval: 10
  driver:
    cores: 1
    memory: "512m"
    serviceAccount: spark-sa
  executor:
    cores: 1
    instances: 2
    memory: "512m"

```

### 요약

Spark Operator를 사용하면 **(1) YAML을 통한 인프라 관리(GitOps 연동 용이)**, **(2) 자동 재시작 및 상태 관리**, **(3) Kubernetes 네이티브한 모니터링**이 가능하다는 것이 공식 문서의 핵심 요지입니다.

특정 환경(AWS EMR on EKS, 온프레미스 등)에 맞는 **상세한 YAML 설정(Volume 마운트나 S3 연동 등) 예시**가 필요하신가요? 구체적인 요구사항을 알려주시면 바로 작성해 드릴 수 있습니다.