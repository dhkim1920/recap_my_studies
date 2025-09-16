
# Kafka 파티션 크기·개수 산정 가이드

## 1) 목표 정의
- **목표 처리량**(records/s, MB/s), **지연 시간**, **보존 기간**(retention), **최대 컨슈머 동시성**을 먼저 수치화 하자
- 파티션은 **병렬성 단위**이며, 컨슈머 그룹의 **동시 처리 스레드 최대치 = 파티션 수**이다.

## 2) 산정 절차
1. **프로듀서/브로커 한 파티션 처리 한계 추정**
   - 네트워크·디스크·압축 코덱에 따라 다르지만, 실무에선 **한 파티션당 수 MB/s** 정도가 일반적이다. 
   - 예비치: `5 – 20 MB/s/partition` (이건 적당히 알아서)
2. **목표 처리량 ÷ 파티션당 처리량**으로 최소 파티션 개수 계산
   - 예: 300 MB/s ÷ 10 MB/s ≈ 30 파티션
3. **컨슈머 병렬성 반영**
   - 목표 동시 소비 스레드가 40이면, 파티션을 **40 이상**으로 설정이 필요하다.
4. **안전 계수 적용**
   - 피크 대비 여유, 스케일아웃 가능성 고려 → **× 1.5 ~ 3** 배
   - 예: 30 × 2 = **60 파티션** 
5. **토픽당 파티션 상한 점검**
   - 브로커 파일 핸들/메모리/Controller 메타데이터 부하 확인한다.
   - 수천 단위 파티션은 운영 난이도도가 높다. kafka 페이지가면 권장 개수가 있으니 참고

## 3) 필수 고려 항목
### A. 메시지 크기·배치
- `batch.size`, `linger.ms`로 **프로듀서 배치 효율**을 높이면 파티션당 처리량이 증가
- 큰 메시지는 **압축(codec: lz4/zstd/snappy)** 로 네트워크 절감
- `max.request.size`, `message.max.bytes` 상한 확인

### B. 로그 세그먼트/압축/보존
- 세그먼트 크기: `log.segment.bytes` (기본 1GB 권장 영역) 
- 보존: `retention.ms` 또는 `retention.bytes`(토픽/브로커)로 결정
- 장보존·대용량이면 파티션 수보다 **세그먼트·보존 정책** 최적화가 먼저
  - 왜? 이유 확인이 필요한 내용

### C. ISR/Replication
- 복제 팩터(`--replication-factor`) 증가 시 **쓰기 지연 증가**한다.
- `min.insync.replicas` 높으면 내구성 높아지는 대신 쓰기 성공률 내려간다. → 처리량·지연 트레이드오프

### D. 키 분포·스큐
- 키 해시가 고르지 못하면 특정 파티션 과열
- **Salting/키 재설계/Partitioner 커스터마이즈** 검토

### E. 브로커 자원 한계 가늠치
- 파티션 수가 증가할수록 **open file handles, page cache, controller 메타데이터** 부담이 커진다. 
- 토픽 × 파티션 총합이 수만을 넘기면 클러스터 설계·운영 자동화 필요(모니터링/리밸런싱/데이터 재분배)

## 4) 계산 예시
### 예시 1: 1 TB/일, 평균 1 KB 메시지
- 총 레코드 수: `1 TB / 1 KB ≈ 1e12 / 1e3 = 1e9 (10억건/일)`  
- 초당 레코드: `1e9 / 86400 ≈ 11574 rec/s` (≈ 11.3k rps)  
- 대역폭(압축 전): `11.3 MB/s`  
- 한 파티션 10 MB/s 가정 → **2 파티션**으로도 가능.  
- 컨슈머 동시성 8개 목표 + 피크 ×2 → **16–24 파티션**으로 시작.

### 예시 2: 300 MB/s 지속 트래픽
- 한 파티션 10 MB/s 가정 → 30 파티션
- 컨슈머 40 스레드 목표 → **≥ 40**
- 안전 계수 1.5x → **60 파티션** 권고

## 5) 운영 체크리스트
- **프로듀서**: `acks=all`, `linger.ms`, `batch.size`, `compression.type`, `max.in.flight.requests.per.connection`  
- **브로커**: `num.io.threads`, `num.network.threads`, `socket.send/receive.buffer.bytes`, `log.segment.bytes`, `log.retention.ms/bytes`  
- **토픽**: 파티션·복제 팩터, `min.insync.replicas`  
- **컨슈머**: `max.poll.interval.ms`, `max.partition.fetch.bytes`, `fetch.max.bytes`, `session.timeout.ms`, 오토 커밋 주기  
- **관측**: 파티션별 lag, P99 fetch/produce latency, broker IO wait, GC, network utilization

## 6) 변경 전략
- **증설은 쉬움**(파티션 수 증가) / **감소는 어렵다**(리파티셔닝 필요, 사실상 불가능)  
- 초기에 **적정 이상**으로 잡고, 소비자 스케일로 병렬성 조절하자
- 불균형 발생 시 **kafka-reassign-partitions** 또는 **Cruise Control**로 리밸런싱
