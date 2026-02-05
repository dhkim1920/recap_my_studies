# HBase WAL는 어떻게 삭제 될까?

## WAL 삭제 시점과 조건

- WAL은 **MemStore가 flush되어 HFile로 반영된 후**, 해당 WAL 파일의 **모든 로그가 참조되지 않으면 삭제**되게 된다.
- 다음 조건 중 하나라도 충족되면 flush가 발생하고, 그에 따라 WAL 삭제된다. (flush에 의존함)
  - `hbase.hregion.memstore.flush.size` 초과
  - `hbase.regionserver.global.memstore.upperLimit` 초과, 전체 memstore 상한
  - `hbase.regionserver.max.logs` 초과 시 자동 flush 발생, wal log가 너무 많아지니까 도달하면 강제로 flush
  
## WAL 삭제 절차 요약

1. 특정 Region의 MemStore가 flush됨  
2. 해당 WAL 파일의 로그가 모두 반영되었고  
3. WAL이 다른 Region에서도 참조되지 않으면 HBase가 해당 WAL 파일을 삭제
