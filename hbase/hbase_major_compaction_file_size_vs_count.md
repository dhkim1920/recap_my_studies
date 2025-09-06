
# HBase Major Compaction: StoreFile 규모와 개수에 따른 부하?

## 큰 StoreFile이 소량이라면?

- **I/O 양**
  - 개별 파일이 커서 한 번에 읽고 쓰는 블록 수가 많음 → I/O 부하는 크지만 횟수는 적음

- **병합 대상 수**
  - 적음 (예: 2~3개)

- **메모리/CPU 부담**
  - 블록 단위 처리량이 커서 메모리 압박은 상대적으로 낮음
    - 파일이 큰데 왜 메모리 압박이 상대적으로 낮을까?
      - 파일이 크더라도 처리 방식이 블록 단위이며, 동시에 처리하는 양이 정해져 있다.

- **HDFS 쓰기 부하**
  - 병합 결과 파일이 크기 때문에, 쓰기 한 번당 부하가 큼

- **요약**
  - 과정은 단순하며, 네트워크와 디스크 부하는 크지만 횟수는 적음

---

## 작은 StoreFile 다수라면?

- **I/O 양**
  - 파일 개수가 많아 open/close 반복 → 오버헤드 큼
    → 연속적인 I/O 작업이 많아짐

- **병합 대상 수**
  - 많음 (예: 20~30개)

- **메모리/CPU 부담**
  - BloomFilter 재생성, block index 병합 등으로 CPU 사용량과 GC 부담 증가

- **HDFS 쓰기 부하**
  - 각 파일은 작지만 병합 결과는 커질 수 있음

- **요약**
  - FileSystem 핸들 수 증가
  - 메타데이터 처리량 많음
  - 전체 Compaction 시간 길어짐

---

## 결론 요약

| 항목                     | 큰 StoreFile 몇 개 | 작은 StoreFile 다수 |
|------------------------|-------------------|---------------------|
| 병합 대상 파일 수           | 적음                | 많음                |
| I/O 횟수                | 적음                | 많음                |
| CPU/메모리 부하          | 낮음                | 높음                |
| HDFS 쓰기/네트워크 부하     | 큼 (단순)           | 분산되고 복잡함       |
| 파일 핸들/메타데이터 오버헤드 | 낮음                | 높음                |

> 작은 StoreFile 다수일 때 시스템 리소스 소모가 더 크다.

### 참고)
Cloudera 관련 글

https://www.cloudera.com/blog/technical/small-files-big-foils-addressing-the-associated-metadata-and-application-challenges.html?utm_source=chatgpt.com
