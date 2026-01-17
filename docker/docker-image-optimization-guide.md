# 도커 이미지 최적화

## 1. 왜 이미지 용량이 커지는가? (이론)

### A. 레이어 시스템 (Copy-on-Write)

Docker 이미지는 여러 개의 읽기 전용(Read-only) 레이어가 쌓인 구조입니다. 특정 파일의 권한을 변경하거나 삭제하더라도, **하위 레이어에 이미 기록된 데이터는 사라지지 않습니다.**

* **문제:** 1GB 파일이 있는 레이어 위에 `chmod`를 실행하면, 수정된 메타데이터를 저장하기 위해 1GB 파일이 새로운 레이어에 통째로 다시 복사됩니다. (합계 2GB 사용)

### B. 빌드 컨텍스트 (Build Context)

`docker build .` 명령을 실행하면 현재 디렉토리의 모든 파일이 Docker 데몬으로 전송됩니다. 빌드에 필요 없는 대용량 파일(예: 백업, 이전 빌드 결과물)이 포함되면 이미지 크기가 비정상적으로 커집니다.

---

## 2. 실전 예제: 데이터 분석 환경 구축

기존의 Spark 예제 대신, **"Pandas 데이터 분석 환경"**을 구축하는 시나리오로 소스를 재구성했습니다.

### [사전 준비] `.dockerignore` 설정

빌드 시 제외할 파일을 명시하여 뻥튀기를 원천 차단합니다.

```text
# .dockerignore
*.csv
*.tar
.venv
__pycache__/

```

### [Step 1] 최적화된 Dockerfile 예시

멀티 스테이지 빌드를 사용하여 '파일 수정 레이어'와 '실행 레이어'를 분리합니다.

```dockerfile
# syntax=docker/dockerfile:1

# --- 1단계: 준비 스테이지 (Preparation Stage) ---
FROM python:3.9-slim AS preparer
WORKDIR /app
USER root

# 분석 스크립트와 소스 복사
COPY scripts/ /app/scripts/

# 권한 변경 (여기서 생기는 레이어 뻥튀기는 최종 이미지에 포함되지 않음)
RUN chmod -R 755 /app/scripts

# --- 2단계: 최종 실행 스테이지 (Final Stage) ---
FROM python:3.9-slim
WORKDIR /data_analysis

# 1단계에서 '완성된 결과물'만 가져옴 (중복 레이어 발생 없음)
COPY --from=preparer /app/scripts /data_analysis/scripts

# 패키지 설치 최적화: 캐시 없이 설치하고 즉시 임시 파일 삭제
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

# 사용자 전환 (보안 권장사항)
USER 1001
CMD ["python", "scripts/main.py"]

```

---

## 3. 핵심 최적화 기법 정리

| 기법 | 이론적 근거 | 효과 |
| --- | --- | --- |
| **Multi-stage Build** | 필요한 아티팩트(결과물)만 선택적으로 복사 | `chmod`, `chown` 등으로 인한 중복 레이어 생성 방지 |
| **`.dockerignore`** | 빌드 컨텍스트에서 불필요한 파일 제외 | 원치 않는 대용량 파일이 이미지에 포함되는 것 방지 |
| **Command Chaining (`&&`)** | 여러 명령을 하나의 레이어로 병합 | 레이어 개수를 줄이고 중간 단계의 찌꺼기 파일 제거 |
| **`--no-cache-dir`** | 패키지 매니저의 임시 다운로드 파일 억제 | `pip` 설치 과정에서 발생하는 수백 MB의 캐시 제거 |

---

## 4. 빌드 결과 확인 및 검증

빌드 후 아래 명령어를 통해 어느 단계에서 용량이 많이 사용되었는지 분석할 수 있습니다.

```bash
# 레이어별 용량 확인
docker history [이미지_이름]

# 전체 이미지 사이즈 확인
docker images | grep [이미지_이름]

```

---

**정리된 내용이 도움이 되셨나요?** 이 가이드를 바탕으로 실제 환경에 적용해 보시고, 특정 에러가 발생하거나 더 구체적인 시나리오가 필요하시면 언제든 말씀해 주세요. 다음 단계로 **이미지 레이어를 더 세밀하게 분석하는 방법**을 도와드릴까요?