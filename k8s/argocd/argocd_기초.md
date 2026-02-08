# Argo CD 기초

## **Argo CD란?**

**핵심 컨셉**
- **GitOps 도구:** Argo CD는 쿠버네티스를 위한 GitOps 도구이다.
- **작동 원리:** Argo CD는 Git과 쿠버네티스 사이에 위치하여, 사용자가 Git에 올린 리소스(Desired State)와 현재 쿠버네티스 클러스터의 상태를 지속적으로 비교한다.
- **Sync:** 두 상태 간에 차이가 감지되면, Git에 정의된 내용대로 쿠버네티스에 배포하는 과정을 수행하며 이를 '배포' 대신 **'Sync'**라고 부른다.

**주요 기능 및 장점**
- **멀티 클러스터 관리:** 하나의 Argo CD로 여러 개의 쿠버네티스 클러스터를 등록하여 동기화 할 수 있다.
  - 클러스터 정보는 **쿠버네티스 Secret**으로 관리된다.
  - **설정하기:** Secret에 `argocd.argoproj.io/secret-type: cluster` 라벨을 붙여야 Argo CD가 클러스터 설정으로 인식
  - API 서버 주소와 인증 정보를 포함한 Secret을 생성하면 등록
- **UI 와 CLI 제공**
  - 웹 UI의 경우 사용하기 편리하다는 장점이 있으나 모든 기능을 사용 할 수는 없다.
  - 이럴 때는 CLI를 사용하면 웹 UI보다 더 세밀한 제어가 가능하다.
- **보안 및 권한:** SSO(Single Sign-On) 연동을 통한 인증과 역할 별 권한 제어(RBAC)가 가능하다.
- **확장성 및 편의성**
    - REST API 및 gRPC를 지원하여 개발 연동 가능
    - Webhook을 통해 비즈니스 로직을 개입시킬 수 있다.
    - 운영 알림 설정 및 전용 CLI(`argocd`)를 제공
    - Helm과 Kustomize를 지원하여 관리 용이이

**주의 사항**
- **쿠버네티스 종속:** 쿠버네티스 네이티브 도구이므로 VM이나 물리 서버 등 쿠버네티스가 아닌 환경에는 배포할 수 없다.
- **버전 관리:** 버그 수정 등을 위해 최신 버전을 유지해야 한다.
- **삭제 주의!!** 
  - 별도의 옵션 없이 삭제하면 Argo CD 애플리케이션 객체와 그 앱이 관리하던 쿠버네티스 리소스(Pod, Service 등)가 **모두 삭제**된다.
  - 운영 중인 `Namespace`를 실수로 Argo CD에 등록했다가 앱을 삭제하면, **네임스페이스 자체가 삭제**되며 그 안의 모든 리소스가 날아가는 대형 장애가 발생할 수 있다.

> Argo CD를 위해서는 Helm도 잘알아야 한다. Argo CD와 Helm 도 버전 별로 버그가 은근많으니 release note를 항상 신경 쓰자

---

### **Argo CD 단위**

#### **Application**
- 가장 기본 단위이며, 어떤 Git 저장소에 있는 내용을 어떤 쿠버네티스 클러스터에 동기화할지 정의한 설정 묶음
- **구현 방식:** 쿠버네티스의 **CRD(Custom Resource Definition)**로 정의되어 있다. 즉, Argo CD의 어플리케이션도 결국 쿠버네티스 상에서는 하나의 리소스관리 된다는 뜻

#### **Project**
- 어플리케이션을 관리하고 그룹화하는 상위 단위
- **계층 구조**
  - **그룹화:** 여러 어플리케이션을 논리적으로 묶어서 관리하는 폴더와 같은 역할을 한다.
  - **권한 제어:** 프로젝트 단위로 배포 가능한 클러스터나 Git 저장소를 제한하는 등의 권한 설정을 할 수 있다.
    - **Source Repositories:** 특정 Git 저장소 URL만 사용하도록 제한 가능
    - **Destinations:** 배포 가능한 **쿠버네티스 클러스터**와 **네임스페이스**를 지정 (잘못된 곳에 배포를 방지지)
    - **Cluster Resource Whitelist/Blacklist:** 특정 리소스만 허용하거나, 특정 리소스의 생성을 차단

---

### **sync**
- Argo CD는 자동 또는 수동으로로 Git과 현재 클러스터 상태를 비교한다. 
- 상태 비교 결과 차이가 있다면 어플리케이션 상태가 **'Out of Sync'** (노란색)로 변경되고, 이때 동기화 할 수 있다.

