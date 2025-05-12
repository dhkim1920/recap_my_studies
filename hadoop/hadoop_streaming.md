# Hadoop Streaming

## 정의

Hadoop Streaming은 Hadoop MapReduce 작업을 실행할 때, 표준 입출력(STDIN/STDOUT)을 사용하는 프로그램이면 
<br>어떤 언어로 작성했든 Mapper와 Reducer로 사용할 수 있게 해주는 Hadoop 기본 유틸리티다.

## 주요 특징
- Java로 프로그램 짤 필요 없이, Python, Shell, Perl, Ruby 같은 스크립트 언어로 MapReduce 작성 가능하다.
- 표준 입력(STDIN)으로 데이터를 받고, 표준 출력(STDOUT)으로 결과를 출력하는 프로그램만 있어서 간편
- Hadoop이 각 Mapper/Reducer 프로세스를 실행하고 입출력을 자동으로 연결한다.

## 구성
- **Mapper 프로그램**: 입력 받은 데이터를 가공해서 중간 결과를 출력
- **Reducer 프로그램**: Mapper 결과를 받아 최종 결과를 집계

## 명령어 예시

```bash
hadoop jar /path/to/hadoop-streaming.jar \
  -input /input/path \
  -output /output/path \
  -mapper /path/to/mapper.py \
  -reducer /path/to/reducer.py
```

## Mapper 예시 (Python)
```python
import sys
for line in sys.stdin:
    print(line.strip().split()[0], 1)
```

## Reducer 예시 (Python)
```python
import sys
from collections import defaultdict

counts = defaultdict(int)
for line in sys.stdin:
    key, value = line.strip().split()
    counts[key] += int(value)
for key in counts:
    print(key, counts[key])
```

## 장점
- 빠르게 프로토타입 작성 가능
- Java 없이 다양한 언어 활용 가능
- 작은 MapReduce 작업은 매우 간편하게 작성 가능

## 단점
- 대규모 작업에는 성능 최적화가 어렵다.
- Mapper/Reducer 프로세스가 별도로 뜨기 때문에 프로세스 부하가 발생한다.
- 복잡한 로직에는 비효율적 (Spark 쓰는게 더 낫다.)

## 요약

| 항목 | 내용 |
|:---|:---|
| 무엇인가 | STDIN/STDOUT 프로그램을 MapReduce로 실행할 수 있게 해주는 Hadoop 유틸리티 |
| 언제 쓰나 | 빠르게 MapReduce 프로토타입 만들 때, Java 없이 작업할 때 |
| 장점 | 다양한 언어 지원, 개발 간편 |
| 단점 | 대규모 처리 성능 한계, 최적화 어려움 |

# Hadoop Streaming vs Spark Streaming 차이

| 항목 | Hadoop Streaming | Spark Streaming |
|:---|:---|:---|
| 기본 구조 | Batch 기반 MapReduce | Micro-Batch 기반 스트리밍 처리 |
| 프로그래밍 모델 | STDIN/STDOUT 기반 외부 스크립트 | RDD, DStream, DataFrame API 기반 내부 처리 |
| 처리 방식 | 대량 데이터 일괄 처리 (Batch) | 실시간 데이터 흐름 처리 (Near Real-time) |
| 사용 언어 | Python, Bash, Perl 등 외부 프로그램 자유 | Scala, Python, Java, R (Spark API 사용) |
| 성능 최적화 | 제한적 (외부 프로세스 통신 부하) | 메모리 기반 처리로 빠름 |
| 실패 처리 | Hadoop 자체 복구 기능 | 체크포인트 기반 복구 지원 |
| 사용 목적 | 빠른 MapReduce 프로토타이핑, 비표준 처리 | 스트리밍 데이터 분석, 실시간 처리 |

# 핵심 요약
- Hadoop Streaming은 Batch성 작업 (대량 로그 처리)용으로, 빠른 개발과 간단한 데이터 변환에 적합
- Spark Streaming은 실시간에 가까운 데이터 흐름 분석에 최적화되어 있고, 메모리 기반이라 성능이 훨씬 좋다.

