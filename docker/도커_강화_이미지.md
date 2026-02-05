# Docker Hardened Images (DHI)

## 개요
Docker Hardened Images(DHI)는 Docker에서 직접 보안 강화를 위해 빌드하고 유지하는 공식 이미지다.
보안 취약점을 최소화하고, 운영 환경에서의 안정성을 높이기 위해 설계되었다고 한다.

## 기존 이미지와의 차이는 무엇일까??
| 항목 | 기존 Docker 이미지 | Docker Hardened Images |
|------|---------------------|------------------------|
| 제작자 | 커뮤니티/조직 | Docker Inc. |
| 보안 책임 | 사용자 | Docker |
| 접근성 | 쉘 접근 가능 | 쉘 접근 불가 |
| 관리방식 | 직접 패치 필요 | Docker가 자동 패치 |
| 투명성 | Dockerfile 열람 가능 | SBOM/VEX 제공 (검증 가능) |

## 주요 특징

- **공격 표면 감소**: 불필요한 구성 요소 제거로 최대 95% 감소
- **보안 취약점 최소화**: CVE 제로 상태 유지, 7일 이내 패치
- **투명성 보장**: SBOM, VEX, SLSA Build Level 3, 디지털 서명 제공
- **운영 편의성**: Dockerfile 한 줄만 수정하면 기존 워크플로우 호환
- **런타임 보안 강화**: 셸, 패키지 매니저, 디버깅 도구 제거

> 참고) CVE (Common Vulnerabilities and Exposures)란? 
> 알려진 보안 취약점들을 식별하고 공유하기 위한 표준화된 고유 식별 번호 시스템

## 운영 시 고려사항

- **접근 제한**: `bash`, `sh`, `yum`, `apt` 등 사용 불가
- **대안 제공**: `docker debug`, 로그 외부화, 헬스체크, 메트릭 수집, 사이드카 패턴
- **런타임 디버깅 제약**: 운영팀의 기존 습관 변경 필요

## 실용적 사용 방식

### 개발 환경 예시

```dockerfile
FROM docker.io/hardened/python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
```

### 운영 환경
- 셸 제거 상태로 실행
- 필요한 도구는 빌드 시점에 포함
- 외부 로그 수집, 헬스체크 등으로 운영

## 결론
- Docker Hardened Images는 보안에 초점을 맞춘 공식 이미지
- 기존 운영 방식과의 차이가 존재하나, 보안 강화가 필요한 프로덕션 환경에서 특히 유용