# AIP-67 Airflow 컴포넌트의 멀티팀 배포

> 출처 https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-67+Multi-team+deployment+of+Airflow+components
> Created by Jarek Potiuk, last modified on Aug 28, 2025

## 상태
- Airflow 3.2에서 Experimental로 들어갈 예정
  
## 개요

여기서 설명하는 멀티팀 기능은 여러 팀이 단일 Airflow 배포를 공유하되, 다음 관점에서 서로 격리될 수 있게 합니다.

* 팀별 구성 정보(Variables, Connections)에 대한 접근 격리
* 팀별 DAG 작성자가 제출한 코드를 격리된 환경에서 실행(파싱과 실행 모두)
* 서로 다른 팀이 서로 다른 의존성 집합과 실행 환경 라이브러리를 사용 가능
* 서로 다른 팀이 서로 다른 Executor를 사용 가능(팀당 여러 Executor도 가능, AIP-61을 따름)
* “dataset” 기능을 통해 서로 다른 팀의 DAG를 연결 가능. 데이터셋은 팀 간에 생산과 소비가 가능하며, AIP-82 “External event-riven scheduling” 없이도 가능하고, 서로 다른 Airflow 인스턴스 사이의 인증을 위한 자격 증명을 설정하지 않고도 가능
* UI 사용자가 단일 팀 또는 여러 팀의 DAG, Connections, Variables, DAGRuns 등을 부분 집합으로 볼 수 있게 함
* Devops, 배포 관리자가 여러 팀에 서비스를 제공해야 하는 상황에서 유지보수와 업그레이드 부담을 줄이고 분산할 수 있게 함

