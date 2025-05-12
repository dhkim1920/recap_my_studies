# Airflow 기본 개념 정리

## DAG Run & Task Instance

### DAG Run
- DAG Run은 특정 시점에 DAG 전체가 실행된 인스턴스를 의미한다.
- 각 DAG Run은 고유한 `logical_date`를 가지며, 이는 DAG가 처리해야 할 데이터의 논리적 시점을 나타낸다. 
  - 자세한 건 [airflow_execution_date_problem.md](airflow_execution_date_problem.md) 참고
- DAG Run은 스케줄러에 의해 자동으로 실행되거나 수동 실행할 수 있다. (UI 또는 cli)

### Task Instance
- Task Instance는 DAG Run 내에서 특정 태스크의 실행 인스턴스를 의미한다.
- 각 Task Instance는 상태를 가지며, 가능한 상태는 다음과 같다.
  - `none`: 아직 실행 대기 중 (start_date를 미래로 했는데 수동 실행하면 볼수 있다.)
  - `scheduled`: 실행이 예정됨
  - `queued`: 실행 대기열에 있음
  - `running`: 실행 중
  - `success`: 성공적으로 완료됨
  - `failed`: 실행 중 오류 발생
  - 등등
  
## Operators & Sensors

### Operators
- Operator는 태스크의 실행 단위를 정의하는 템플릿이다.
- Airflow는 다양한 내장 Operator를 제공한다.
  - `PythonOperator`: Python 함수를 실행
  - `BashOperator`: Bash 명령어를 실행
  - `EmailOperator`: 이메일을 전송
  - 이외에도 spark submit을 제출할 수 있는 SparkSubmitOperator 등등 여러 Oerator를 제공한다.
    - 자세한 내용은 공홈 참고 https://airflow.apache.org/docs/apache-airflow-providers/operators-and-hooks-ref/index.html

### Sensors
- Sensor는 특정 조건이 충족될 때까지 대기하는 특수한 Operator이다.
- `FileSensor` (예: 파일이 존재할 때까지 대기한다.)
- Sensor는 두 가지 모드를 지원한다.
  - `poke`: 주기적으로 상태 확인 (워커를 점유)
  - `reschedule`: 대기 중 워커 리소스를 해제하여 효율적 운영 가능 


## **XCom (Cross Communication)**  
- 태스크 간에 데이터를 교환하기 위해 사용 
- **Push와 Pull** 방식으로 데이터를 주고받을 수 있음 
- 데이터 전달 시 **JSON 직렬화** 가능
- 작은 데이터 교환을 위한 것이므로, 큰 데이터를 공유에는 부적합 (DB에 저장되기 때문에 성능과 관련도 있음)
- Airflow 2.0부터는 보안상의 이유로 Pickle 직렬화가 기본적으로 비활성화되어 있음
  - 원격 코드 실행(RCE) 취약점을 방지
- 태스크 간의 의존성이 생길 수 있으므로, DAG 설계 시 주의

## **Executor**  
- 태스크를 실제로 실행하는 역할  
- **종류:**  
  - **SequentialExecutor:** 단일 태스크 실행 (테스트용)  
  - **LocalExecutor:** 멀티스레드 기반으로 병렬 실행  
  - **CeleryExecutor:** 분산 환경에서 태스크 병렬 실행 (대규모 환경)  
  - **KubernetesExecutor:** 쿠버네티스 클러스터에서 태스크를 컨테이너로 실행 
    - k8s 장점을 그대로 갖고 있음 (관리가 어렵다는 거)
  
## **Variables**  
**key-value 쌍**으로 구성된 전역 설정 값을 저장하고 검색하기 위한 기능
- **중앙 집중식 관리**  
  - Airflow UI, CLI, 환경 변수 또는 코드 내에서 Variables를 생성, 수정 및 삭제 가능
- **JSON 지원**  
  - 값을 JSON 형식으로 저장하여 복잡한 데이터 구조를 관리  
  - 직렬화/역직렬화
    <br>`Variable.set("key", json.dumps(obj))`
    <br>`Variable.get("key", deserialize_json=True)`
- **보안**  
  - 민감한 정보는 환경 변수나 시크릿 백엔드를 통해 관리하는 것을 권장 (평문으로 저장됨)  
  
### **DAG 파일의 최상위 코드에서 Variable.get() 호출했을 때 발생하는 문제**  

#### **문제점**  
- DAG 파일의 최상위 코드(전역 범위)에서 `Variable.get()`을 호출하면 **매번 DAG 파일이 파싱될 때마다 DB에 접근**  
- Airflow는 DAG 파일을 주기적으로 스캔하고 파싱하여 DAG 객체를 메모리에 올리기 때문에, 이 과정에서 **매번 DB 접근이 일어나면 성능 저하**를 유발  

### **잘못된 사용 예시**  
```python
from airflow.models import Variable
# DAG 파싱 시 매번 DB 접근 발생
my_var = Variable.get("my_key")
```

### **해결 방법:**  

1. **Operator 내부에서 호출:**  
   - 태스크 실행 시점에 변수 값을 가져오므로 **DAG 파싱 시에는 DB 접근을 회피**
   - **태스크 실행 시점**에 변수를 로드하여 더 효율적
2. **Jinja 템플릿 사용:**   
   - 템플릿 사용으로 변수를 직접 코드에 포함하지 않아도 되어 **가독성이 높음** 
   - 성능 저하 없이 **실행 시점에 값을 가져옴**  

### **예시 코드:**  
```python
with DAG("template_dag", start_date=datetime(2023, 1, 1)) as dag:
    task = BashOperator(
        task_id="print_var",
        bash_command="echo {{ var.value.my_key }}" # jinja template
    )
```

### 영향이 큰가?
- 보통 variables에 설정하는 값이 작은 값들로 DB I/O는 적을 실제 영향은 미비할 것이다. 
그러나 dag가 많아지고 스케쥴이 자주 돌아간다면? 그러니 주의해서 나쁠건 없다. 