
# Docker-compose의 좀비 프로세스

### init: true 설정
컨테이너 내에서 신호 전달과 좀비 프로세스 처리를 담당하는 간단한 초기화 시스템을 실행하도록 지정하는 설정이다.
<br>이는 컨테이너 내에서 생성된 자식 프로세스들을 종료하고, 신호가 적절하게 처리되도록 보장한다.

#### 사용법
```commandline
version: '3.7'
services:
  web:
    image: myapp:latest
    init: true
```

#### init: true를 설정했을 때와 설정하지 않았을 때의 차이는?

- 예시로 docker compose 파일을 작성해 보자.
```commandline
version: '3.7'
services:
  init_false:
    image: test_init
    command: sh -c "sleep 1000 & while true; do sleep 1; done"
  init_true:
    image: test_init
    init: true
    command: sh -c "sleep 1000 & while true; do sleep 1; done"
```

- init: true 설정을 하지 않은 경우
```commandline
PID   USER     TIME  COMMAND
    1 root      0:00 sh -c sleep 1000 & while true; do sleep 1; done
    7 root      0:00 sh -c sleep 1000 & while true; do sleep 1; done
   14 root      0:00 sleep 1000
```
- PID 1이 sh 자체가 PID 1로 동작된다. (직접 실행)

- init: true 설정을 한 경우
```
PID   USER     TIME  COMMAND
    1 root      0:00 /dev/init -- sh -c sleep 1000 & while true; do sleep 1; done
    7 root      0:00 sh -c sleep 1000 & while true; do sleep 1; done
   14 root      0:00 sleep 1000
```
- PID 1이 /dev/init로 할당된 것을 볼수 있다. (Docker Init Process의 사용)
- 따라서 모든 자식 프로세스가 init을 통해 정리된다.

#### 결론
- init: true를 사용하면 Docker의 기본 초기화 프로세스가 PID 1로 작동하여 자식 프로세스와 신호를 제대로 관리한다.
- init: true를 설정하지 않으면 컨테이너 내부 프로세스가 직접 PID 1로 실행되어 좀비 프로세스 될 수 있다.
- 좀비 프로세스가 될경우 docker container가 제대로 종료되지 않을 수 있다.
