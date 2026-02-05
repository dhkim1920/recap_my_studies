# Spark 저장 완료 확인 (_SUCCESS 파일)

## 언제 생성될까?
- Hadoop FileOutputCommitter가 잡 커밋 시 `_SUCCESS` 파일을 기록한다.
- 기본적으로 **0바이트 파일**로 생성된다.
- S3A 커밋터(매직/매니페스트 등)를 사용할 경우 `_SUCCESS`는 **JSON 요약 파일**이 될 수 있으며, 어떤 커밋터가 사용되었는지도 포함된다.

## 위치
- 출력 루트 디렉터리에만 1개 생성된다.
- 파티션 저장이어도 루트에만 생긴다.

## 생성되지 않는 경우
- `mapreduce.fileoutputcommitter.marksuccessfuljobs=false`로 설정된 경우
- Delta Lake: `_delta_log` 디렉터리에 커밋 JSON/체크포인트 파일로 완료를 관리한다.
- Apache Iceberg: 스냅샷·매니페스트/매니페스트 리스트 파일로 상태를 추적한다.

## 설정 방법
- spark-submit 시
    ``` bash
    --conf spark.hadoop.mapreduce.fileoutputcommitter.marksuccessfuljobs=true
    ```

## 의미와 한계
- `_SUCCESS`는 "잡 커밋 완료"를 의미하는 **마커 파일**이다.
- 레코드 단위 무결성까지 보장하지 않으므로, 필요 시 count, 해시 비교 등 별도 검증을 수행해야 한다.
