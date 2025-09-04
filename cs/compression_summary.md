### 손실 압축 vs 무손실 압축
- **무손실(Lossless)**: 원본 데이터 완벽 복원 가능 
  - 텍스트, 로그, 실행 파일 등 정보 손실이 허용되지 않는 데이터에 사용 
  - 예: Huffman Coding, LZ77/78, Deflate(gzip), Bzip2, Zstandard, Snappy 
- **손실(Lossy)**: 일부 정보 손실 허용, 대신 압축률 높음 
  - 이미지, 오디오, 영상 등에서 주로 사용 
  - 예: JPEG(DCT 기반), MP3(주파수 마스킹), MPEG

### 대표 무손실 압축 알고리즘
- **Huffman Coding** 
  - 자주 등장하는 문자는 짧은 비트 코드, 드물게 등장하는 문자는 긴 코드 할당 
  - 가변 길이 부호, prefix-free(접두어 중복 없음) 특성 → 효율적 
- **Lempel-Ziv (LZ77/78)** 
  - 중복되는 문자열을 dictionary/offset으로 치환 
  - gzip, zip, PNG 내부에서 사용됨 
- **Zstandard (Zstd)** 
  - Facebook이 개발한 최신 알고리즘 
  - LZ77 + entropy coding 조합 
  - 압축률과 속도 모두 뛰어나 Spark, Kafka, ClickHouse 등에서 널리 사용

### 실제 데이터 엔지니어링 적용 예시
- 로그 데이터: 무손실 압축 필수 (예: gzip, zstd, snappy) 
- 스트리밍/실시간 처리: 속도가 중요 → **Snappy, LZ4** 
- 장기 보관: 압축률이 중요 → **Zstandard, gzip** 
- Spark/Hadoop: 코덱 지정 가능 (`spark.sql.parquet.compression.codec = zstd` 등)
