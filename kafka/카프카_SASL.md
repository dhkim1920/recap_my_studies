
# Apache Kafka SASL 

## SASL이란?
SASL(Simple Authentication and Security Layer)은 클라이언트와 브로커 간의 인증을 위한 프레임워크

### 1. SASL/PLAIN
- **설명**: 사용자 이름과 비밀번호를 평문으로 전송하는 간단한 인증 방식
- **보안 고려사항**: TLS(SSL)과 함께 사용해야 자격 증명이 암호화
- **클라이언트 구성 예시**
  ```properties
  security.protocol=SASL_SSL
  sasl.mechanism=PLAIN
  sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="user" password="pass";
  ```

### 2. SASL/SCRAM
- **설명**: 해시된 비밀번호를 사용하는 인증 방식으로 보안성이 높다.
- **사용 예시**
  ```bash
  bin/kafka-configs.sh --zookeeper localhost:2181 --alter --add-config 'SCRAM-SHA-512=[password=secret]' --entity-type users --entity-name user1
  ```

### 3. SASL/OAUTHBEARER
- **설명**: OAuth 2.0 토큰을 사용하는 인증 방식
- **구성 예시**
  ```properties
  security.protocol=SASL_SSL
  sasl.mechanism=OAUTHBEARER
  sasl.jaas.config=org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;
  ```

### 4. SASL/GSSAPI (Kerberos)
- **설명**: Kerberos를 사용하는 인증 방식
- **구성 예시**
  ```properties
  security.protocol=SASL_SSL
  sasl.mechanism=GSSAPI
  sasl.kerberos.service.name=kafka
  ```

---

## SASL 구성 방법

### 1. JAAS 설정 파일 작성

#### 브로커용 (`kafka_server_jaas.conf`)
```plaintext
KafkaServer {
  org.apache.kafka.common.security.plain.PlainLoginModule required
  username="admin"
  password="admin-secret"
  user_admin="admin-secret"
  user_alice="alice-secret";
};
```

#### 클라이언트용 (`kafka_client_jaas.conf`)
```plaintext
KafkaClient {
  org.apache.kafka.common.security.plain.PlainLoginModule required
  username="alice"
  password="alice-secret";
};
```

### 2. Kafka 브로커 설정 (`server.properties`)
```properties
listeners=SASL_PLAINTEXT://<KAFKA_HOST>:<KAFKA_PORT>
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN
```

### 3. Kafka 브로커 환경변수 설정
```bash
export KAFKA_OPTS="-Djava.security.auth.login.config=/path/to/kafka_server_jaas.conf"
```

### 4. 클라이언트 설정
```properties
security.protocol=SASL_PLAINTEXT
sasl.mechanism=PLAIN
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="alice" password="alice-secret";
```

---

## TLS와 함께 구성하는 방법

### 1. TLS 인증서 생성
```bash
keytool -keystore kafka.server.keystore.jks -alias broker -validity 365 -genkey -keyalg RSA
openssl req -new -x509 -keyout ca-key -out ca-cert -days 365
keytool -keystore kafka.server.truststore.jks -alias CARoot -import -file ca-cert
```

### 2. 브로커 설정
```properties
listeners=SASL_SSL://:9093
advertised.listeners=SASL_SSL://localhost:9093
security.inter.broker.protocol=SASL_SSL
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-512
sasl.enabled.mechanisms=SCRAM-SHA-512

ssl.keystore.location=/path/to/kafka.server.keystore.jks
ssl.keystore.password=<keystore-password>
ssl.key.password=<key-password>
ssl.truststore.location=/path/to/kafka.server.truststore.jks
ssl.truststore.password=<truststore-password>
ssl.client.auth=required
```

### 3. 클라이언트 설정
```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="admin" password="admin-secret";
ssl.truststore.location=/path/to/kafka.client.truststore.jks
ssl.truststore.password=<truststore-password>
```

### 4. 사용자 등록
```bash
bin/kafka-configs.sh --zookeeper localhost:2181 --alter --add-config 'SCRAM-SHA-512=[password=admin-secret]' --entity-type users --entity-name admin
```

---

## ZooKeeper와 SASL 연동 설정

### ZooKeeper 설정 (`zookeeper.properties`)
```properties
authProvider.1=org.apache.zookeeper.server.auth.SASLAuthenticationProvider
requireClientAuthScheme=sasl
jaasLoginRenew=3600000
```

### ZooKeeper JAAS 설정 (`zookeeper_jaas.conf`)
```plaintext
Server {
  org.apache.zookeeper.server.auth.SASLAuthenticationProvider required
  user_kafka="kafka-password";
};
```

### Kafka 브로커 JAAS 설정
```plaintext
Client {
  org.apache.zookeeper.server.auth.SASLAuthenticationProvider required
  username="kafka"
  password="kafka-password";
};
```

### Kafka 브로커 환경변수
```bash
export KAFKA_OPTS="-Djava.security.auth.login.config=/path/to/kafka_server_jaas.conf"
```

---

## SASL 사용 여부에 따른 장단점

### SASL 사용 시

**장점**
- 인증 기능 제공
- 다양한 인증 메커니즘 지원
- 기존 인증 인프라와 통합 가능

**단점**
- 설정 복잡성 증가
- 성능 저하 가능성
- 운영 부담 증가

### SASL 미사용 시

**장점**
- 구성 간편
- 낮은 운영 부담
- 성능 최적화

**단점**
- 보안 취약성
- 규제 준수 어려움
- 접근 제어 불가
