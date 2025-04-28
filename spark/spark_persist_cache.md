
# Spark persist vs cache

## 1. cache()

- DataFrame, RDD를 메모리에 저장 (기본 MEMORY_AND_DISK)
- lazy하게 동작 (action 실행 시 캐싱)
- 재사용 시 다시 계산하지 않고 메모리/디스크에서 읽음

**사용법**
```python
df.cache()
```

**특징**
- 메모리 초과 시 디스크 저장
- 자주 접근하는 데이터의 성능 대폭 향상
- cache 호출 후 count(), collect() 같은 action으로 강제 materialization 수행
  - cache 호출 시에는 메모리에 올라가는게 아니고 action에 올라간다는 말

---

## 2. persist()

- DataFrame, RDD를 특정 StorageLevel로 저장
- cache()보다 세밀한 저장 옵션 제어 가능

**사용법**
```python
df.persist(StorageLevel.MEMORY_ONLY)
df.persist(StorageLevel.MEMORY_AND_DISK_SER)
```

## persist StorageLevel 주요 특징

| StorageLevel | 메모리 부족 시 동작 | 직렬화 여부 |
|:-------------|:------------------|:------------|
| MEMORY_ONLY | 다시 계산 | 직렬화 안 함 |
| MEMORY_AND_DISK | 디스크 복구 | 직렬화 안 함 |
| MEMORY_ONLY_SER | 다시 계산 | 직렬화 함 |
| MEMORY_AND_DISK_SER | 디스크 복구 | 직렬화 함 |
| DISK_ONLY | 디스크 읽음 | 직렬화 함 |

**특징 요약**
- MEMORY_ONLY: 빠르지만 메모리 초과 시 다시 계산
- MEMORY_AND_DISK: 안정적, 디스크 백업
- MEMORY_ONLY_SER: 메모리 절약, CPU 부하 증가
- MEMORY_AND_DISK_SER: MEMORY_ONLY_SER 절충안
- DISK_ONLY: 메모리 부담 없음, 느림

## persist(StorageLevel.MEMORY_ONLY_SER())

- 메모리에 직렬화(Serialized) 형태로만 저장
- 일반 MEMORY_ONLY는 Java 객체 형태로 저장해서 메모리를 많이 차지함
- MEMORY_ONLY_SER()는 직렬화된 상태로 저장하여 메모리 사용량이 훨씬 적음
- 대신 직렬화/역직렬화 비용 때문에 CPU 부하는 약간 증가할 수 있음

**사용법**
```java
rdd.persist(StorageLevel.MEMORY_ONLY_SER());
dstream.persist(StorageLevel.MEMORY_ONLY_SER());
```

**주의사항**
- 메모리 부족 시 디스크 저장 없이 다시 계산
- 직렬화/역직렬화 오버헤드가 있기 때문에 빈번한 접근에는 MEMORY_ONLY가 더 빠를 수 있음

## persist(StorageLevel.MEMORY_AND_DISK_SER())

- 메모리에 직렬화 형태로 저장, 부족하면 디스크에도 저장

**사용법**
```java
rdd.persist(StorageLevel.MEMORY_AND_DISK_SER());
dstream.persist(StorageLevel.MEMORY_AND_DISK_SER());
```

**특징**
- 메모리 최적화 + 안정성 확보 (디스크 복구 가능)

---

## cache() vs persist() 차이

| 항목 | cache() | persist() |
|:-----|:--------|:----------|
| 저장 방식 | MEMORY_AND_DISK 고정 | 다양한 StorageLevel 선택 가능 |
| 사용 목적 | 간편한 캐싱 | 메모리 최적화, 디스크 활용 등 세밀 제어 |
| 호출 시점 | lazy (action 시 저장) | lazy (action 시 저장) |

---


## unpersist() vs checkpoint()

| 항목 | unpersist() | checkpoint() |
|:-----|:------------|:-------------|
| 목적 | 캐싱 데이터 해제 | 데이터 복구 지점 저장 |
| 사용 시기 | 캐시가 불필요할 때 | 긴 lineage 끊기 위해 |
| 저장 위치 | 메모리/디스크 캐시 제거 | 디스크(HDFS 등) 저장 |
| 비용 | 빠름 (해제) | 느림 (파일 저장) |
| 장점 | 메모리 회수 | 장애 복구, lineage 최적화 |

---

# 요약

- `cache()`: 간단한 메모리/디스크 캐시
- `persist()`: 세밀한 저장 방식 선택
- `unpersist()`: 캐시 해제
- `checkpoint()`: 장애 복구와 lineage 최적화용 스냅샷 저장

---

# 추가 팁

- 장기 실행하는 작업은 중간에 checkpoint() 추천
- cache() 후 unpersist() 하지 않으면 메모리 누수 위험
