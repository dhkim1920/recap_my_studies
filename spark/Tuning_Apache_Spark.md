**※ 클라우데라 공식 문서 참고하여 작성합니다.**


# 소프트웨어 성능 개선
- Yarn 메모리 조정
- Kryo Serializer 사용 (고성능 직렬화 라이브러리)
  - 기본 직렬화 보다 직렬화 속도가 빠름
  - 메모리 사용량이 적음
  - GC 부하 감소
  - 주의점: 사용자 정의 클래스를 직접 등록해야함, 안하면 성능 감소
- 셔플 줄이기
  - 네트워크 I/O, 디스크 I/O 비용, CPU 오버헤드 발상생
- 알맞은 조인 선택 
  - ShuffledHashJoin: 양쪽 테이블 모두 셔플
  - BroadcastHashJoin: 작은 테이블을 전체 노드에 브로드 캐스트
  
# Spark App 튜닝
## Spark 셔플(Shuffle) 연산 튜닝
Spark에서 데이터셋은 여러 개의 파티션(partition)으로 나누어져 있습니다. 이 파티션은 고정된 수만큼 존재합니다.
Spark가 변환 작업을 할 때, 두 가지 의존성 관계가 생깁니다.

**좁은 의존성(Narrow Dependency)**
- 하나의 부모 파티션이 하나의 자식 파티션을 직접 만들 때 생깁니다.
- 예를 들어 map, filter 같은 연산은 한 파티션 안에서만 작업이 끝나기 때문에 다른 파티션과 데이터 교환이 필요 없습니다.

**넓은 의존성(Wide Dependency)**
- 하나의 자식 파티션을 만들기 위해 여러 부모 파티션에서 데이터를 가져와야 할 때 생깁니다.
- 예를 들어 reduceByKey, groupByKey 같은 연산은 같은 키를 가진 데이터를 모아야 하므로 여러 파티션에서 데이터를 모읍니다.
- 여기서 셔플이 발생, 셔플은 데이터를 네트워크를 통해 다른 워커 노드로 보내야 하고, 중간 결과를 디스크에 저장했다가 다시 읽어야 합니다.
- 이 과정은 디스크 I/O와 네트워크 I/O를 유발하여 전체 작업 속도를 느리게 만드는 주요 원인입니다.

## 셔플 최소화하기
1. groupByKey().mapValues(.sum) 대신 reduceByKey( + _)를 쓰자
- groupByKey()는 모든 키-값 데이터를 셔플해서 키별로 모은 다음 다시 mapValues(_.sum)로 합칩니다. (네트워크 트래픽, 메모리 증가)
- reduceByKey(_ + _)는 데이터를 모으면서 동시에 합산합니다. 같은 키끼리 로컬에서 먼저 합치고, 최종 합계만 네트워크로 보내기 때문에 셔플량이 훨씬 적습니다.

2. flatMap-join-groupBy 패턴 대신 cogroup를 쓰자
- flatMap-join-groupBy는 다음과 같이 동작합니다. 먼저 여러 데이터셋을 펼쳐서(flatMap) 조인(join)하고 다시 groupBy로 묶습니다. join과 groupBy 모두 셔플이 발생합니다.
- cogroup은 여러 데이터셋을 한 번의 셔플로 묶어버립니다. 그리고 같은 키에 해당하는 값들을 한꺼번에 가져옵니다.

## 셔플이 발생하지 않는 경우
- 두 RDD가 동일한 파티셔너로 파티셔닝되어 있고, 조인 시 파티션 수가 같으면 추가적인 셔플이 필요 없습니다.
- 작은 데이터셋은 브로드캐스트 조인(Broadcast Join)으로 셔플 없이 처리할 수 있습니다.

## 셔플 변환을 추가해야 할 때
- 입력 데이터가 매우 적은 파티션 수로 들어오는 경우, repartition으로 파티션 수를 늘려 CPU 사용량을 높일 수 있습니다.
- 대규모 집계를 수행할 때, driver의 병목을 줄이기 위해 중간 단계에서 reduceByKey, aggregateByKey 등을 사용하는 것이 좋습니다.

## Secondary Sort
repartitionAndSortWithinPartitions: 셔플 과정에서 키 별 정렬 처리 가능 
- 예시) 사용자 별, 시간별 순서

## 파티션 수 튜닝
Spark의 각 stage는 여러 개의 task로 구성되며, 각 task는 순차적으로 데이터 처리
이때 stage 별 task의 수가 Spark 성능을 결정

