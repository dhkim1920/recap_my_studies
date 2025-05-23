# 네트워크 기초 개념 정리

## 통신 모델 (OSI 7계층)

| 계층 | 설명 | 예시 |
|:-----|:-----|:-----|
| 응용 (Application) | 사용자 인터페이스 | HTTP, FTP |
| 표현 (Presentation) | 데이터 변환, 암호화 | JPEG, SSL |
| 세션 (Session) | 연결 제어, 동기화 | NetBIOS |
| 전송 (Transport) | 신뢰성 보장 | TCP, UDP |
| 네트워크 (Network) | 주소 지정, 경로 결정 | IP, ICMP |
| 데이터링크 (Data Link) | 물리적 주소, 오류 감지 | Ethernet, MAC 주소 |
| 물리 (Physical) | 실제 전기 신호 | 케이블, 허브 |

### 계층별 주요 프로토콜과 네트워크 장비

#### 1. 물리 계층 (Physical Layer)
- **역할**: 실제 비트(0/1)를 전기적/광학적 신호로 변환하여 전송
- **장비**: 케이블 (UTP, 광케이블), 허브, 리피터
- **특징**: 신호 전송만 담당, 주소 개념 없음

#### 2. 데이터 링크 계층 (Data Link Layer)
- **역할**: 프레임 단위 전송, MAC 주소 기반 통신
- **에러 감지**, **흐름 제어** 수행
- **장비**: 스위치, 브리지
- **프로토콜**: Ethernet, PPP, ARP

#### 3. 네트워크 계층 (Network Layer)
- **역할**: 패킷 전달 및 라우팅 (출발지 → 목적지)
- **IP 주소** 기반 주소 지정
- **장비**: 라우터
- **프로토콜**: IP (IPv4/IPv6), ICMP, IGMP

#### 4. 전송 계층 (Transport Layer)
- **역할**: 신뢰성 보장, 세그먼트 단위 전송
- **TCP**: 연결 지향, 흐름 제어, 혼잡 제어, 순서 보장
- **UDP**: 비연결성, 빠름, 단순 데이터그램 전송

#### 5~7. 세션/표현/응용 계층 (Session, Presentation, Application)
- TCP/IP 모델에서는 응용 계층으로 통합
- **응용 계층의 역할**: 사용자 인터페이스 제공, 전송 포맷 정의
- **프로토콜**: HTTP, HTTPS, FTP, SMTP, DNS, DHCP

---

### 프로토콜과 인접지역 트래픽

- **브로드캐스트 (Broadcast)**: 같은 네트워크 상 모든 장치로 전송
  - 예: ARP 요청
- **멀티캐스트 (Multicast)**: 특정 그룹에만 전송 (ex. IPTV)
- **유니캐스트 (Unicast)**: 특정 하나의 대상에만 전송 (일대일)

#### 방화벽 (Firewall)
- 포트, IP, 프로토콜 기반으로 접근 제어
- 인바운드/아웃바운드 트래픽 필터링


---

## NAT (Network Address Translation)

- 사설 IP ↔ 공인 IP 변환 기술
- 내부 네트워크 장비들이 인터넷에 나갈 수 있게 해줌
- IP 부족 문제 해결, 기본적인 보안 기능 제공

---

## DNS (Domain Name System)

- 도메인 이름(ex: www.google.com)을 IP 주소(ex: 142.250.206.68)로 변환해주는 시스템
- 이름 → IP 매핑

---

## DHCP (Dynamic Host Configuration Protocol)

- 자동으로 IP 주소를 할당해주는 프로토콜
- 네트워크 연결 시 IP, 서브넷 마스크, 게이트웨이, DNS 등을 자동으로 할당

---

## NTP (Network Time Protocol)

- 네트워크 상의 모든 시스템 시계를 정확하게 동기화하는 프로토콜

---

## 프록시 (Proxy)

- 클라이언트와 서버 사이에 중간에 위치해서 요청을 대신 처리하는 서버
- 클라이언트가 직접 서버에 요청하지 않고 프록시 서버를 거쳐 요청하고, 결과를 받아온다.

