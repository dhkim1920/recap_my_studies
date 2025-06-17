# Iceberg DataFile 수동 등록 시 주의사항

## 1. DataFiles.builder(PartitionSpec) 사용 시 필수 조건

- `PartitionSpec`는 테이블과 정확히 일치해야 한다.
- 필수 필드:
  - `withPath(String)`: 절대 경로, 테이블 warehouse 하위여야 한다.
  - `withFileSizeInBytes(long)`: 파일 크기
  - `withRecordCount(long)`: 레코드 수 (0이면 조회 누락 가능)
  - `withFormat(FileFormat)`: 예: `FileFormat.PARQUET`
  - `withPartition(...)`: 파티션 테이블이면 반드시 지정

## 2. Iceberg 메타데이터 반영

```java
table.newAppend()
     .appendFile(dataFile)
     .commit();  
```
- `commit()` 까지 해야 최종 반영된다.
- 메타 파일이 충돌이 발생할 수 있으므로 한번만 해야한다.

## 3. 예제

```java
DataFile dataFile = DataFiles.builder(table.spec())
    .withPath("hdfs://warehouse/my_table/data/part-0000.parquet")
    .withFileSizeInBytes(fs.getFileStatus(new Path(...)).getLen())
    .withRecordCount(100)
    .withFormat(FileFormat.PARQUET)
    .withPartition(...) 
    .build();

table.newAppend()
    .appendFile(dataFile)
    .commit();
```