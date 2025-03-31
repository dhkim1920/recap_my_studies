

## 2022년 부터 세션 ID가 음수가 되는 이슈
참고) 공식 지라 https://issues.apache.org/jira/browse/ZOOKEEPER-1622

※ 이 이슈는 zookeeper 3.4.5 이하에서 발생하며 3.4.6에서 해결되었습니다.

### 문제 상황
- myid 파일에 너무 큰 값을 사용했을 때, 세션 ID가 음수가 되어 제대로 로직이 동작하지 않음
  - 서버 측에서 해당 세션 ID를 정상적으로 인식하지 못하고 계속, 연결을 끊고 재시도하는 루프에 빠지게됨
  
### 문제 코드 분석
```
public static long initializeNextSession(long id) {
    long nextSid = 0;
    nextSid = (System.currentTimeMillis() << 24) >> 8; // 문제가 되는 부분
    nextSid = nextSid | (id << 56);
    return nextSid;
}
```
- System.currentTimeMillis()는 현재 시간을 밀리초 단위로 반환하여 long 타입(64비트)으로 표현한다.
- << 24: 현재 시간 값을 왼쪽으로 24비트 이동하여 유일성을 확보한다.
- \>\> 8: 다시 8비트 오른쪽으로 이동하는데 이때 부호가 변결될 수 있다.
- 이는 >> 연산이 산술 시프트기 때문에 발생 <br> 
→ 결과적으로 부호 비트(40번째 비트)가 1이면 음수가 되고 따라서 nextSid가 음수가된다.

### 해결 방법
- 산술 시프트 >> 대신 논리 시프트 >>> 를 사용하여 부호 확장을 방지한다.
- \>\>\>의 경우 부호 비트 확장 없이 0으로 채우게 되므로 문제를 피할수 있다. 


## 자바의 산술 시프트와 논리 시프트
### 1. 산술 시프트 (>>)
- 부호 비트를 유지하면서 오른쪽으로 밀어낸다.
- 음수인 경우, 왼쪽 빈자리를 1로 채운다.
```
public class ShiftExample {
    public static void main(String[] args) {
        int negativeNumber = -8; // 11111111 11111111 11111111 11111000

        int result = negativeNumber >> 1;
        System.out.println("산술 시프트: " + result);
    }
}
```
결과
```commandline
-8의 이진수:       11111111 11111111 11111111 11111000
>> 1 (산술 시프트): 11111111 11111111 11111111 11111100
```
- 왼쪽 최상위 비트가 1로 채워짐 → 음수 유지

### 2. 논리 시프트 (>>>)
- 항상 왼쪽 빈자리를 0으로 채운다.
- 음수여도 부호 비트가 유지되지 않는다.

```
public class ShiftExample {
    public static void main(String[] args) {
        int negativeNumber = -8; // 11111111 11111111 11111111 11111000

        int result = negativeNumber >>> 1;
        System.out.println("논리 시프트: " + result);
    }
}
```
결과 
```
-8의 이진수:        11111111 11111111 11111111 11111000
>>> 1 (논리 시프트): 01111111 11111111 11111111 11111100
```
- 왼쪽 최상위 비트가 0으로 채워짐 → 양수로 변환됨

### 정리
- 산술 시프트 (>>): 부호 비트를 유지하며 오른쪽으로 이동 → 음수는 음수로 유지
- 논리 시프트 (>>>): 부호 비트 무시, 무조건 0으로 채움 → 음수가 양수로 변할 수 있음