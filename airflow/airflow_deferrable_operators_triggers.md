
# Airflow Deferrable Operators와 Triggers

> 아래 문서들을 통합하여 정리한 내용입니다.  
> https://notebooklm.google.com/notebook/3f290bc9-005b-4591-a3f4-d6ead15369ad  
> https://www.astronomer.io/docs/learn/deferrable-operators

## 개요
- Deferrable Operators는 작업이 외부 리소스(예: API 응답, 클러스터 작업 완료, 파일 생성)를 “기다리는 동안” 워커 슬롯을 계속 점유하지 않도록 설계된 실행 방식이다.
- 대기 구간에 작업은 스스로 실행을 멈추고 워커 슬롯을 해제(defer)하며, 이후 대기/폴링은 triggerer가 실행하는 trigger가 담당한다. 조건이 충족되면 트리거가 이벤트를 발생시키고, 작업은 다시 진행된다.

※ 참고) 이 문서에서 지연 가능(deferrable), 비동기(async/asynchronous)는 같은 의미로 혼용된다.

---

## 용어 및 핵심 개념

### 1. asyncio
- Python 비동기 라이브러리.
- 트리거 구현의 기반이 되는 핵심 요소

### 2. Trigger
- 작고 비동기적인 Python 코드 조각
- 단일 트리거러 프로세스 안에서 다수의 트리거가 효율적으로 공존할 수 있도록 설계됨
- 조건 충족 시 이벤트(TriggerEvent 등)를 발생시킴

### 3. Triggerer
- 스케줄러/워커와 유사한 Airflow 구성 요소(서비스/프로세스)
- asyncio 이벤트 루프를 실행하며 트리거를 돌림
- 지연 가능 연산자를 사용하려면 트리거러 실행이 필요함

### 4. Deferred
- 작업이 실행을 멈추고 워커 슬롯을 해제한 뒤, 트리거러가 수행할 트리거를 제출한 상태를 의미하는 작업 상태

### 5. 워커 슬롯 / Pool 슬롯 점유
- 지연 단계에서 작업은 워커 슬롯을 점유하지 않음
- 기본적으로 Pool 슬롯도 점유하지 않음

---

## 전통적인 방식 vs 지연 가능 방식

### 1. 전통적인 연산자/센서 방식
- 작업이 외부 시스템에 요청을 보낸 뒤 완료될 때까지 반복 폴링(poke/poll)을 수행함
- 폴링 자체는 큰 연산이 아니어도, **대기 내내 워커 슬롯을 계속 점유함**
- 워커 슬롯이 가득 차면 다른 작업이 큐에 쌓이고 시작이 지연됨

### 2. 지연 가능 연산자 방식
- 작업이 “기다림” 상태가 되면 스스로 defer하여 워커 슬롯을 해제함
- 대기/폴링은 트리거러의 트리거가 담당함(워커에서 트리거러로 오프로딩)
- 외부 조건 충족 이벤트가 발생하면 작업이 다시 실행되어 마무리 단계로 진행함
- 일부 연산자는 처음부터 워커를 거치지 않고 바로 지연 상태로 시작할 수도 있음

---

## 장점

### 1. 리소스 소비 감소
- 단일 트리거러 프로세스에서 수백~수천 개의 지연 작업을 동시에 처리할 수 있음(리소스와 트리거 작업량에 따라 달라질 수 있다.)
- 동시성이 높은 상황에서 필요한 워커 수를 줄여 인프라 규모를 낮출 수 있음

### 2. 재시작에 대한 복원력
- 트리거는 stateless 방식으로 설계됨
- 배포/인프라 문제로 트리거러 재시작이 필요해도, 지연된 작업이 자동으로 실패로 바뀌지 않음
- 트리거러가 다시 실행되면 지연 작업도 재개됨

### 3. 센서 reschedule 대비 유연성
- reschedule은 일정 주기로 재실행되며 시간 기반 조건에 유리하지만, 복잡한 외부 이벤트 대기에는 비효율적일 수 있음
- deferrable은 대기 구간에 워커를 점유하지 않아 외부 이벤트/리소스 대기에 효율적임

---

## 언제 사용해야 하는가?

- 외부 시스템의 완료/조건 충족을 기다리면서 워커 슬롯을 점유하는 작업이 있다면 지연 가능 연산자 사용이 권장됨
- 트리거러를 사용할 수 없는 긴 센서 작업이라면, 불필요한 리소스 낭비를 줄이기 위해 센서 mode='reschedule' 사용이 권장됨

---

## 지연 가능 연산자 사용 방법(운영/설정)

### 1. 트리거러 실행
- 최소 1개 이상의 triggerer 프로세스가 실행 중이어야 함
- 기본 트리거 처리 용량(capacity)은 1000개

### 2. 연산자의 deferrable 매개변수 사용
- 여러 연산자/센서가 `deferrable` 파라미터를 지원함
  - 예: TriggerDagRunOperator, WasbBlobSensor 등

### 3. 기본값을 deferrable로 강제
- 환경 변수로 기본 동작을 지연 가능 모드로 설정할 수 있음.
  - `AIRFLOW__OPERATORS__DEFAULT_DEFERRABLE=True`

### 4. 개별 작업에서 deferrable 끄기 예시
```python
trigger_dag_run = TriggerDagRunOperator(
    task_id="task_in_downstream_dag",
    trigger_dag_id="downstream_dag",
    wait_for_completion=True,
    poke_interval=20,
    deferrable=False,
)
```

