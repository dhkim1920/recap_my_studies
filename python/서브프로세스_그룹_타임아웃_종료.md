# subprocess.Popen에서 start_new_session=True와 timeout 처리

## 왜 쓸까?
- 프로세스 그룹 분리: 기존 터미널 세션 및 PGID로부터 완전히 격리시킬 수 있다.
- 전체 종료 가능: `os.killpg(os.getpgid(pid), signal.SIGKILL)`로 그룹 전체 종료 가능하다.
- 안전한 타임아웃 처리: fork된 하위 프로세스까지 포함해 종료 가능
- Thread-safe: `preexec_fn=os.setsid`보다 예외 처리와 안정성에서 우수 (내부적으로 로직은 동일함)
- subprocess Popen의 경우 network 이슈 등으로 접속이 안되면 행이 걸리는 수가 있다. 이럴 경우 timeout 처리 및 sub process를 종료해줘야 하는데 이 때 쓰자

---

## 코드 예시

```python
import subprocess, os, signal

p = subprocess.Popen(['sleep', '100'], start_new_session=True)

try:
    p.wait(timeout=10)
except subprocess.TimeoutExpired:
    os.killpg(os.getpgid(p.pid), signal.SIGKILL)
```

- `p.pid`는 새로운 프로세스 그룹의 리더
- `getpgid(p.pid)`는 해당 PGID 반환
- `killpg()`는 그룹 전체에 SIGKILL 시그널 전송

---

## 주의사항

- **Unix/Linux 환경에서만 사용 가능하다.**
- **Windows**에서는 `CREATE_NEW_PROCESS_GROUP`과 `taskkill` 사용 필요 (안써봐서 모르것다.)
- `p.pid`가 종료된 후 참조하면 예외 발생 가능 → 항상 `try-except`로 감쌀 것
