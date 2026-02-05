# `sqlline.py` vs `sqlline-thin.py` 비교

## 1. 연결 방식

| 항목 | sqlline.py | sqlline-thin.py |
|------|------------|-----------------|
| 연결 대상 | HBase 직접 연결 | Phoenix Query Server(PQS) 통해 연결 |
| 프로토콜 | Phoenix JDBC (Thick Client) | Avatica over HTTP (Thin Client) |
| 경로 | `bin/sqlline.py` | `bin/sqlline-thin.py` |

- **Thick Client**: JDBC 기반, Phoenix가 직접 HBase와 통신
- **Thin Client**: PQS를 통해 Avatica 프로토콜로 간접 통신

## 2. 네트워크 요구사항

| 항목 | sqlline.py | sqlline-thin.py |
|------|------------|-----------------|
| 접근 대상 | HBase 클러스터 내부 노드 | PQS (기본 포트: 8765) |
| 보안/방화벽 고려 | 클러스터 모든 노드 허용 필요 | PQS 단일 포트만 열면 됨 |

- `sqlline.py`: 내부 네트워크 또는 VPN 필요
- `sqlline-thin.py`: PQS에만 접근 가능하면 외부에서도 연결 가능

## 3. 클라이언트 풋프린트 (의존성)

| 항목 | sqlline.py | sqlline-thin.py |
|------|------------|-----------------|
| 의존성 | Full Phoenix 클라이언트 필요 | 최소한의 JAR만 필요 |
| 배포 난이도 | 복잡 | 간단 |

- `sqlline.py`: phoenix-client 포함된 전체 배포 필요
- `sqlline-thin.py`: avatica-client만으로도 동작 가능

## 결론
- **로컬에서 테스트하거나 클러스터 접근 가능한 경우**: `sqlline.py`
- **보안망 외부 또는 경량화된 클라이언트 환경**: `sqlline-thin.py` + PQS

