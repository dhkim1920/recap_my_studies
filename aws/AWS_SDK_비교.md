
# AWS SDK

## SDK v1 vs SDK v2 차이

- **모듈화**  
  - v1: 전체 SDK 의존성 필요  
  - v2: 서비스 별 모듈만 추가 가능

- **비동기**  
  - v1: 별도 구현 필요  
  - v2: 기본 제공 (Non-blocking I/O, Netty 기반)
    - Netty는 적은 스레드로 수많은 요청을 처리하는 고성능 비동기 네트워크 프레임워크

- **빌더 패턴**  
  - v2: 객체 생성과 요청 모두 빌더 패턴 적용 (가독성, 안전성 우수)

- **성능**  
  - v2: 넌블로킹 기반으로 비동기 시 성능 우수

---

## S3AsyncClient 클라이언트 객체

- AWS SDK for Java v2에서 비동기 S3 작업 지원
- `software.amazon.awssdk.services.s3.S3AsyncClient`
- 내부적으로 Netty 기반 비동기 HTTP 클라이언트 사용

**생성 예시)**
```java
S3AsyncClient s3AsyncClient = S3AsyncClient.builder()
    .region(Region.AP_NORTHEAST_2)
    .credentialsProvider(ProfileCredentialsProvider.create())
    .build();
```

---

## 참고
### Blocking I/O vs Non-blocking I/O

| 구분 | Blocking I/O (BIO) | Non-blocking I/O (NIO, Netty) |
|:-----|:------------------|:-----------------------------|
| 모델 | 요청마다 스레드 1개 사용 | 여러 요청을 하나의 스레드가 관리 |
| 연결 수 | 스레드 수 == 연결 수 | 스레드 수 << 연결 수 |
| 대기 방식 | 읽거나 쓸 때까지 스레드 블로킹 | 읽을 데이터 있을 때만 처리 |
| 성능 | 동시 처리량 낮음 | 초당 수천~수만 연결 처리 가능 |
| 예시 | 기본 Java Socket | Netty, AWS SDK v2 AsyncClient |


