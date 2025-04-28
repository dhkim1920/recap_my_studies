# HDFS Block 깨짐 (Missing Block / Corrupt Block) 정리

## Block 기본 개념
- HDFS는 파일을 Block 단위(기본 128MB 또는 256MB)로 나누어 저장
- 각 Block은 기본적으로 3개 복제본(replica)으로 분산 저장

---

## Missing Block vs Corrupt Block

| 구분 | 설명 |
|:---|:---|
| Missing Block | 클러스터 어디에도 복제본이 없는 Block (완전 손실, 복구 불가) |
| Corrupt Block | 복제본 중 일부가 손상된 Block (남은 복제본으로 복구 가능) |

- **Missing Block**: 모든 복제본이 사라짐 → 복구 불가능
- **Corrupt Block**: 일부 복제본만 손상 → 복구 가능 (남은 복제본으로 자동 복제)

---

## 주요 발생 원인
- 파일시스템 마운트 누락 (ex. 디스크 unmount)
- 데이터노드 장애 또는 다운
- 파일시스템 재포맷
- 디스크 물리적 손상
- 다수의 데이터노드 장애로 복제본 손실

---

## 복구 방법

### 1. 상태 확인
```bash
hdfs fsck / -list-corruptfileblocks
```
- 손상된 파일, 블록 목록 출력

### 2. 복구 명령어
- Corrupt Block 이동 및 복구
```bash
hdfs fsck / -move
```
- 완전히 삭제
```bash
hdfs fsck / -delete
```

※ Missing Block은 소스 데이터로 재생성하거나, 백업에서 복원하는 수밖에 없음

---

## 주의사항
- Corrupt Block은 자동 복구될 수도 있지만, Missing Block은 복구가 안 됨
- 데이터센터 장애처럼 다수 노드 장애 시, 복제본 부족으로 Missing Block 발생할 수 있음