### 동작 흐름
1. 클라이언트 → 프록시 서버에 요청
2. 프록시 서버 → 실제 서버에 요청
3. 실제 서버 → 프록시 서버에 응답
4. 프록시 서버 → 클라이언트에 응답

### 프록시 주요 목적

| 목적 | 설명 |
|:-----|:-----|
| 보안 | 클라이언트 IP를 숨기고 서버에 접근 |
| 캐싱 | 자주 요청되는 데이터를 저장해 빠른 응답 제공 |
| 접근 제어 | 특정 사이트 차단, 트래픽 제한 가능 |
| 로드 밸런싱 | 요청을 여러 서버로 분산시켜 부하 분산 |
| 로깅/모니터링 | 트래픽을 중간에서 감시하고 기록 |

### 프록시 종류

| 종류 | 설명 |
|:-----|:-----|
| 포워드 프록시 (Forward Proxy) | 클라이언트 → 서버 요청 대리 |
| 리버스 프록시 (Reverse Proxy) | 서버 앞에 두고 외부 요청을 서버 대신 받음 |

---

## 로드 밸런서 (Load Balancer)

- 들어오는 트래픽을 여러 서버로 분산시켜주는 장비나 소프트웨어이다.

### 동작 흐름
1. 클라이언트 → 로드 밸런서에 요청
2. 로드 밸런서 → 여러 서버 중 하나에 요청 전달
3. 서버 → 로드 밸런서 → 클라이언트로 응답

### 로드 밸런싱 방식

| 방식 | 설명 |
|:-----|:-----|
| 라운드 로빈 (Round Robin) | 서버들을 순서대로 골고루 분배 |
| 최소 연결 (Least Connection) | 현재 연결 수가 가장 적은 서버로 분배 |
| IP 해시 (IP Hash) | 클라이언트 IP 기반으로 고정 서버에 분배 |
| 가중치 라운드 로빈 (Weighted Round Robin) | 서버마다 가중치를 다르게 설정해 분배 |
| 건강 체크 (Health Check) | 서버 상태를 주기적으로 점검하고, 죽은 서버는 제외 |

### 로드 밸런서 종류

| 종류 | 설명 |
|:-----|:-----|
| 하드웨어 로드 밸런서 | 전용 장비 (F5, A10 등) |
| 소프트웨어 로드 밸런서 | 소프트웨어 기반 (Nginx, HAProxy) |
| 클라우드 로드 밸런서 | AWS ELB, GCP Load Balancer 등 |

### 로드 밸런서 vs 리버스 프록시

| 항목 | 로드 밸런서 | 리버스 프록시 |
|:-----|:------------|:--------------|
| 주목적 | 트래픽 분산 | 요청 중개 및 서버 보호 |
| 대상 | 여러 서버 | 하나 또는 소수 서버 |
| 예시 | AWS ELB, HAProxy | Nginx, Apache HTTP Server |

---

## 라우터(Router)와 스위치(Switch)

| 항목 | 라우터 (Router) | 스위치 (Switch) |
|:-----|:----------------|:----------------|
| 기본 역할 | 다른 네트워크 간 연결 (IP 기반) | 같은 네트워크 내 장비 연결 (MAC 기반) |
| 기준 정보 | IP 주소 | MAC 주소 |
| 주 용도 | 네트워크 간 트래픽 라우팅 | 네트워크 내부 통신 |
| 계층 (OSI) | 3계층 | 2계층 |
| 주요 기능 | 라우팅, NAT, DHCP, 방화벽 | MAC 주소 학습, 브로드캐스트 분할 |
| 예시 | 공유기, 기업 라우터 | 사무실/서버실 스위치 |

---

### L2 스위치 vs L3 스위치

| 항목 | L2 스위치 (Layer 2 Switch) | L3 스위치 (Layer 3 Switch) |
|:-----|:---------------------------|:---------------------------|
| 기준 계층 | 2계층 | 3계층 |
| 처리 기준 | MAC 주소 | IP 주소 |
| 주요 역할 | 같은 세그먼트 장치 연결 | 서로 다른 세그먼트 연결 (라우팅) |
| 라우팅 기능 | 없음 | 있음 |
| 주 사용처 | 사무실 LAN | 데이터센터 VLAN 간 통신 |

