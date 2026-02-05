
## 인증과 인가

### 인증 (Authentication)
- **정의**: "누구인지"를 확인하는 과정
- 사용자가 주장하는 신원을 증명하는 단계
- 대표적인 방식
  - 아이디/비밀번호 로그인
  - OTP, 이메일/문자 인증
  - 생체인증(지문, 얼굴 인식)
  - 인증서, 토큰 기반 인증

### 인가 (Authorization)
- **정의**: "무엇을 할 수 있는지"를 결정하는 과정
- 인증이 끝난 사용자가 어떤 자원(Resource)에 접근 가능한지 권한을 부여하거나 제한
- 대표적인 방식
  - Role-Based Access Control (RBAC, 역할 기반 접근 제어)
  - Attribute-Based Access Control (ABAC, 속성 기반 접근 제어)
  - ACL(Access Control List)

### 관계

- 인증이 **먼저**, 인가가 **그다음**에 수행된다.
  1. 로그인 → 인증 (사용자 신원 확인)
  2. 권한 확인 → 인가 (특정 기능/데이터 접근 여부 결정)

---

## Authentication / Authorization Protocols and token format

### OAuth 2.0
- 권한 부여 프레임워크, 클라이언트가 리소스 소유자 대신 보호 자원에 제한적 접근권을 얻는 표준

### OpenID Connect (OIDC)
- OAuth 2.0 위에 **신원 계층**을 더한 표준, 사용자를 인증하고 **ID 토큰**(JWT)을 발급
- **ID 토큰 vs Access 토큰**
  - ID 토큰은 “누가 로그인했는가”를 앱이 검증할 때 사용
  - Access 토큰은 API 접근 권한 증빙에 사용
  - 혼용 금지
- OAuth로는 권한을 위임하고, OIDC로는 사용자 신원을 확인한다.
- 
### SAML 2.0
- XML 기반 엔터프라이즈 SSO 표준, 주로 브라우저 SSO 연동에 사용.

### JWT
- 토큰 **형식**(헤더.페이로드.서명). OIDC의 ID 토큰 형식으로 사용되며, Access 토큰으로도 쓰일 수 있음(표준은 형식만 정의)
- **검증 포인트**: 서명, `iss`/`aud`/`exp` 등 클레임 검증이 필수. 

### 언제 무엇을 쓰나
- **웹/모바일 로그인**: OIDC(+Authorization Code + PKCE)
- **엔터프라이즈 SSO(기존 SAML 인프라)**: SAML 2.0
- **서버 간/머신 간 API 권한 부여**: OAuth 2.0(Client Credentials 등) + Bearer 토큰

