
## Airflow 스케줄링 구조 개편: `execution_date` 문제 해결

### `execution_date`가 불러일으키는 오해
- 이름만 보면 실행 시간 같지만 아이러니 하게도 **작업이 실행되는 시점이 아님**
- **DAG가 처리해야 할 데이터 구간의 시작 시점**을 의미

#### 예시
```python
DAG(
    dag_id='test_dag',
    schedule_interval='@daily',
    start_date=datetime.datetime(2025, 11, 11),
)
```
- 위 DAG는 11월 11일을 시작일로 설정 했지만 **첫 실행은 11월 12일 자정**에 발생
- 하지만 이 실행의 `execution_date`는 **11월 11일** -> ???

---

### 왜 이런 구조인가?
- 전통적인 배치 처리 방식에서는 **기간이 지난 후 그 데이터를 처리하기 때문**
- 무슨 소리인가 하면, **작업 실행 시점과 대상 데이터 시점은 다르다는 뜻**
- 예를 들어 오후 11시 59분까지 운영하는 가게 매출을 정산한다고 가정하자 
  - 11월 11일에 발생한 매출은 당일에 바로 정산 할수 없다 12일에 정산이 가능하다
  → `execution_date = 2025-11-11`, 실제 실행 시점 = 2025-11-12 00:00:00


---

### AIP-39의 등장
참고) 공식 링크: [AIP-39](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-39%2BRicher%2Bscheduler_interval)

- `schedule_interval`이 **두 가지 개념을 동시에 표현**
  1. 스케줄 간격
  2. 데이터 타임 윈도우
- 이로 인해 작업 실행 시점과 대상 데이터 시점을 **정확히 분리할 수 없음**

---

### 핵심 개념 변화
execution_date → data_interval 기반 모델로 전환
#### 기존 → 새로운 변수 구조
| 기존 이름                         | AIP-39 이후 대체 변수               | 설명 |
|----------------------------------|------------------------------------|------|
| `execution_date`                | `logical_date`                     | DAG 실행의 논리적 시점 (기존 execution_date 의미 유지) |
| *(신규)*                        | `data_interval_start`             | DAG가 참조하는 데이터 범위의 시작 시점 |
| *(신규)*                        | `data_interval_end`               | DAG가 참조하는 데이터 범위의 종료 시점 (= logical_date) |
| `next_execution_date`           | `next_logical_date`               | 다음 DAG 실행의 논리적 시점 |
| `prev_execution_date`           | `prev_logical_date`               | 이전 DAG 실행의 논리적 시점 |
| `yesterday_ds`, `tomorrow_ds` 등 | deprecated                        | 날짜 문자열 매크로는 폐기 예정 (대체 방식 사용 권장) |


---

### Timetable 클래스 도입 – 유연한 스케줄 정의
기존 schedule_interval은 timedelta 또는 cron 표현식만 지원하여 

다음과 같은 복잡한 요구사항을 만족할 수 없었음
- 공휴일 제외
- 월말 마지막 영업일에만 실행
- 금융 거래일 기준 실행
- 사용자 지정 반복 규칙 등

Airflow 2.2부터, 사용자는 Timetable이라는 인터페이스를 상속받아 직접 스케줄링 로직을 구현 가능