[Airflow Survey 2023](https://airflow.apache.org)에서 멀티테넌시는 가장 많이 요청되는 기능 중 하나로 나타납니다.

물론 멀티테넌시라는 표현은 사람마다 다르게 이해될 수 있습니다. 이 문서는 Airflow 유지보수자가 선택한 멀티팀 모델을 제안하며, 모든 리소스가 테넌트 간 완전히 격리되는 “고객 멀티테넌시”를 목표로 하지 않습니다. 대신, 동일 조직 내 여러 팀이 동일 Airflow 배포를 공유하면서도 격리될 수 있는 방식, 그리고 많은 사용자가 멀티테넌시라고 이해해 온 요구를 충족하는 방식을 제안합니다. 혼동을 피하기 위해 “multi-tenancy” 대신 “multi-team”이라는 이름을 사용합니다.

현재도 일정 수준의 멀티테넌시를 달성하는 방법은 “Multi-tenancy today” 장에서 논의하며, 이 제안과 기존 방법의 차이는 “Differences vs. current Airflow multi-team options”에서 설명합니다.

## 동기

주요 동기는, 회사 구조 내의 각 팀이 자신에게 속한 리소스(예: DAG와 dag_id에 연동된 테이블) 일부에만 접근할 수 있도록, 단일 Airflow 배포를 제공해야 한다는 필요입니다.

이렇게 하면 UI, Webserver 배포와 Scheduler는 여러 팀이 공유할 수 있으면서도, DAG 처리와 구성, 민감 정보는 팀 단위로 격리할 수 있습니다. 또한 높은 기밀성이 필요한 별도 DAG 그룹을 별도 환경에서 실행할 수 있도록 허용합니다. 이로 인해 여러 Scheduler와 Webserver를 중복 배포하지 않아도 되어 배포 비용을 줄일 수 있습니다.

이는 동일 조직에서 여러 부서나 여러 팀이 여러 Airflow 배포를 사용하고 있고, (복잡도가 더 높더라도) 여러 독립 인스턴스를 유지하는 것보다 단일 인스턴스를 유지하는 편이 더 낫다고 판단되는 경우에 해당합니다.

또한 Airflow의 일부 관리를 중앙화하면서도, 실행 환경 결정은 팀에 위임할 수 있습니다. 워크로드 격리가 쉬워지면서, Airflow의 공통 데이터셋 기능을 통해 팀 간 상호작용도 유지할 수 있습니다.

## 상위 목표 요약

이 제안의 목표를 두고 많은 논의가 있었고, 적합성에 대한 다양한 의견이 있습니다. 다만 “북극성”으로 삼는 가장 중요한 세 가지 목표는 다음과 같습니다.

* 여러 실행 환경이 중요해지는 멀티팀 운영에서( AIP-72가 완료되면) 운영 오버헤드를 줄이는 것
* 팀 간 가상 자산을 공유할 수 있게 하는 것
* “admin”과 “team sharing” 기능을 제공하여 여러 팀의 DAG를 단일 Airflow UI에서 볼 수 있게 하는 것
  (이를 위해 커스텀 RBAC과 AIP-56의 Auth Manager 구현이 필요하며, KeyCloak Auth Manager가 참조 구현입니다)

## 용어와 문구

이 문서는 형식적 명세가 아닙니다. 다만 대문자로 강조한 경우, “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, “OPTIONAL” 같은 키워드는 [RFC 2119](https://www.ietf.org)의 정의대로 해석합니다.

## 고려 사항

### 현재의 멀티테넌시

현재 멀티팀 Airflow를 운영하는 방법은 여러 가지가 있습니다.

A. 테넌트별 별도 Airflow 인스턴스

가장 단순한 방식은, 각 테넌트마다 서로 다른 Airflow 인스턴스를 별도로 배포하고 관리하는 것입니다. 이 방식은 각 인스턴스가 자체 DB, Webserver, Scheduler, Worker, 설정과 실행 환경(라이브러리, OS, Variables, Connections)을 갖습니다.

B. 테넌트별 별도 Airflow 인스턴스, 일부 리소스 공유

조금 더 복잡한 방식은 비용 절감을 위해 일부 리소스를 공유하는 것입니다. DB는 공유될 수 있으며(각 Airflow 환경이 동일 DB에서 각자 스키마를 사용), Webserver 인스턴스는 동일 환경에서 실행할 수도 있고, 동일 Kubernetes 클러스터를 사용해 작업을 실행할 수도 있습니다.

A 또는 B에서처럼 여러 Airflow 인스턴스를 배포하는 경우, Airflow의 AuthUI 접근(특히 [Auth Manager feature AIP-56](https://cwiki.apache.org))을 단일 인증 프록시에 위임할 수 있습니다. 예를 들어 KeyCloak Auth Manager를 구현하면 단일 KeyCloak 인증 프록시로 여러 Airflow Webserver UI 인스턴스에 대해 통합된 접근 방식을 제공하고, 통합된 URL 스킴으로 노출할 수 있습니다.

C. 단일 Airflow 인스턴스를 여러 팀이 사용

현재 Airflow에서도 팀별로 실행과 파싱 환경을 분리할 가능성은 있습니다.

Airflow DAG 폴더 내의 각 폴더별로 DAG File Processor 집합을 분리하고, 팀별로 서로 다른 실행 환경(라이브러리, 시스템 라이브러리, 하드웨어)과 큐(Celery), 또는 서로 다른 Kubernetes Pod Template을 사용해 실행 워크로드를 분리할 수 있습니다. 이는 Cluster Policy로 강제할 수 있습니다.

팀별 UI 접근 또한 조직 관리 인증과 인가 프록시와 통합된 커스텀 Auth Manager 구현으로 구성할 수 있습니다.

하지만 이 방식에서는 워크로드가 동일 DB에 접근하며, Connections와 Variables를 포함해 서로의 DB 영역에 간섭할 수 있습니다. 즉 팀별 “보안 경계”가 없고, 한 팀 DAG 작성자가 다른 팀 DAG에 간섭하는 것을 막을 수 없습니다. 이런 격리 부족이 주요 단점이며, 이 AIP는 A와 B 수준의 격리와 보안을 단일 인스턴스 배포에서 제공하는 것을 목표로 합니다.

또한 Airflow 설정만으로 손쉽게 지원되는 방식도 아닙니다. 일부 사용자는 제한을 두거나(예: Kubernetes Pod Operator만 사용), 커스텀 Cluster Policy나 코드 리뷰 규칙을 통해 팀 간 DAG 혼합을 방지하지만, 이를 활성화하는 단일하고 쉬운 메커니즘은 없습니다.

## 멀티팀 제안과 기존 멀티팀 옵션의 차이

현재 가능한 방식 대비 이 제안이 어떻게 다른지 요약하면 다음과 같습니다.

* 스케줄링과 실행 리소스 사용량은 A 또는 B에 비해 약간 낮을 수 있습니다. 스케줄링과 UI를 위한 하드웨어는 공유하고, 워크로드는 A나 B에서처럼 팀 단위로 분리합니다. 단일 DB와 단일 스키마를 모든 팀이 재사용하지만, 리소스 이득과 격리는 B에서 동일 DB 내 여러 독립 스키마를 사용하는 경우와 크게 다르지 않습니다.
  리소스 사용량 감소는 이 제안의 목표가 아닙니다.
* 유지보수 측면에서는 A와 B의 완전한 실행 환경 격리와, C의 일부 중앙화 사이에서의 트레이드오프입니다. 팀 간 결합이 증가(예: 같은 Airflow 버전)할 수 있지만, C보다 훨씬 더 완전한 워크로드 격리를 제공합니다.

* 제안된 해법은, 옵션 C에서 Cluster Policy로 하는 것보다 더 쉽고 더 완전하게 팀 분리를 관리할 수 있게 합니다. 이 제안에서는 팀이 서로의 코드와 실행에 간섭할 수 없다고 신뢰할 수 있습니다. Scheduler 알고리즘의 공정성을 전제로 하면 팀 간 실행 효율도 격리되어야 합니다.
  서로 다른 팀에 속한 DAG 작성자가 초래하는 워크플로우 간 간섭을 방지하고, 보안과 격리를 제공하는 것이 핵심 차이입니다.
* 모든 팀을 위한 단일 통합 Webserver 진입점을 제공하고, 전체 “클러스터” 관리를 위한 단일 관리자 UI도 제공할 수 있습니다.
* (현재 강화되고 개선된) 데이터셋 기능을 활용해, 데이터셋을 매개로 팀 간 인터페이스를 구성할 수 있습니다. Airflow 2.9 기준으로는 A와 B에서도 새로운 API를 통해 인스턴스 간 데이터셋 이벤트 공유가 가능하지만, 단일 인스턴스 멀티팀 Airflow에서는 서로 독립된 인스턴스 간 인증 설정 없이도 팀 간 데이터셋 기반 스케줄링이 가능합니다.
* 단일 API와 단일 DB 소스에서 Airflow 사용량 분석과 상관관계 분석, 태스크 분석이 가능합니다.

Credits and standing on the shoulders of giants.

### 가능하게 만든 선행 AIP

개념을 마무리하기까지 시간이 오래 걸렸습니다. 다른 AIP 위에 구축해야 했기 때문이며, Airflow에 기능이 점진적으로 추가되고 반복 개선되면서, 다른 AIP가 “거인의 어깨”가 될 정도로 준비가 된 뒤에야 멀티팀 레이어를 얹는 설계를 할 수 있었습니다.

관련 AIP 목록은 다음과 같습니다.

* [AIP-12 Persist DAG into DB](https://cwiki.apache.org)  DAG 구조를 DB에 저장(Serialization)하기로 한 초기 결정, DB 내 DAG 직렬화를 OPTIONAL로 둘 수 있게 함
* [AIP-24 DAG Persistence in DB using JSON for Airflow Webserver and (optional) Scheduler](https://cwiki.apache.org)  Webserver를 분리해 공통 인프라로 추출할 수 있게 함
* [AIP-43 DAG Processor separation](https://cwiki.apache.org)  DAG 파싱과 실행 환경을 Scheduler와 분리하고 Scheduler를 공통 인프라로 이동 가능
* [AIP-48 Data Dependency Management and Data Driven Scheduling](https://cwiki.apache.org)  팀 간 인터페이스로 사용할 수 있는 DataSets 개념 도입
* [AIP-51 Removing Executor Coupling from Core Airflow](https://cwiki.apache.org)  Executor를 코어에서 분리하고 명확한 Executor API를 도입하여 Hybrid Executor 구현 가능
* [AIP-56 Extensible user management](https://cwiki.apache.org)  조직의 Identity 서비스와 통합할 수 있는 외부 관리 방식의 유연한 사용자 관리 제공
* [AIP-60 Standard URI representation for Airflow Datasets](https://cwiki.apache.org)  팀이 Datasets로 소통할 때 사용할 “공통 언어” 구현
* [AIP-61 Hybrid Execution](https://cwiki.apache.org)  여러 Executor를 사용할 수 있게 하여, 팀별 Executor 집합으로 가는 길을 마련
* [AIP-66 DAG Bundles and Parsing](https://cwiki.apache.org)  DAG를 번들로 묶어 관리하고, 번들에서 팀을 매핑할 수 있게 함
* [AIP-72 Task Execution Interface aka Task SDK](https://cwiki.apache.org)  새로운 Task SDK API를 통한 GRPC 또는 HTTPS 통신 기반 실행 모델 제공
* [AIP-73 Expanded dataset awareness](https://cwiki.apache.org)  데이터셋을 데이터 자산으로 재정의하는 하위 AIP 포함
* [AIP-82 External event driven scheduling in Airflow](https://cwiki.apache.org)  데이터셋에 대한 외부 이벤트 기반 스케줄링 구현

초기 제안은 AIP-44 기반의 DB 접근 격리를 전제로 했지만, 이 AIP는 Airflow 3을 타겟으로 하므로 위의 AIP-72를 기반으로 합니다.

* ~~[AIP-44 Airflow Internal API](https://cwiki.apache.org)  (진행 중) DAG 작성자가 만든 코드를 실행할 수 있는 컴포넌트에서 DB 접근을 분리하여, DAG 파싱과 실행에 대한 완전한 보안 경계를 제공~~

## 설계 목표

### 구조적, 아키텍처 변경

이 제안의 구현 접근 목표는, 멀티팀 기능을 도입하면서도 Airflow의 구조적, 아키텍처 변경을 최소화하고, DAG 작성자 관점의 하위 호환성과 조직 배포 관리자 관점의 오버헤드를 최소화하는 것입니다. Airflow 2용으로 작성된 DAG는, [Airflow의 Public Interface](https://airflow.apache.org)를 사용하고 있다면, 멀티팀 환경에서도 변경 없이 실행되어야 합니다.

DAG bundle을 팀 ID를 결정하는 수단으로 사용합니다.

멀티팀 배포를 지원하기 위해 DB 구조는 최소한으로 수정합니다.

* “teams” 신규 테이블 정의
* Bundle name에서 Team ID로의 매핑을 보관하는 신규 테이블 정의(다대일 관계)
  멀티팀이 활성화된 경우, 이 테이블로 특정 DAG의 team_id를 조회합니다.
* Connection과 Variable에 추가 “team_id” 선택 필드 추가
  team_id가 있으면, 번들 매핑으로 해당 team_id에 속하는 DAG만 Task SDK를 통해 접근할 수 있습니다.
  team_id가 없는 Connection과 Variable은 어떤 DAG도 접근할 수 있습니다.
  이 team_id는 UI 사용자 접근을 결정할 때 Auth Manager에도 제공됩니다.
* Pool에 추가 “team_id” 선택 필드 추가
  team_id가 있으면, 번들 매핑으로 같은 team_id인 DAG에서만 사용되어야 합니다.
  DAG File Processor는 다른 팀의 pool을 사용하는 DAG 파싱에 실패해야 합니다.
* DAG File Processor는 “--team-id” 플래그로 시작할 수 있습니다.
  이 플래그가 있으면, 해당 team_id로 매핑되는 번들에 속한 DAG만 파싱합니다.

그 외 구조적 DB 변경은 필요하지 않습니다. Airflow DB 스키마에 “연쇄 효과”는 없습니다.

### 보안 고려 사항

멀티팀 Airflow의 보안 특성에 대해 다음 가정을 둡니다.

* 다른 AIP에 대한 의존
  멀티팀 모드는 AIP-72(Task SDK)와 Standalone DAG file processor, AIP-66(DAG Bundles and Parsing)와 함께 사용할 수 있습니다.
* 리소스 접근 보안 경계
  이 AIP에서 파싱과 실행의 보안 경계는 팀 경계입니다.
  팀 환경(실행 또는 파싱) 안에서 워크로드가 실행되면, 같은 팀의 모든 리소스(DAG 및 관련 리소스)에 대해 완전한 접근(읽기와 쓰기)을 가진다고 가정합니다.
  반대로 다른 팀의 리소스에는 어떤 접근도 할 수 없다고 가정합니다.
* Task SDK 인증
  DAG file processor나 Worker에 전달되는 JWT 토큰에는 bundle_name claim이 포함됩니다. Worker나 파싱 프로세스가 이를 수정할 수 없으므로, 다른 팀의 Connections와 Variables에 접근하는 것을 방지할 수 있습니다.
* DAG 작성
  각 팀의 DAG는 팀 전용 번들에 저장됩니다.
* 실행
  파싱과 실행 모두 격리된 환경에서 실행되어야 합니다.
  예를 들어 Celery에서는 팀별 큐, 서로 다른 Executor 설정 등입니다.
  다만 조직 배포 관리자는 프로세스 분리 정도가 충분하다고 판단하면, 일부 또는 모든 팀을 동일 환경에 배치할 수도 있습니다.
* Triggerer
  Triggerer는 선택적으로 “--team-id” 파라미터를 가지며, 해당 경우 특정 팀의 번들에 속한 DAG ID의 deferred task만 처리합니다.
  “--team_id”가 없는 Triggerer는 특정 팀의 번들에 속한 DAG의 deferred event를 모두 처리합니다.
  쿼리는 멀티팀이 아닌 환경에서는 추가 조건을 피하도록 최적화될 수 있습니다.
* Data assets
  URI를 가진 Data asset은 팀 간 공유될 수 있으며, 한 팀이 생산한 이벤트를 다른 팀이 소비할 수 있습니다.
  DAG 작성자는 같은 URI를 사용한다면 팀 간 이벤트를 생산하고 소비할 수 있습니다.
  다만 소비하는 쪽 DAG 작성자는 어떤 다른 팀의 이벤트를 소비할지 지정할 수 있습니다.
  이를 통해 조직 내에서 URI로 자산을 공유하면서, 소비 팀이 어떤 팀이 자산 이벤트를 생산하는 것을 허용할지 제어할 수 있습니다.
* UI 접근
  UI에서 리소스(DAG 관련)의 필터링은 Auth Manager가 합니다.
  DAG, DagRun, Task Instance, Connection, Variable 등 각 리소스 타입에 대해, Auth Manager는 사용자가 속한 팀에 따라 필터링할 책임이 있습니다.
  Auth Manager는 접근 결정을 위해 team_id 필드를 전달받습니다.
  현재 FAB Auth Manager는 레거시로 간주하며 멀티팀용 필터링을 구현할 계획이 없습니다.
  KeyCloak Auth Manager 통합은 KeyCloak의 사용자 그룹에 team_id를 매핑할 수 있어야 합니다.
* 커스텀 플러그인
  멀티팀 환경에서는 향후 UI 플러그인만 사용해야 합니다.
  Airflow 2의 레거시 플러그인은 지원하지 않습니다(FAB Auth Manager에 의존).
  플러그인에는 team_id가 전달되며(해당 리소스에 team_id가 있고 멀티팀이 활성화된 경우), 플러그인 작성자는 Auth Manager의 접근 메커니즘을 사용해 리소스 접근을 결정할 수 있습니다.
* UI 제어와 사용자, 팀 관리
  AIP-56에서 Airflow는 인증과 인가 관리를 Auth Manager에 위임했습니다.
  멀티팀 배포에서도 동일합니다.
  즉 Airflow Webserver는 로그인 사용자가 어떤 리소스와 UI 일부에 접근할 수 있는지에 대해 알거나 결정하지 않습니다.
  또한 Airflow는 사용자가 어떤 팀에 접근 가능한지, 여러 팀에 접근 가능한지, UI에서 팀 전환이 가능한지 같은 기능을 관리하지 않습니다.
  이런 기능은 이 AIP 범위 밖이며, Auth Manager 구현체마다 다르게 선택할 수 있습니다.
  사용자 팀 전환 같은 고급 기능은 Auth Manager에 새로운 API가 필요할 수 있지만, 이는 이 AIP 범위 밖이며 필요 시 후속 AIP로 다룹니다.

## 설계 비목표

이 제안의 비목표를 설명합니다. 사용자가 멀티팀 Airflow를 배포하려 할 때, 이 제안이 실제로 의미하는 바를 더 명확히 하기 위함입니다.

* 현재 멀티테넌시 방식 대비 Airflow 설치의 리소스 소비를 크게 줄이는 것이 주 목표가 아닙니다.
  보안과 격리를 고려해, 리소스에 약간의 영향이 있을 수 있는 방식을 의도적으로 택하지만, 큰 영향을 주는 것은 목표가 아닙니다.
  특히 동일 DB에 여러 독립 Airflow 인스턴스를 두는 옵션 B와 비교할 때 그렇습니다.
  격리는 성능보다 우선이며, 격리를 위해 성능 이득을 일부 포기할 수 있습니다.
* 단일 Airflow 인스턴스의 전체 수용량을 늘리는 것이 목표가 아닙니다.
  변경 이후에도 DAG 수나 태스크 수 처리 능력은 현재와 동일하며, 현재의 확장 한계가 그대로 적용됩니다.
  수백 팀이나 수천 팀을 단일 인스턴스에 올리며 팀이 늘어날수록 용량이 늘어난다고 기대할 수 없습니다.
* 멀티팀 Airflow를 “한 번에 설치”하는 메커니즘을 제공하는 것이 목표가 아닙니다.
  이 제안의 목표는 멀티팀 배포가 가능해지도록 하는 것이며, 실제 배포는 조직 배포 관리자가 아키텍처를 설계하고 구현해야 합니다.
  Helm chart 등에서 단순히 스위치를 켜면 되는 턴키 솔루션이 아닙니다.
  문서는 여러 Airflow Helm chart 인스턴스를 조합하는 가이드를 제공할 수 있으나, 여전히 가이드이며 턴키가 아닙니다.
* 여러 팀의 요구에 대응하는 전체 유지보수 노력을 줄이는 것이 목표는 아니지만, 책임 일부를 팀에 위임하고, 공통 Airflow 인스턴스 하나를 유지할 수 있게 합니다.
  단일 인스턴스를 20개 팀이 공유한다면, 20개의 컨테이너 이미지를 빌드, 커스터마이즈, 업그레이드하고 올바르게 배치하는 파이프라인을 Airflow 밖에서 구축해야 할 수 있습니다.
  Airflow는 기존의 constraint file, 참조 컨테이너 이미지, 이미지 빌드와 확장 문서 외의 추가 도구를 제공하지 않습니다.
* 서로 다른 팀을 브랜칭 전략이나 DEV, PROD, QA 환경 분리를 위해 사용하는 케이스를 지원하는 것이 목표가 아닙니다.
  이 솔루션은 동일 Airflow 인스턴스에 접근하는 서로 다른 사용자 그룹 간 격리를 위한 것이지, 같은 사용자 그룹의 환경 변형 관리를 위한 것이 아닙니다.

## 아키텍처

멀티팀 Airflow는 [Overall Airflow Architecture](https://airflow.apache.org)에 설명된 “Separate DAG processing” 아키텍처를 확장합니다.

### 현재의 “Separate DAG processing” 아키텍처 개요

“Separate DAG processing”은 몇 가지 격리 기능을 제공하지만, 여러 문제를 해결하지는 못합니다.
이 아키텍처가 제공하는 기능은, DAG 작성자가 제출한 코드 실행이 Scheduler와 Webserver가 실행되는 환경과 분리된 격리 경계에서 이뤄질 수 있다는 점입니다.
즉 오늘도, DAG 작성자의 코드를 Scheduler나 Webserver 환경과 같은 곳에서 실행하지 않도록 배포할 수 있습니다.

하지만 해결하지 못하는 점은, DB 접근 격리가 없고 DAG 작성자 간 코드 실행을 서로 격리할 수 없다는 것입니다.
즉 DAG 작성자가 Airflow 메타데이터 DB를 직접 수정하는 코드를 DAG에 작성할 수 있고, 다른 DAG 작성자가 제출한 코드와의 상호작용(코드 인젝션, 원격 코드 실행 등)을 유발할 수도 있습니다.

또한 운영 UI 액션 접근을 제한하는 명확한 메커니즘도 없습니다.
현재 권한 관리는 “DAG 개별” 단위이며, DAG 그룹에 권한을 적용할 수도 있지만 도구와 동기화가 번거롭고 이해하기 어렵습니다.

[Image](https://cwiki.apache.org)

### 멀티팀 설정을 포함한 제안 대상 아키텍처

멀티팀 설정은 워크로드 격리를 제공하며, DB 격리는 AIP-72가 제공합니다.

AIP-72가 준비되면, 이는 현재 Airflow 3 제안과 비교해 상대적으로 작은 변화입니다.
핵심은 DAG File Processing과 Task, Triggerer 환경을 격리하여, 한 테넌트의 코드가 팀별로 다른 의존성을 사용하고, 팀별로 다른 Executor를 구성하며, 다른 팀과 격리된 상태에서 실행될 수 있도록 하는 것입니다.

멀티팀 설정은 다음을 제공합니다.

* 팀별로 서로 다른 의존성 집합을 허용
* 팀별로 사용하는 자격 증명과 시크릿을 격리
* 팀 간 코드 워크로드 격리. 한 팀의 코드는 별도 보안 경계에서 실행됨

[Image: Airflow > AIP-67 Multi-team deployment of Airflow components > image-2025-6-21_14-28-32.png](https://cwiki.apache.org)

## 구현 제안

### 배포 레벨에서 여러 팀 관리

멀티팀은 전체 배포 환경을 관리하는 조직 배포 관리자용 기능입니다.
조직 배포 관리자는 팀별로 Airflow 컴포넌트를 격리된 보안 경계와 실행 환경에 배치하고, 한 팀 환경이 다른 팀 환경에 간섭하지 않도록 설정과 네트워크 기능을 적용할 수 있어야 합니다.

조직 배포 관리자가 멀티팀 형태로 배포를 준비해야 하며, Airflow 컴포넌트는 설정 일관성을 검사하지만, 팀을 추가, 제거, 이름 변경하는 별도 도구나 메커니즘을 제공하지 않습니다.
팀 추가와 제거는 수동 배포 재구성이 필요합니다.

우리는 팀 관리를 위한 UI, CLI 도구를 제공하지 않습니다.
멀티팀 배포를 재구성하기 위해 필요한 설정과 재설정 작업은 배포 변경의 일부로 구현되어야 합니다.

### Executor 지원

구현은 [AIP-61 Hybrid Execution](https://cwiki.apache.org)을 활용합니다.
각 팀은 별도 설정으로 자신의 Executor 집합을 가질 수 있습니다.
멀티팀 배포는 여러 Local Executor로도 동작할 수 있지만, Local Executor는 DAG 실행 격리를 제공하지 않으므로 테스트 목적에만 SHOULD 사용해야 합니다.

Scheduler가 시작되면, 설정된 모든 팀의 모든 Executor를 인스턴스화합니다.

Celery Executor의 경우, 여러 팀은 각각 별도의 broker와 result backend를 사용합니다.
향후에는 단일 broker와 단일 result backend를 사용하면서 `team:` 접두 큐를 사용할 수도 있지만, 이는 이 구현 범위 밖입니다.

### 설정 변경

Scheduler와 Webserver의 멀티팀은 “core, multi-team” boolean 플래그(default False)로 제어합니다.
Connections와 Variables 접근은 Task SDK가 만든 JWT 토큰으로 제어할 수 있으므로, 팀별로 별도 설정 세트를 여러 개 둘 필요는 없습니다.

설정은 단일 설정 파일에 저장되어야 합니다.
추후 팀별 설정을 전달할 필요가 생기면 Task SDK 기능으로 추가할 수 있습니다.
Task SDK는 Worker, Triggerer, DAG processor에 팀별 설정을 전달할 수 있을 것입니다.
하지만 멀티팀의 첫 번째 반복에서는 필요하지 않습니다.

기존의 multi executor 설정은 팀 접두사를 포함하도록 확장합니다.
접두사는 “:”로 구분하고, 팀 간 엔트리는 “;”로 구분합니다.

[core]

executor = team1=Kubernetes Executor,my.custom.module.Executor Class;team2=CeleryExecutor

Executor 설정 섹션도 같은 팀 접두사를 사용합니다.

[team1:kubernetes_executor]

api_client_retry_configuration = { "total": 3, "backoff_factor": 0.5 }

환경 변수에서 설정을 보관할 때는 “:”를 “___”(언더스코어 3개)로 바꿉니다. 예:

AIRFLOW__TEAM1___KUBERNETES_EXECUTOR__API_CLIENT_RETRY_CONFIGURATION

Connections와 Variables 접근 제어

멀티팀 배포에서는 Connection과 Variable 정의에 team_id를 지정할 수 있습니다.
Connection이나 Variable에 team_id가 지정되어 있으면, Task SDK는 태스크 또는 DAG가 해당 team_id에 속하는 경우에만 태스크와 DAG file processor에 Connection과 Variable 정보를 제공합니다.
team_id가 없는 Connection과 Variable은 파싱 중인 모든 태스크와 DAG가 접근할 수 있습니다.

Pools

Pool에는 추가 team_id 필드가 생기며 nullable입니다.
즉 Pool은 공용일 수도 있고 팀 전용일 수도 있습니다.
예를 들어 default_pool이 모든 팀 공용일 수도 있고, 각 팀이 자체 default_pool을 가질 수도 있습니다(팀 설정 파일 또는 환경 변수로 구성).
DAGFileProcessor는 다른 팀의 pool을 사용하는 DAG file 파싱에 실패합니다.
스케줄링 로직은 pool에 대해 기존과 동일합니다.

### Dataset triggering 접근 제어

어떤 DAG도 어떤 data asset과 연관된 이벤트를 생산할 수 있지만, data asset을 소비하는 DAG는 기본적으로 같은 팀에서 발생한 이벤트 또는 Auth Manager가 같은 팀에 속한다고 판정한 사용자 API 호출로 발생한 이벤트만 받습니다.

DAG 작성자는 data asset의 URI를 매개로, 추가로 트리거를 허용할 팀 목록을 지정할 수 있습니다. 예:

allow_triggering_by_teams = [ "team1", "team2" ]

이 부분은 AIP-73 Expanded Data Awareness에 의존하며, 구체 구현은 Data asset의 상세 구현을 기반으로 합니다.

AIP-82 External Driven Scheduling과의 관계도 존재합니다.
여러 Airflow 인스턴스가 있을 때는, 여러 인스턴스가 공유하는 “Physical dataset”을 통해 유사한 결과를 얻을 수 있습니다.
예를 들어 한 인스턴스가 생성한 S3 객체를 다른 인스턴스가 소비할 수 있습니다.
이 경우 deferred trigger가 외부 dataset을 모니터링해야 하고 외부 dataset에 대한 권한도 필요합니다.
하지만 팀 간 dataset 공유 기능은, 물리적으로 공유된 객체가 없는 가상 자산에도 동작하며, 그런 자산의 변경을 감지하는 트리거에도 동작합니다.

### 메타데이터 DB 변경

DB 변경은 이전 버전의 이 AIP보다 훨씬 작고, Airflow 코드베이스 전반으로 퍼지는 “연쇄 효과”를 피합니다.

* “teams” 신규 테이블 정의
* Bundle name에서 Team ID로의 매핑을 보관하는 신규 테이블 정의(다대일 관계)
  이에 대한 UI 설정도 추가되어야 합니다.
* Connection과 Variable에 team_id 선택 필드 추가
  team_id가 있으면, 번들 매핑으로 해당 team_id에 속한 DAG만 Task SDK를 통해 접근할 수 있습니다.
  team_id가 없는 Connection과 Variable은 파싱 또는 실행되는 어떤 DAG도 접근할 수 있습니다.
* Pool에 team_id 선택 필드 추가
  team_id가 있으면 번들 매핑으로 같은 team_id인 DAG에서만 사용되어야 합니다.
  DAG File Processor는 다른 팀의 pool을 사용하는 DAG 파싱에 실패합니다.

### UI 변경

UI의 리소스 필터링은 AuthManager가 team_id 존재를 기반으로 수행합니다.
사용자에게 허용할 팀 접두사를 어떻게 결정할지는 AuthManager별로 구현되어야 합니다.
AuthManager가 제공하는 사용자는 하나 이상의 팀에 속할 수 있으며, UI의 모든 리소스에 대한 접근은 리소스가 속한 팀에 따라 결정됩니다.

### 팀별 배포

각 팀은 자체 보안 경계와 자체 설정으로 배포되므로, 배포의 다음 속성은 팀별로 정의할 수 있습니다.

* 팀별 의존성 집합(가능하면 컨테이너 이미지)
  팀에 속한 각 컴포넌트는 서로 다른 의존성 집합을 가질 수 있습니다.
* 팀별 credential, secrets manager 설정

### 배포 관리자 역할

멀티팀 Airflow 아키텍처에는 두 종류의 배포 관리자가 있습니다. Organisation Deployment Managers와 Team Deployment Managers입니다.

#### Organization Deployment Managers

Organization Deployment Managers는 전체 배포를 설계하고 구현할 책임이 있습니다.
팀을 정의하고 보안 경계를 어떻게 구현할지 정의하며, 팀 간 방화벽과 물리적 격리를 배치하고, 조직의 identity, authentication 시스템을 Airflow 배포와 연결하는 방법을 결정해야 합니다.

또한 공통 Airflow 설정, Metadata DB, Scheduler와 Webserver 실행 환경(필요 패키지와 플러그인, 보통 컨테이너 이미지) 관리, Scheduler와 Webserver 실행 관리도 담당합니다.
배포 설계는 보안 경계 간 적절한 격리를 제공해야 합니다.

이는 서로 다른 보안 경계에서 실행되는 워크로드의 물리적 격리뿐 아니라, 서로 다른 팀 경계 간 연결 규칙의 구현과 배치를 의미합니다.
규칙은 서로 다른 경계에서 실행되는 컴포넌트를 격리해야 하며, 경계 밖과 통신이 필요한 컴포넌트는 허용하되, 불필요한 통신은 차단해야 합니다.

예를 들어 팀 보안 경계 내부에서 실행되는 Internal API 또는 GRPC API 컴포넌트만 Metadata DB와 통신할 수 있도록 구성하는 것은 Organisation Deployment Manager의 책임입니다.
그 외 컴포넌트는 DB와 직접 통신하지 못해야 하며, 같은 보안 경계 내부의 Internal API 또는 GRPC API 컴포넌트와만 통신해야 합니다.

조직의 identity, authentication 시스템과 Airflow 통합은 두 영역에서 수행되어야 합니다.

* 조직 identity 시스템과 통합된 Auth Manager 구현
  운영 사용자가 특정 팀 리소스에 접근할 수 있도록 적절한 규칙을 적용해야 합니다.
  Airflow는 그런 Auth Manager의 특정 구현을 제공하지 않으며, 이 AIP도 이를 바꾸지 않습니다.
  권한 할당은 전적으로 Auth Manager 구현의 책임입니다.
  AIP-56으로 구현된 Airflow의 Auth Manager API는, 조직 특화 Auth Manager 구현이 결정을 내리는 데 필요한 정보를 제공합니다.
* DAG 작성자의 권한 구현
  Airflow는 팀별 DAG 폴더 접근 권한을 제한하는 메커니즘을 관리하지 않습니다.
  이는 오늘과 동일하게, Airflow가 DAG 폴더 전체 접근 권한 메커니즘을 추상화하기 때문입니다.
  팀 DAG 파일에 접근해야 하는 사용자만 접근하도록 규칙과 그룹 접근, 조직 identity, authentication, authorisation 시스템과의 통합을 정의하고 구현하는 것은 배포 관리자의 책임입니다.
  이를 선택하고 구현하는 것은 이 AIP 범위 밖입니다.
* 공통 설정에서 팀별 Executor 구성

Team Deployment Managers

Team Deployment Manager 역할은 다른 사람에게 부여될 수도 있고, Organization Deployment Managers가 수행할 수도 있습니다.
Team Deployment Manager의 역할은 팀의 설정과 실행 환경을 관리하는 것입니다.
즉 팀 실행 환경(공통 환경과 같은 Airflow 버전에서)에서 배포할 패키지와 플러그인 집합을 관리하고, 팀별 설정을 관리합니다.

또한 팀에 할당된 DAG 폴더 접근 관리에 관여할 수도 있지만, 범위와 방식은 이 AIP 범위 밖입니다.
Team Deployment Manager는 자신 팀의 Executor 집합을 독자적으로 결정할 수 없습니다.
그런 설정과 결정은 Organization Deployment Manager가 구현해야 합니다.

Team Deployment Manager는 태스크 처리 리소스를 제어할 수 있습니다.
예를 들어 Kubernetes Executor가 사용하는 Kubernetes 클러스터의 크기와 노드를 제어하거나, 팀 전용 Celery 큐를 처리하는 worker 노드 수를 제어하거나, 그 밖의 Executor 수신단 리소스(AWS Fargate 등)를 제어할 수 있습니다.

현재 AIP와 설정 상태에서는, Team Deployment Manager가 Executor 설정의 특정 부분(예: Kubernetes Pod template)을 바꾸려면 Organization Deployment Manager의 참여가 필요합니다.
다만 향후 Executor 변경을 통해 원격 팀 설정에서 그 설정을 유도할 수 있게 하는 것도 가능하며, 예를 들어 KPO template을 Kubernetes 커스텀 리소스로 배포하고 Executor가 이를 가져오도록 할 수도 있습니다.

Team Deployment Manager는 자신 팀 Executor에 할당할 리소스에 대해 Organization Deployment Manager와 합의해야 합니다.
현재 Executor는 Scheduler 프로세스 내부의 서브프로세스로 실행되므로, Executor 개별 리소스 사용량에 대한 제어가 적습니다.
후속 AIP로, 팀과 Executor별로 더 세밀한 리소스 제어를 구현할 수 있습니다.