**Refresh:** 기본적으로 주기적으로 상태를 비교하나 Refresh 버튼을 누르면 바로 상태를 비교할 수 있다.
**Sync Policy**
- **Manual (default):** 변경 사항이 있어도 사용자가 직접 `Sync` 버튼을 눌러야 배포된다.
- **Automatic:** 변경 사항(Out of Sync)이 감지되면 Argo CD가 자동으로 배포를 수행한다.

**주요 Sync 옵션**
- **Self-Heal:**
  - Auto Sync를 사용할 때 활성화할 수 있는 옵션이다.
  - 누군가 `kubectl` 등으로 클러스터 리소스를 직접 수정하더라도, Argo CD가 즉시 Git에 정의된 상태로 되돌려 **Git의 상태를 항상 보장**한다.
- **Prune (리소스 삭제):**
  - Git에서 리소스 파일을 삭제했을 때, 실제 클러스터에서도 해당 리소스를 삭제할지 결정한다.
  - **기본값은 비활성화(Disabled)**이므로, Git에서 파일을 지워도 클러스터에는 리소스가 남아있게 됩니다. Git과 클러스터를 완벽히 일치시키려면 이 옵션을 켜야 한다.

**Status**
- **Sync Status:** Git과 클러스터의 설정 일치 여부 (Synced / Out of Sync).
- **Health Status:** 리소스의 동작 상태 (Healthy, Missing, Progressing, Degraded)

**Sync Lifecycle**
- Argo CD의 Sync 과정은 크게 3단계로 나누어 실행된다.
- **Pre-Sync:** 실제 리소스 배포 전에 실행되며, 주로 데이터베이스 스키마 마이그레이션, 데이터 백업 등의 작업에 사용
- **Sync:** 사용자가 정의한 애플리케이션 리소스가 배포되는 단계계
- **Post-Sync:** 배포가 성공적으로 끝난 후에 실행된다. 주로 슬랙/이메일 알림 발송, 로드밸런서 등록, 헬스 체크 등의 작업에 사용

---

## **helm 차트와 kustomize**

### Helm
**Helm 차트 연동하기**
- **Helm Repository:** `Source Type`을 Helm으로 선택하고 차트 저장소 URL과 차트명/버전을 지정
- **Git Repository:** 일반 Git 연동처럼 하되, `Chart.yaml`이 있는 경로를 지정하면 자동으로 Helm 앱으로 인식한다.

**Values Override하기**
- UI의 `PARAMETERS` 탭에서 값을 직접 수정하거나, Git에 있는 별도의 `values` 파일(예: `values.yaml`)을 지정하여 덮어쓸 수 있다.

**내부 동작 방식 (중요)**
- Argo CD는 `helm install`을 쓰지 않고, **`helm template`**으로 렌더링한 후 `kubectl apply`를 수행한다.
- 따라서 클러스터에서 `helm ls`로 조회되지 않으며, Helm의 자체 라이프사이클 명령어(upgrade, rollback 등)는 사용할 수 없다.

### Kustomize
**Kustomize 기본 사용법**
- Git 경로에 `kustomization.yaml` 파일이 있으면 Argo CD가 자동으로 Kustomize 앱으로 인식
- 내부적으로 `kustomize build` 후 적용하는 방식

### 차이점
- K8s 리소스를 관리할 때 **Helm**과 **Kustomize**는 가장 많이 언급되는 도구이며, **"Template 방식이냐, 덮어쓰기(Overlay) 방식이냐"**의 차이가 있다.

#### 1. 주요 차이점 비교

| 구분 | Helm | Kustomize |
| --- | --- | --- |
| **방식** | **Template** | **Overlay** |
| **핵심 개념** | YAML 내부에 `{{ .Values.name }}` 같은 변수를 심음 | 원본 YAML은 그대로 두고, 변경할 부분만 덧칠함 |
| **제어 로직** | `if/else`, `range(반복문)` 등 프로그래밍 로직 가능 | 로직 없음, YAML Merge와 Patch |
| **설치 및 배포** | 별도 클라이언트(Helm CLI) 설치 필요 | **`kubectl`에 내장**되어 있어 별도 설치 불필요 |
| **복잡도** | 초기 학습 곡선이 높지만 강력함 | 직관적이고 단순함 |

#### ArgoCD와 함께 쓸 때는 뭐가 좋을까?
- ArgoCD는 **두 가지 방식 모두 완벽하게 지원**하며 실제 실무에서는 섞어 쓰는 경우가 많다.

1. **오픈소스 설치 (Airflow 등):** 이미 잘 만들어진 **Helm Chart**를 쓴다.
2. **자체 서비스 관리:** 우리 회사가 만든 간단한 API 서버 등은 관리가 편한 **Kustomize**를 선호하기도 함
