# RDBMS vs Apache Iceberg: 스키마 진화 비교

## 스키마 진화 항목 비교

| 항목 | RDBMS | Apache Iceberg |
|------|--------|----------------|
| 컬럼 추가/삭제 | O | O |
| 컬럼 이름 변경 | O (제약 있음) | O (이름 매핑 유지) |
| 컬럼 순서 변경 | 보통 안됨 | O |
| 파티션 스키마 변경 | 보통 제약 많음 | O |
| 과거 쿼리에서 과거 스키마 유지 | ✖ | O (Snapshot별 스키마 유지) |
| 물리 데이터 재정렬 필요 여부 | 있음 | 없음 (append-only 구조) |

## Iceberg의 스키마 진화 특징

- 컬럼 추가/삭제/이름 변경/순서 변경 모두 가능
- 스냅샷별 스키마 버전 관리
  - 과거 스냅샷은 그 시점의 스키마로 유지됨
  - Time Travel 시, 해당 시점의 컬럼 구조도 같이 조회됨
- 메타데이터만 수정
  - Parquet 등 실제 데이터 파일은 수정하지 않음
  - 새로운 스냅샷에서만 새로운 스키마 적용됨
- Schema ID로 컬럼 추적
  - 컬럼 이름이 아니라 내부 ID 기반으로 추적
  - 이름이 바뀌어도 같은 컬럼으로 인식 가능
  
## 예시
```sql
ALTER TABLE sales ADD COLUMN refund_reason STRING;
ALTER TABLE sales RENAME COLUMN name TO customer_name;
```

- 위 변경은 새로운 스냅샷부터 적용됨
- 이전 데이터는 기존 스키마 유지됨

## 결론
- Iceberg의 스키마 진화는 RDBMS보다 유연하고, 변경 이력 관리에 강점을 가짐
- 스냅샷 기반 버전 관리 + 분산 저장 환경에 최적화됨
- RDBMS도 일부 지원하지만, Iceberg는 시간과 스키마 버전을 함께 관리하는 것이 본질적 차이