---

## Packet

패킷은 네트워크에서 **데이터를 전송하기 위해 일정한 형식으로 나눈 작은 데이터 단위**

### 패킷의 구성 요소

| 구성 요소 | 설명 |
|-----------|------|
| **Header**  | 출발지/목적지 주소, 패킷 번호, 프로토콜 정보 등 제어 정보 포함 |
| **Payload** | 실제 전송하려는 데이터 |
| **Trailer** | 오류 검출 정보 등 (필요 시 사용) |

### 패킷 전송의 이유

- **효율성**: 네트워크 자원을 효율적으로 사용하며 동시 처리 가능  
- **신뢰성**: 일부 패킷만 재전송 가능하여 전체 재전송 불필요  
- **유연성**: 서로 다른 경로로 전송되어 혼잡 회피 가능

### 패킷 전송 과정

1. 전송할 데이터를 일정 크기로 나눈다.
2. 각 조각에 헤더/트레일러를 붙여 패킷을 만든다.
3. 패킷들을 네트워크를 통해 전송한다.
4. 수신 측에서 순서대로 재조립하여 원래 데이터를 복원한다.

> 이 방식은 **Packet Switching** 이라 하며, 현대 인터넷 통신의 핵심 구조


---

## Socket Communication

- 소켓은 네트워크를 통해 데이터를 주고받기 위한 연결 포인트다.
- 소켓은 IP 주소 + 포트 번호 조합으로 식별된다.

### 소켓 통신 기본 흐름

| 단계 | 클라이언트 | 서버 |
|:-----|:-----------|:-----|
| 서버 IP와 포트로 연결 요청 | 서버 소켓 생성하고 대기 |
| 연결 요청 전송 | 연결 요청 수락 (Accept) |
| 데이터 송신/수신 | 데이터 송신/수신 |
| 통신 종료 | 통신 종료 및 소켓 닫기 |

---

## Subnetting (서브넷 분할)

- IP 네트워크를 더 작은 네트워크로 나누는 것
- 서브넷 마스크로 네트워크/호스트 영역 구분

### 서브넷 나누기 예시

| 서브넷 | IP 범위 |
|:-------|:--------|
| 192.168.1.0/26 | 192.168.1.0 ~ 192.168.1.63 |
| 192.168.1.64/26 | 192.168.1.64 ~ 192.168.1.127 |
| 192.168.1.128/26 | 192.168.1.128 ~ 192.168.1.191 |
| 192.168.1.192/26 | 192.168.1.192 ~ 192.168.1.255 |

### 서브넷 마스크 표

| CIDR 표기 | 서브넷 마스크 | 호스트 수 (실제 사용 가능) |
|:----------|:--------------|:---------------------------|
| /24 | 255.255.255.0 | 254개 |
| /25 | 255.255.255.128 | 126개 |
| /26 | 255.255.255.192 | 62개 |
| /27 | 255.255.255.224 | 30개 |
| /28 | 255.255.255.240 | 14개 |
| /29 | 255.255.255.248 | 6개 |

---

## CIDR (Classless Inter-Domain Routing)

- IP 주소 뒤에 슬래시(`/`)와 숫자를 붙여서 네트워크 범위를 표기하는 방식이다.

### CIDR 표기법 예시

| 표기 | 의미 |
|:-----|:-----|
| 192.168.1.0/24 | 앞 24비트가 네트워크 주소 |
| 10.0.0.0/8 | 앞 8비트가 네트워크 주소 |
| 172.16.0.0/16 | 앞 16비트가 네트워크 주소 |

### CIDR과 서브넷 마스크 관계

| CIDR | 서브넷 마스크 | 사용할 수 있는 호스트 수 |
|:----|:--------------|:--------------------------|
| /8 | 255.0.0.0 | 16,777,214개 |
| /16 | 255.255.0.0 | 65,534개 |
| /24 | 255.255.255.0 | 254개 |
| /26 | 255.255.255.192 | 62개 |
| /28 | 255.255.255.240 | 14개 |

---