
# HBase 키 설계 
## 1. RowKey는 정렬 기준
- HBase는 RowKey 기준으로 사전순 정렬
- 조회 성능은 RowKey 설계에 크게 의존한다.
- 스캔 효율을 위해 **조회 패턴에 맞는 정렬** 구조로 설계해야 한다. 

## 2. Hotspot(쓰기 병목) 방지
### 문제
- 시간 순 정렬 RowKey 사용 시 특정 Region에 쓰기 집중 → 병목 발생

### 해결 방법
- **해시 기반 prefix**: `00_user123`, `01_user123` 등으로 앞단 분산
- **reverse timestamp**: 최신 데이터가 앞에 오게 하여 read latency 개선
- **UUID 사용**: 랜덤 키라 분산에 유리하지만 범위 조회가 어려움 
  - hbase는 범위 조회용이 아니어서 느리긴하지만 가능한다. 단 UUID같이 랜덤키로 분산하면 범위 조회가 사실상 불가능하다.

## 3. 시간 기반 RowKey 설계
### 최근 데이터 조회 특성
- 대부분 로그/시계열 데이터는 최근 데이터만 조회 (예: 실시간 모니터링)

### 시간 위치 주의사항
- 시간 값을 RowKey 앞에 두면 새로운 데이터가 하나의 Region에 집중됨 → **Hotspot 발생**
- 시간은 **RowKey 중간 또는 뒤쪽**에 배치해야 분산 가능

### 시간 표현 방식
- **문자열 시간 (지양)**: padding 오류, 정렬 부정확, 범위 조회 어려움
- **숫자 시간 (권장)**: Unix epoch time (ms) 사용  
  → 정렬 자연스럽고 범위 필터링 쉬움, 공간 효율 좋음

## 4. 스캔 범위 최적화
### 설계 원칙
- 자주 사용하는 필터 조건을 RowKey에 포함시켜 범위 스캔 유도

### 예시
- `userId_timestamp`: 특정 사용자 로그
- `regionId_storeId_date`: 지역·매장 분석 등

## 5. 고정 길이 및 복합 키 사용
- 정렬/압축/저장 효율 향상을 위해 고정 길이 권장
  - 숫자에는 zero-padding 적용 (예: `order_0001234567`)
- 여러 필드를 조합한 **복합 RowKey** 사용
  - 예: `지역코드_매장ID_날짜시간`
  - 사용 패턴에 맞게 구성


## 6. 추천 RowKey 설계 패턴
### 패턴 1 – 시계열 로그 (분산도 보장)
```
[해시(user_id)]_[user_id]_[epoch_ms]
```
- 해시 prefix로 Region 분산
- user_id로 필터링
- epoch_ms로 시간 범위 쿼리

### 패턴 2 – 센서 데이터
```
[device_id]_[epoch_ms]
```
- 디바이스 기준 조회
- 시간 순서 보장

## 7. 최종 정리

| 설계 요소     | 권장 방식             | 이유                              |
|---------------|------------------------|-----------------------------------|
| 시간 위치     | RowKey 뒤쪽 또는 중간 | Hotspot 방지                      |
| 시간 포맷     | Epoch time (ms)        | 정렬, 범위 조회 쉬움              |
| 문자열 사용   | 지양 (특히 시간은 숫자) | 등가 비교만 되고 범위 검색 어려움 |
| 데이터 분산   | Prefix에 해시 추가 등  | Region 간 로드 분산               |

## 8. 주의할 점

- RowKey가 너무 길면 저장 비효율, 100바이트 이내 권장
  - HBase는 row key를 메모리에 인덱싱하며, 크면 클수록 Java heap, block index 등에 부담을 주게된다.
  - 네트워크 비용 및 읽고 비교하는 오버헤드가 커진다.
- salt는 적절히 조절해야 키 조합 복잡도 증가 방지
- 버저닝 설정 미사용 시 동일 RowKey 덮어쓰기 주의
- Secondary Index 없음: 컬럼 기반 조회는 인덱스 테이블 별도 설계 필요
- Column Family는 자주 함께 접근되는 컬럼 단위로 묶되, 너무 많으면 리소스 부담

> 참고) 
> 100 Byte 기준은 초창기 HBase RowKey 구현 클래스에서 100 Byte를 넘으면 발생하는 
> 불필요한 패딩으로 인한 성능 저하 때문에 기준이 된거 같다. 0.x 버전 때 얘기로 그 후에는 클래스가 바꼈다.