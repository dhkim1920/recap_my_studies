# Salted Tables

HBase는 RowKey가 단조 증가(monotonically increasing)할 경우, 순차적 쓰기(sequential write)로 인해 특정 Region Server에 데이터가 몰리는 핫스팟(hotspotting) 문제가 발생할 수 있습니다.  
RowKey에 Salt를 추가하는 방법은 이 문제를 완화할 수 있습니다. 자세한 방법은 별도 링크에 설명되어 있습니다.

Phoenix는 테이블 생성 시, RowKey에 투명하게(silently) 1바이트 Salt를 추가하는 방법을 제공합니다.  
테이블을 만들 때 `"SALT_BUCKETS"` 속성에 1에서 256 사이의 값을 설정해야 합니다. 예를 들면 다음과 같습니다:

```sql
CREATE TABLE table (a_key VARCHAR PRIMARY KEY, a_col VARCHAR) SALT_BUCKETS = 20;
```

Salted 테이블을 사용할 때 알아야 할 주의사항과 동작상의 차이점들이 있습니다.

## Sequential Scan (순차 스캔)

Salted 테이블은 데이터를 순서대로 저장하지 않기 때문에, 순차적 스캔(sequential scan)을 해도 원래 자연스러운 정렬 순서대로 결과가 반환되지 않습니다.  
예를 들어 `LIMIT` 절을 사용해 강제 순차 스캔을 하면, 일반 테이블과 다른 순서의 결과를 받을 수 있습니다.

## Splitting (스플리팅)

테이블 생성 시 Split Point를 명시하지 않으면, Salted 테이블은 각 Salt 바이트 경계마다 미리 분할(pre‑split)됩니다.  
이렇게 해서 테이블 생성 초기부터 Region Server 간에 부하가 균등하게 분산됩니다.  
사용자가 수동으로 Split Point를 제공할 경우, **Salt Byte**를 포함해서 Split Point를 지정해야 합니다.

## Row Key Ordering (RowKey 정렬)

Pre‑split을 하면 하나의 Region Server에 저장된 모든 엔트리의 시작이 동일한 Salt Byte로 맞춰지게 되어, Region 안에서는 정렬 상태가 유지됩니다.  
이 구조 덕분에 병렬 스캔(parallel scan)을 할 때 클라이언트 측에서 Merge Sort를 수행해 결과를 다시 정렬할 수 있습니다.  
결국, 일반 테이블과 같이 정렬된 순서로 데이터를 받을 수 있습니다.

`hbase-site.xml` 파일에서 `phoenix.query.rowKeyOrderSaltedTable` 값을 `true`로 설정하면 이 RowKey 순서 스캔 기능이 활성화됩니다.  
이 설정을 켜면 Salted 테이블에 사용자 정의 Split Point를 허용하지 않으며, 각 버킷에는 동일한 Salt Byte의 데이터만 들어가게 강제합니다.  
이때는 Salted 테이블도 일반 테이블처럼 RowKey 순서로 결과를 반환합니다.

## Performance (성능)

Salted 테이블과 미리 스플릿된 구조를 사용하면, 전체 Region Server에 쓰기 부하가 고르게 분산됩니다.  
그 결과, 쓰기 성능이 향상됩니다. Phoenix 자체 테스트 결과, Salted 테이블은 Non‑Salted 테이블에 비해 쓰기 처리량이 **80%** 증가했습니다.

또한 읽기 성능도 데이터가 고르게 분포되면서 이점을 얻습니다.  
특히 데이터의 일부(subset)를 대상으로 하는 쿼리에서는 Salted 테이블이 Non‑Salted 테이블에 비해 읽기 성능이 상당히 개선되었습니다.
