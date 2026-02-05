# Dockerfile 명령어 모음

### FROM
- 사용할 베이스 이미지를 지정

```dockerfile
FROM ubuntu:20.04
```

### RUN
- 빌드할 때 실행할 명령어

```dockerfile
RUN apt-get update && apt-get install -y python3
```

### COPY
- 호스트의 파일을 이미지 안으로 복사
- Dockerfile 과 동일한 디렉토리에 있어야한다.

```dockerfile
COPY ./src /app
```

### ADD
- 파일 복사 + URL 다운로드 + 압축 해제를 지원

```dockerfile
ADD https://example.com/app.tar.gz /opt/
```

### ENV
- 환경 변수를 설정

```dockerfile
ENV APP_ENV=production
```

### EXPOSE
- 컨테이너가 사용할 포트를 명시
- 실제로 저 포트를 사용하는게 아니니 주의

```dockerfile
EXPOSE 8080
```

### WORKDIR
- 작업 디렉터리를 지정하고 이후 명령어들은 이 디렉터리 기준으로 실행

```dockerfile
WORKDIR /app
```

### VOLUME
- 데이터 공유용 볼륨을 설정

```dockerfile
VOLUME /data
```

### ARG
- 빌드 시점에만 사용할 변수 설정

```dockerfile
ARG VERSION=1.0
```

### LABEL
- 이미지에 메타데이터를 추가

```dockerfile
LABEL maintainer="admin@example.com"
```

### USER
- 명령어를 특정 사용자 권한으로 실행하도록 설정

```dockerfile
USER appuser
```

# CMD와 ENTRYPOINT
CMD와 ENTRYPOINT는 Dockerfile에서 컨테이너 실행 시 기본 명령어를 지정하는데 사용된다.

## CMD
- 컨테이너가 실행될 때 기본으로 실행할 명령어나 인수를 지정한다.

```commandline
쉘 형식: CMD echo "Hello, World!"

exec 형식: CMD ["echo", "Hello, World!"]
```
- docker run 명령어에서 다른 명령어나 인수를 제공하면 CMD에서 지정한 내용이 대체된다. (덮어씀)
- Dockerfile에 여러 개 작성 시, 마지막 CMD만 실행된다.

## ENTRYPOINT
- 컨테이너가 실행될 때 항상 실행될 명령어를 지정한다.

```commandline
exec 형식: ENTRYPOINT ["nginx", "-g", "daemon off;"]
```
- docker run 명령어에서 추가적인 인수를 제공하면 ENTRYPOINT에서 지정한 명령어의 인수로 전달된다.
- Dockerfile에 여러 개 작성 시, 마지막 ENTRYPOINT에서 실행된다.

## CMD + ENTRYPOINT
- 두 지시어를 함께 사용할 경우, ENTRYPOINT에서 기본 실행 파일을 지정하고, CMD에서 전달할 기본 인수를 지정하는 방식으로 사용가능

```commandline
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
```
- nginx -g daemon off;가 실행된다.
- 인자를 추가할 경우 CMD 구문은 무시된다.