### 5. 과거의 -Async 연산자

- 과거에는 `DateTimeSensorAsync` 같은 별도 클래스 형태(-Async)가 있었으나, 현재는 기존 연산자 패키지에 통합되는 방향으로 정리되고 있음

---

## 지연 가능 연산자 작성(커스텀 구현)

### 지연 가능 연산자를 직접 만들 때 고려할 점

- 연산자는 트리거를 사용해 스스로 defer해야 함
- defer 시 워커에서 작업이 중지/제거되며, 지역 변수 등 런타임 상태는 유지되지 않음
- 상태가 필요하면 재개 메서드(method_name)로 인자를 전달(kwargs)하거나, 재개 시 재구성되도록 설계해야 함
- 필요한 만큼 여러 번 defer할 수 있음(제어 책임은 구현자에게 있음)
- 일반 모드/지연 모드를 모두 지원하는 연산자는 설정의 default_deferrable 값을 읽어 동작을 분기하는 것이 권장됨

### 1. 트리거 클래스 예시(MyTrigger)

```python
class MyTrigger(BaseTrigger):
    def __init__(self, poll_interval: int = 60, ...):
        super().__init__()
        self.poll_interval = poll_interval
        # ...

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return ("include.deferrable_operator_template.MyTrigger", {"poll_interval": self.poll_interval, ...})

    async def run(self) -> AsyncIterator[TriggerEvent]:
        while True:
            result = await self.my_trigger_function()
            if result == 1:
                yield TriggerEvent(self.serialize())
                return
            await asyncio.sleep(self.poll_interval)
```

### 2. 연산자 클래스 예시(MyOperator)

```python
class MyOperator(BaseOperator):
    def execute(self, context: Context):
        if self._defer:
            self.defer(
                trigger=MyTrigger(poll_interval=self.poke_interval, ...),
                method_name="execute_complete",
            )
        else:
            ...

    def execute_complete(self, context: Context, event: tuple[str, dict[str, Any]], ...):
        self.log.info("Trigger is complete.")
```

---

## Writing Triggers

트리거는 BaseTrigger를 상속하고 다음 3개 메서드를 구현해야 함

### 1. **init**

- 연산자로부터 필요한 인자를 전달받아 저장

### 2. run

- 반드시 비동기 메서드(async def)여야 함
- 비동기 제너레이터로서 하나 이상의 이벤트를 yield 해야 함(TriggerEvent 등)
- 블로킹 작업을 수행하면 안 되며, 필요한 경우 await를 올바르게 사용해야 함
- 트리거가 여러 번 실행될 수 있으므로, DB 행 추가 같은 부작용이 없도록 설계해야 함

### 3. serialize

- 트리거를 재구성하는 데 필요한 정보를 반환:
  - 클래스 경로
  - __init__에 전달할 키워드 인자(dict)

### 4. 추가 주의사항

- 트리거 코드 변경을 반영하려면 트리거러 프로세스를 재시작해야 함(클래스 캐시)
- Airflow 2.9.0부터 트리거에 전달되는 kwargs는 DB에 암호화되어 저장됨

---

## 작업 시작부터 바로 지연(Triggering Deferral from Task Start)

- Airflow 2.10.0에 추가된 기능
- 워커를 거치지 않고 처음부터 트리거러에서 대기하도록 설정 가능
- 연산자 클래스 레벨에 `start_from_trigger = True`를 설정하고, `StartTriggerArgs`를 `start_trigger_args` 속성에 지정함
- Dynamic Task Mapping 에서 워커 실행을 생략하고 바로 대기하도록 할 때 유용함

---

## 트리거에서 작업 바로 종료(Exiting deferred task from Triggers)

- Airflow 2.10.0에 추가된 기능
- 트리거러가 조건 충족 후 워커로 돌아가지 않고, 트리거러에서 작업 인스턴스를 바로 성공/실패 종료 가능
- 연산자 인스턴스에 `end_from_trigger = True` 설정
- 트리거 run에서 `TaskSuccessEvent()` 또는 `TaskFailureEvent()`를 yield하여 종료

---

## High Availability

- 트리거는 고가용성을 고려해 설계됨
- 여러 호스트에서 여러 트리거러 복사본을 실행할 수 있음
- 기본 capacity는 트리거러당 1000개이며, 용량은 인자로 조정 가능
- 트리거러 노드 장애/네트워크 문제 시 Airflow가 다른 호스트로 트리거를 재예약함
- 드물게 중복 실행이 발생해도 이벤트는 자동 중복 제거(de-duplicate)됨

---

## mode='reschedule' 과 deferrable=True 차이

### 1. mode='reschedule'

- 내장 스케줄링으로 조건 충족까지 자신을 재예약
- 주기적으로 다시 실행되므로 리소스 사용량이 상대적으로 높을 수 있음
- 시간에 따라 변할 것으로 예상되는 조건(예: 파일 생성 대기)에 적합

### 2. deferrable=True

- 유휴/대기 구간에서 실행을 멈추고 워커 슬롯을 해제
- 트리거가 조건 확인을 수행
- 리소스 사용량이 낮고, 외부 이벤트/리소스 대기에 효율적임
- 필요한 경우 커스텀 트리거/로직 구현이 필요할 수 있음
