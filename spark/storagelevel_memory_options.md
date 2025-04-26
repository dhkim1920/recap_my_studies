
## persist(StorageLevel.MEMORY_ONLY_SER())

- Spark RDD나 DStream에 적용하는 저장(Storage) 메서드
- 메모리에 직렬화(Serialized) 형태로만 저장하는 옵션

## 주요 특징

| 항목 | 설명 |
|:-----|:-----|
| 저장 위치 | 메모리(RAM) |
| 저장 방식 | 직렬화(Serialized) 형태로 저장 |
| 복구 속도 | 빠름 (메모리 접근) |
| 메모리 사용량 | 작음 (일반 객체 저장보다 훨씬 압축됨) |
| 디스크 백업 | 없음 (메모리 부족 시 RDD 재계산 필요) |
| 사용 목적 | 메모리 최적화가 필요한 경우 |

## 왜 MEMORY_ONLY_SER()를 쓰는가?

- 일반 MEMORY_ONLY는 Java 객체 형태로 저장해서 메모리를 많이 차지함
- MEMORY_ONLY_SER()는 직렬화된 상태로 저장하여 메모리 사용량이 훨씬 적음
- 대신 직렬화/역직렬화 비용 때문에 CPU 부하는 약간 증가할 수 있음

## 기본 사용 예시
```java
rdd.persist(StorageLevel.MEMORY_ONLY_SER());
dstream.persist(StorageLevel.MEMORY_ONLY_SER());
```

- 이후 해당 RDD/DStream은 첫 계산 이후 메모리에 직렬화된 형태로 저장됨
- 재사용 시 계산 없이 메모리에서 직접 읽음

## 주의사항

- 메모리에 저장할 수 없을 정도로 크면 디스크로 가지 않고 RDD를 다시 계산함
- 직렬화/역직렬화 오버헤드가 있기 때문에 빈번한 접근에는 MEMORY_ONLY가 더 빠를 수 있음
- 데이터 크기가 크거나 메모리 자원이 부족한 경우에 MEMORY_ONLY_SER가 유리

---

## persist(StorageLevel.MEMORY_AND_DISK_SER())

- Spark RDD나 DStream을 메모리에 직렬화(Serialized) 형태로 저장하고
- 메모리가 부족하면 디스크에도 저장하는 옵션

## 주요 특징

| 항목 | 설명 |
|:-----|:-----|
| 저장 위치 | 우선 메모리, 부족하면 디스크 |
| 저장 방식 | 직렬화(Serialized) 형태로 저장 |
| 복구 속도 | 메모리에 있으면 빠름, 디스크에 있으면 느림 |
| 메모리 사용량 | 직렬화된 데이터 저장으로 최적화 |
| 디스크 백업 | 있음 (메모리 부족 시 디스크 저장) |
| 사용 목적 | 메모리에 다 못 올라가는 큰 데이터 처리 |

## 왜 MEMORY_AND_DISK_SER()를 쓰는가?

- 메모리에 다 올라가지 않는 경우 일부 데이터를 디스크에 저장하여 재계산 없이 복구
- MEMORY_ONLY_SER()는 메모리 부족 시 재계산이 필요한 반면, MEMORY_AND_DISK_SER()는 디스크에서 읽어옴
- 직렬화 상태로 메모리 절약 + 디스크 안정성 확보

## 기본 사용 예시
```java
rdd.persist(StorageLevel.MEMORY_AND_DISK_SER());
dstream.persist(StorageLevel.MEMORY_AND_DISK_SER());
```

---

## StorageLevel 비교

| 항목 | MEMORY_ONLY | MEMORY_AND_DISK | MEMORY_ONLY_SER | MEMORY_AND_DISK_SER |
|:-----|:------------|:----------------|:----------------|:--------------------|
| 저장 위치 | 메모리 | 메모리 → 디스크 | 메모리(직렬화) | 메모리(직렬화) → 디스크 |
| 저장 방식 | 객체(Java 오브젝트) | 객체(Java 오브젝트) | 직렬화(Serialized) | 직렬화(Serialized) |
| 메모리 사용량 | 큼 | 큼 | 작음 | 작음 |
| 디스크 저장 여부 | 없음 (메모리 부족 시 재계산) | 있음 (디스크 저장) | 없음 (메모리 부족 시 재계산) | 있음 (디스크 저장) |
| 재계산 필요성 | 메모리 부족 시 필요 | 없음 (디스크 복구) | 메모리 부족 시 필요 | 없음 (디스크 복구) |
| CPU 부하 | 낮음 | 낮음 | 높음 (직렬화/역직렬화) | 높음 (직렬화/역직렬화) |
| 사용 추천 상황 | 데이터 크기가 작고 메모리가 충분할 때 | 데이터 크기가 크고 일부 디스크 사용 허용할 때 | 메모리 최적화가 필요할 때 | 메모리 부족+안정성 둘 다 필요할 때 |

---

## 요약

- **MEMORY_ONLY**: 메모리 여유 충분하면 가장 빠름
- **MEMORY_AND_DISK**: 메모리 부족 대비 안전
- **MEMORY_ONLY_SER**: 메모리 아낄 수 있지만 CPU 부하 약간 있음
- **MEMORY_AND_DISK_SER**: 메모리 최적화 + 디스크 백업 둘 다 필요한 경우
