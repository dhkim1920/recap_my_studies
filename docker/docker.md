
### CMD와 ENTRYPOINT
CMD와 ENTRYPOINT는 Dockerfile에서 컨테이너 실행 시 기본 명령어를 지정하는데 사용된다.

#### CMD
- 컨테이너가 실행될 때 기본으로 실행할 명령어나 인수를 지정한다. 
```commandline
쉘 형식: CMD echo "Hello, World!"

exec 형식: CMD ["echo", "Hello, World!"]
```
- docker run 명령어에서 다른 명령어나 인수를 제공하면 CMD에서 지정한 내용이 대체된다. (덮어씀)
- Dockerfile에 여러 개 작성 시, 마지막 CMD만 실행된다.

#### ENTRYPOINT
- 컨테이너가 실행될 때 항상 실행될 명령어를 지정한다.
```commandline
exec 형식: ENTRYPOINT ["nginx", "-g", "daemon off;"]
```
- docker run 명령어에서 추가적인 인수를 제공하면 ENTRYPOINT에서 지정한 명령어의 인수로 전달된다.
- Dockerfile에 여러 개 작성 시, 마지막 ENTRYPOINT에서 실행된다.

#### CMD + ENTRYPOINT
- 두 지시어를 함께 사용할 경우, ENTRYPOINT에서 기본 실행 파일을 지정하고, CMD에서 전달할 기본 인수를 지정하는 방식으로 사용가능
```commandline
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
```
- nginx -g daemon off;가 실행된다.
- 인자를 추가할 경우 CMD 구문은 무시된다.