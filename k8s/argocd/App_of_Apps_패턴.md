# App of apps 패턴턴

## 구조적 정의
- 공식 문서에서는 이를 **'하나의 단위로 여러 앱을 관리하는 방법'**으로 정의한다.
- **메커니즘:** Root Application이 특정 Git 레포지토리의 경로를 바라보게 한다. 그 경로 안에는 실제 서비스가 아니라, **Argo CD `Application` CRD 파일들**이 들어있다.
- **작동 원리:** Argo CD가 부모 앱을 배포하면, 그 안에 들어있던 자식 `Application`들이 클러스터에 등록되고, 그때서야 비로소 자식 앱들이 각각의 서비스를 배포하기 시작

## Sync & Prune
- 이 패턴은 root 앱의 `Automated Sync Policy` 설정이 자식 앱에 큰 영향을 준다.
- **Prune 활성화 시:** Git 리포지토리에서 자식 앱의 YAML 파일을 삭제하고 부모를 Sync하면, Argo CD에서 해당 자식 앱이 **즉시 제거**된다.
- **Self-Heal:** 자식 앱의 설정을 누군가 수동으로 클러스터에서 건드려도, 부모 앱이 이를 감지하여 다시 Git 상태로 되돌린다.

## 삭제 시의 위험성 
- 삭제 시 연쇄 반응과 주의사항은 [Non-cascade.md](Non-cascade.md) 문서를 참고

## Best Practices)

| 항목 | 권장 설정 | 이유 |
| --- | --- | --- |
| **Project 분리** | 부모와 자식을 다른 Project로 관리 | 권한 제어 및 보안 강화 |
| **Namespace** | 자식 앱들은 각자의 Namespace 지정 | 부모 앱이 있는 `argocd` 네임스페이스와 격리 |
| **SyncPolicy** | 부모 앱은 `Manual` 혹은 신중한 `Auto` | 연쇄 삭제 사고 방지를 위해 부모 앱의 수정은 신중해야 함 |

