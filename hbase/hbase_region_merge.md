# HBase Region 병합 정리 (Adjacent vs Non-Adjacent)

## 기본 원칙: Adjacent Region 병합만 허용
- 기본적으로 HBase는 **인접한 Region 간에만 병합을 허용**한다.
- **조건**: 하나의 Region의 End Key가 다른 Region의 Start Key와 정확히 일치해야 한다.

## Non-Adjacent Region 병합 (강제)
- `merge_region` 명령어의 세 번째 인자에 `true`를 전달하면 **강제로 병합 가능**
```bash
hbase> merge_region 'ENCODED_REGIONNAME1', 'ENCODED_REGIONNAME2', true
```
- 그러나, 비인접 Region을 병합할 경우 **키 범위 겹침(overlapping)** 문제가 발생할 수 있으므로 **권장되지 않음**

## 키 범위 겹침 시 발생하는 문제

| 영향 범위          | 상세 내용 |
|--------------------|-----------|
| 데이터 일관성 오류 | 동일 RowKey가 여러 Region에 존재할 수 있어, 읽기/쓰기 시 충돌 발생 |
| 메타테이블 오류    | `hbase:meta` 테이블이 중복된 키 범위를 참조 → Region 위치 오류 발생 |
| 시스템 불안정      | RegionServer 간 Region 충돌로 인해 서버 다운 또는 불안정 상태 초래 |
| hbck 자동 복구 불가 | HBase 2.0 이후 `hbck` 도구는 겹치는 Region에 대해 자동 복구 기능 제한 |

## 권장 사항 및 병합 전 고려 사항

- **항상 인접 Region만 병합** (기본 방식)
- 비인접 Region 병합 시에는 **명확한 키 범위 확인 후 사용**
- 병합 전 각 Region의 **StartKey / EndKey** 수동 확인 필수
- 자동 병합을 수행하는 **Normalizer 설정**을 검토하여 비인접 병합이 일어나지 않도록 제한하거나 비활성화

## 관련 명령 요약

| 명령어 | 설명 |
|--------|------|
| `merge_region region1 region2` | 인접 Region 병합 (기본) |
| `merge_region region1 region2 true` | 비인접 Region 강제 병합 (위험) |

## 요약

- HBase는 키 범위가 겹치지 않는 구조를 유지해야 하며, 이를 위반하면 **데이터 정합성·시스템 안정성 모두 위험**
- 강제 병합 기능은 존재하지만, 운영 환경에서는 **신중하게 사용하거나 회피하는 것이 최선**