### **XCom (Cross Communication)**  
- 태스크 간에 데이터를 교환하기 위해 사용 
- **Push와 Pull** 방식으로 데이터를 주고받을 수 있음 
- 데이터 전달 시 **JSON 직렬화**가 가능

### **Executor**  
- 태스크를 실제로 실행하는 역할  
- **종류:**  
  - **SequentialExecutor:** 단일 태스크 실행 (테스트용)  
  - **LocalExecutor:** 멀티스레드 기반으로 병렬 실행  
  - **CeleryExecutor:** 분산 환경에서 태스크 병렬 실행 (대규모 환경)  
  - **KubernetesExecutor:** 쿠버네티스 클러스터에서 태스크를 컨테이너로 실행  
  
### **Variables**  
**키-값 쌍**으로 구성된 전역 설정 값을 저장하고 검색하기 위한 기능
- **중앙 집중식 관리**  
  - Airflow UI, CLI, 환경 변수 또는 코드 내에서 Variables를 생성, 수정 및 삭제 가능
- **JSON 지원**  
  - 값을 JSON 형식으로 저장하여 복잡한 데이터 구조를 관리  
- **보안**  
  - 민감한 정보는 환경 변수나 시크릿 백엔드를 통해 관리하는 것을 권장 (평문으로 저장됨)  
  
#### **성능 고려: DAG 파일의 최상위 코드에서 Variable.get() 호출 문제**  

##### **문제점**  
- DAG 파일의 최상위 코드(전역 범위)에서 `Variable.get()`을 호출하면 **매번 DAG 파일이 파싱될 때마다 데이터베이스에 접근**  
- Airflow는 DAG 파일을 주기적으로 스캔하고 파싱하여 DAG 객체를 메모리에 올리기 때문에, 이 과정에서 **매번 DB 접근이 일어나면 성능 저하**를 유발  

#### **잘못된 사용 예시**  
```python
from airflow.models import Variable
# DAG 파싱 시 매번 DB 접근 발생
my_var = Variable.get("my_key")
```

#### **해결 방법:**  

1. **Operator 내부에서 호출:**  
   - 태스크 실행 시점에 변수 값을 가져오므로 **DAG 파싱 시에는 DB 접근을 회피  
   - **태스크 실행 시점**에 변수를 로드하여 더 효율적
2. **Jinja 템플릿 사용:**   
- 템플릿 사용으로 변수를 직접 코드에 포함하지 않아도 되어 **가독성이 높음** 
- 성능 저하 없이 **실행 시점에 값을 가져옴**  

#### **예시 코드:**  
```python
with DAG("template_dag", start_date=datetime(2023, 1, 1)) as dag:
    task = BashOperator(
        task_id="print_var",
        bash_command="echo {{ var.value.my_key }}" # jinja template
    )