### Spark에서 파티션 수가 결정되는 경우 (3가지)
1. 상위 데이터셋이 있을 때 (일반 변환)
- 기본적으로 상위 데이터셋의 파티션 수를 그대로 따라갑니다.
- 단, 변환 연산 종류에 따라 예외가 있습니다:
  - coalesce: 파티션 수를 줄임
  - union: 상위 데이터셋들의 파티션 수를 합침
  - cartesian: 상위 데이터셋들의 파티션 수를 곱함

2. 부모 데이터셋이 없는 경우 (파일 입력 등)
- textFile, hadoopFile 같은 경우
- MapReduce InputFormat이 결정한 스플릿 수를 기반으로 파티션 생성
- 일반적으로 HDFS 블록 하나당 파티션 하나 생성

3. parallelize 같은 메서드로 직접 생성한 경우
- 메서드 호출 시 명시한 파티션 수를 따름 (지정하지 않으면 spark.default.parallelism 설정값 참고)

### task 수가 클러스터의 실행 슬롯 수보다 적으면 발생하는 문제
- CPU를 적절하게 활용하지 못함
- task aggregation 시 메모리를 더 사용
- 메모리 부족 시 GC 증가 → 작업 지연 → 디스크로 데이터가 spill → 디스크 I/O 및 정렬 발생 → 작업 중단 또는 지연

### 적절한 numPartitions 값 찾기
- 상위 데이터셋의 파티션 수를 확인, 거기에 1.5를 곱하면서 성능이 개선 모니터링, 성능이 좋아질 때 까지만 진행

Spark에서는 각 task로 보내는 데이터량이 그 task가 사용할 수 있는 메모리 크기 안에 들어 가야 함
이는 메모리 초과로 인한 디스크 spill 없애기 위함

1. 각 task에 할당 가능한 메모리 계산 공식
```(spark.executor.memory * spark.shuffle.memoryFraction * spark.shuffle.safetyFraction) / spark.executor.cores```
- spark.executor.memory: Executor 하나가 가지는 전체 메모리
- spark.shuffle.memoryFraction: 셔플 작업에 배정되는 메모리 비율 (기본 20%)
- spark.shuffle.safetyFraction: 안전 여유 메모리 비율 (기본 80%)
- spark.executor.cores: Executor 하나당 CPU 코어 수
- 메모리 일부를 셔플용, 여유 공간 까지 계산

2. 왜 약간 올려 잡아야 하나?
- 파티션 수가 너무 적으면: 한 task에 몰리는 데이터가 많아져서 메모리 초과, spill 발생
- 파티션 수가 많으면: task가 작게 나뉘어 메모리에 여유 있게 들어감 (Spark는 task 수가 많은 것은 잘처리 함)
- 때문에 조금 여유 있게(파티션 수 크게) 설정하는 것이 안전

## 데이터 구조 크기 줄이기
Spark는 메모리에서 역직렬화된(Deserialized) 객체로 데이터를 다룹니다. 
- 따라서 객체가 클 경우 디스크 스필이 증가하고 캐시 가능한 레코드 수가 감소한다. 
- 큰 객체는 지양

## 데이터 포맷 선택
디스크 저장 시 JSON 대신 이진 포맷이 좋음 (Parquet, Avro, Protobuf 등)
- 이유: JSON은 파싱 비용이 커서 비효율적


## Spark와 YARN에서 CPU 설정 관계
- Spark는 실행 시 CPU 할당량을 요청
- 이때 요청 가능한 최대 CPU 수는 YARN 설정 값인 `yarn.nodemanager.resource.cpu-vcores`를 초과할 수 없음
- Spark 주요 CPU 관련 설정:
  - `--executor-cores` 또는 `spark.executor.cores`
  - `--driver-cores`

## Spark에서 코어 할당 시 주의할 점
- **Executor에 5 core 이상 할당 할 경우**:
  - HDFS I/O 경쟁이 심해져 처리량 감소할 수 있음
  - 너무 많은 코어를 할당할 경우 **Context Switching 증가**, **I/O 병목 발생** 가능성이 높아짐
- **적절한 코어 수**를 설정하여 CPU와 I/O 리소스를 균형 있게 사용하는 것이 중요


※ 본 문서는 Cloudera 공식 문서 내용을 요약 및 재구성한 것입니다. 원문은 Cloudera Documentation을 참고하십시오."