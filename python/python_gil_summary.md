
## Python의 GIL(Global Interpreter Lock) 정리

### GIL이란?
GIL은 CPython 인터프리터에서 동시에 하나의 스레드만 Python 바이트코드를 실행할 수 있도록 제한하는 전역 락

멀티스레딩 환경에서 메모리 관리의 일관성과 안정성을 보장하기 위해 도입

### 도입 배경
- Python은 참조 카운팅 기반의 메모리 관리 방식을 사용
- 멀티스레드 환경에서는 참조 수 증가/감소 시 동기화가 필요
- GIL은 객체 참조 수 갱신 등의 작업이 동시에 실행되지 않도록 함으로써 레이스 컨디션을 방지

> 참고)
> 레이스 컨디션(Race Condition) 이란?
여러 작업(쓰레드, 프로세스 등)이 동시에 공유 데이터에 접근하거나 수정할 때 처리 순서나 타이밍에 따라 결과가 달라지는 상황을 말한다.

### 장점
- 참조 카운팅 방식의 메모리 관리를 단순하게 구현 가능
- C로 작성된 확장 모듈과의 호환성 확보
- 단일 스레드 기반 프로그램에서 안정성과 성능 유지

### 단점
- 멀티코어 시스템에서 스레드를 통한 병렬 처리 성능 제한
- CPU 바운드 작업에서 오히려 스레드 사용 시 성능 저하
- Python 스레드는 동시 실행이 아닌 스케줄링에 의해 순차 실행됨

### I/O 바운드 vs CPU 바운드
- I/O 바운드 작업 (ex. 파일 처리, 네트워크 요청):
  - 작업 중 GIL이 해제되므로 스레드 간 병렬성이 어느 정도 확보됨

- CPU 바운드 작업 (ex. 수치 계산, 이미지 처리):
  - GIL로 인해 여러 스레드를 활용하더라도 한 번에 하나만 실행됨
  - 병렬 처리가 사실상 불가능

### Python 3.13의 변화
- GIL 없는 Python 지원 (Free-threaded Python)
- `--disable-gil` 옵션으로 빌드 가능
- 일부 C 확장 모듈과의 호환성 문제 발생 가능
- 실험적 기능으로 성능, 안정성 이슈 있음

### GIL 우회 방법

#### 1. multiprocessing 모듈
- `multiprocessing`은 프로세스를 여러 개 띄워 병렬 처리 수행
- 각 프로세스는 별도의 Python 인터프리터와 GIL을 갖기 때문에 병렬성 확보 가능

```python
from multiprocessing import Process

def task():
    print("작업 수행 중")

if __name__ == "__main__":
    p1 = Process(target=task)
    p2 = Process(target=task)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```
- 단점: 프로세스 간 메모리 공유가 안 되므로 Queue, Pipe, Manager 등을 통해 데이터 전달 필요
- 적합한 작업: CPU 바운드, 대규모 병렬 계산

#### 2. asyncio 모듈
- 비동기 I/O 처리에 특화된 모듈
- GIL의 영향을 적게 받음
- 이벤트 루프 기반으로 여러 작업을 병렬로 처리 가능

```python
import asyncio

async def download():
    print("다운로드 시작")
    await asyncio.sleep(1)
    print("다운로드 완료")

async def main():
    await asyncio.gather(download(), download())

asyncio.run(main())
```
- 단점: CPU 바운드 작업에는 적합하지 않음
- 적합한 작업: 대량의 네트워크 요청, 파일 I/O, 데이터베이스 접근 등

### 결론
- GIL은 Python의 안정성을 확보해주지만, 병렬 처리 성능에는 제한
- 병렬 처리가 필요한 경우, 작업 유형에 따라 `multiprocessing` 혹은 `asyncio`를 선택하여 GIL의 영향을 우회
