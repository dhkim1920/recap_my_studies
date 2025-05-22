# Hadoop NameNode RPC 성능 모니터링 및 개선 설정

## 중요 모니터링 지표 (Top 3)

| 지표명                  | 설명                              | 임계값                        |
|-----------------------|----------------------------------|-----------------------------|
| **CallQueueLength**   | 현재 RPC 큐에 대기 중인 요청 수           | 100 이상 시 과부하 의심             |
| **RpcQueueTimeAvgTime** | 요청이 큐에서 대기한 평균 시간            | 100ms 이상 시 주의, 500ms 이상 시 심각 |
| **NumOpenConnections** | 현재 열린 RPC 연결 수                  | 평상시 대비 2배 이상이면 연결 누수 가능성 |

---

## 왜 처리 속도보다 큐 길이가 중요한가

1. **포화 상태 조기 경고**: 큐 길이는 시스템이 처리 한계에 도달했음을 즉시 보여줌  
2. **장애의 원인 추적**: 큐 증가 → 지연 → 처리 속도 저하 순  
3. **예측 가능한 임계점**: 처리 속도는 이미 늦은 결과  
4. **회복 시간 차이**: 큐는 누적이므로 복구에 오래 걸림  
5. **사용자 체감 지연 직접 반영**

---

## 성능 개선 설정 (권장 적용 순서)

### 1. Fair Call Queue 활성화
- heavy user의 과도한 요청 방어

```xml
<property>
  <name>ipc.8020.callqueue.impl</name>
  <value>org.apache.hadoop.ipc.FairCallQueue</value>
</property>
```

### 2. Handler 수 증가
- 동시 RPC 처리 스레드 확장

```xml
<property>
  <name>dfs.namenode.handler.count</name>
  <value>100</value> <!-- 기본값: 10 -->
</property>
```

### 3. Backoff 메커니즘 활성화
- 과도한 지연 요청 차단

```xml
<property>
  <name>ipc.8020.backoff.enable</name>
  <value>true</value>
</property>
<property>
  <name>ipc.8020.decay-scheduler.backoff.responsetime.thresholds</name>
  <value>10s,20s</value>
</property>
```

### 4. DecayRpcScheduler 적용
- 사용자별 요청 우선순위 자동 감소

```xml
<property>
  <name>ipc.8020.scheduler.impl</name>
  <value>org.apache.hadoop.ipc.DecayRpcScheduler</value>
</property>
<property>
  <name>ipc.8020.scheduler.priority.levels</name>
  <value>4</value>
</property>
```

### 5. Cost-based 우선순위 설정
- 연산 시간에 따라 가중치 기반 처리

```xml
<property>
  <name>ipc.8020.costprovder.impl</name>
  <value>org.apache.hadoop.ipc.WeightedTimeCostProvider</value>
</property>
```