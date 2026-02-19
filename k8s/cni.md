# Kubernetes CNI 기본 개념 정리

## CNI(Container Network Interface)란?
- CNI는 런타임이 네트워크 플러그인을 호출해 컨테이너(파드) 네트워크를 구성하기 위한 규격이다. 런타임은 환경변수로 파라미터를 전달하고, stdin으로 JSON 설정을 주고, 성공 시 stdout으로 JSON 결과를 반환한다.
- Kubernetes 네트워크 모델을 구현하려면 CNI 플러그인이 필요하다.
- Kubernetes는 CNI 스펙 v0.4.0 이상 호환 플러그인을 사용해야 하며, v1.0.0 호환을 권장한다.
  - cniVersion과 플러그인이 지원하는 버전이 안 맞으면 버전 incompatible 오류 발생생

## 왜 사용할까?

- 각 Pod는 클러스터 전역에서 유니크한 IP를 가진다.
- 클러스터의 모든 Pod는 NAT 없이 서로를 볼 수 있고 직접 통신할 수 있다.
- Pod에 IP를 할당하고, Pod/노드 간 통신이 가능하도록 클러스터 네트워킹을 구성하는 역할을 네트워크 플러그인이 담당
- 이 요구를 만족시키는 구현체가 CNI 플러그인(또는 그와 동등한 네트워크 플러그인 구성)이다.

## CNI 호출 모델

### 플러그인 타입

- Interface 플러그인: 컨테이너 내부에 네트워크 인터페이스를 만들고 연결성을 보장
- Chained 플러그인: 이미 만들어진 인터페이스 설정을 조정하며, 필요 시 추가 인터페이스 생성도 가능

### 전달 방식

- 런타임 → 플러그인
  - 환경변수로 파라미터 전달
  - stdin으로 JSON 설정 전달
- 플러그인 → 런타임
  - 성공: stdout에 JSON 결과
  - 실패: stderr에 오류 출력 후 종료 코드로 종료

### 동작

- `ADD`: 컨테이너 네트워크에 추가한다(인터페이스 생성 또는 기존 인터페이스 조정), 성공 시 결과 구조를 stdout으로 출력
- `DEL`: 컨테이너 네트워크에서 제거
- `CHECK`: 현재 네트워킹이 기대대로인지 점검
- `GC`, `VERSION`: 정리/버전 지원 질의에 사용

## Kubernetes에서 누가 CNI를 로딩할까?

### 컨테이너 런타임 중심

- 컨테이너 런타임은 Kubernetes 네트워크 모델 구현에 필요한 CNI 플러그인을 로드하도록 구성되어야 한다.
- Kubernetes 1.24 이전에는 kubelet이 `cni-bin-dir`, `network-plugin` 커맨드라인 파라미터로 CNI 플러그인을 관리할 수 있었으나, 이 파라미터들은 Kubernetes 1.24에서 제거되었고 CNI 관리는 kubelet 범위 밖이 되었다.

## NetworkPolicy와 CNI

### NetworkPolicy

- NetworkPolicy는 L3/L4(IP/포트) 수준 트래픽 제어 규칙을 정의하는 리소스다.
- NetworkPolicy를 사용하려면 enforcement를 지원하는 네트워크 플러그인이 필요하다.
- 구현하는 컨트롤러가 없으면 NetworkPolicy 리소스를 만들어도 효과가 없다.

## CNI 플러그인 요구사항

### Loopback(`lo`)
- 네트워크 모델 구현용 CNI 플러그인 외에도, 컨테이너 런타임은 각 sandbox(파드 sandbox 등)에 loopback 인터페이스 `lo`를 제공해야 한다.

### hostPort 지원
- CNI 네트워킹 플러그인은 `hostPort`를 지원한다.
- `hostPort`를 쓰려면 CNI 설정에 `portMappings` capability를 지정해야 한다.

### 트래픽 셰이핑(실험 기능)
- CNI 네트워킹 플러그인은 Pod ingress/egress 트래픽 셰이핑도 지원한다.
- 트래픽 셰이핑을 쓰려면 CNI 설정 파일(기본 경로 `/etc/cni/net.d`)에 `bandwidth` 플러그인을 추가하고, CNI 바이너리 경로(기본 경로 `/opt/cni/bin`)에 바이너리가 포함되어야 한다.
- 이후 Pod에 `kubernetes.io/ingress-bandwidth`, `kubernetes.io/egress-bandwidth` 애노테이션을 추가해 사용한다.

## 영향이 큰가?

### CNI 플러그인 선택/구성이 직접 영향을 주는 범위

- Pod에 IP를 할당하는 주체가 네트워크 플러그인이므로, IP 대역/할당/연결성은 CNI 구성에 직접 좌우된다.
- NetworkPolicy는 플러그인이 enforcement 해야만 동작하므로, 보안/격리 요구가 있으면 플러그인 지원 여부가 기능 유무를 결정한다.
