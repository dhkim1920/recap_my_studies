# Spark Stage

## Stage
- Stage는 동일한 연산 흐름을 수행하는 태스크들의 묶음이다.
- 셔플이 발생하는 지점이 경계가 되어 DAG가 여러 Stage로 분리된다.
- Stage의 태스크 수는 해당 Stage가 처리하는 입력 파티션 수를 따른다.
- 스케줄러 관점에서 Stage 타입은 ShuffleMapStage, ResultStage 두 가지로 나뉜다.

## ShuffleMapStage
- 셔플이 필요한 지점에서 만들어지는 중간 Stage다.
- 목적은 다음 Stage가 사용할 셔플 데이터 map output을 만드는 것
- 각 태스크는 자신의 입력 파티션을 처리한 뒤 셔플 파일을 로컬 디스크에 기록한다.
- reduce 쪽에서 데이터를 가져갈 수 있도록 map output 위치 정보를 추적한다.
- ShuffleDependency와 1대1로 연결되는 형태로 다뤄진다.
- 실행 상태 관리에서 missing partition 추적, 모든 output 준비 여부 판단 같은 개념이 등장한다.

## ResultStage
- 액션이 실제로 끝나는 마지막 Stage다.
- count, save, write 같은 액션이 요구하는 최종 결과를 계산한다.
- 앞선 ShuffleMapStage가 만든 셔플 데이터를 읽어 최종 결과를 만들거나 파일 쓰기 같은 최종 작업을 수행한다.

## 로그에서 ShuffleMapStage, ResultStage가 의미하는 것
- ShuffleMapStage는 셔플의 map 쪽 결과를 만들고 로컬에 기록하는 단계가 실행 중이라는 뜻이다.
- ResultStage는 액션을 완료하는 최종 단계가 실행 중이라는 뜻이다.
- 셔플이 여러 번 있으면 ShuffleMapStage가 여러 개 생길 수 있고 마지막에 ResultStage가 붙는 형태가 된다.

## 참고)
### DAG
- Directed Acyclic Graph의 약자다.
- 방향이 있는 간선으로 연결된 그래프이며 사이클이 없는 구조다.
- Spark에서는 연산 의존성을 DAG 형태로 표현하고 액션이 호출되면 이 DAG를 기반으로 실행 계획을 세운다.

### DAGScheduler
- Spark의 스케줄러 구성 요소 중 하나다.
- 액션이 호출되면 DAG를 분석해 Stage들을 만들고 Stage 간 의존성을 고려해 실행 순서를 결정한다.
- 셔플 경계를 기준으로 Stage를 나누고 각 Stage 실행을 TaskScheduler 쪽으로 전달한다.