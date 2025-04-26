
# Jackson vs Gson

## 성능 비교

| 항목 | Jackson | Gson |
|:-----|:--------|:-----|
| 직렬화 속도 | 빠름 | 느림 |
| 역직렬화 속도 | 빠름 | 느림 |
| 메모리 사용량 | 효율적 | 약간 비효율적 |
| 대용량 데이터 처리 | 강함 | 상대적으로 약함 |

- Jackson은 스트리밍 API(JsonParser, JsonGenerator) 덕분에 메모리 사용을 최소화하면서 빠르게 처리 가능
- Gson은 객체를 모두 메모리에 올리고 변환하기 때문에 대용량 처리 시 부하가 큼

---

## 확장성 비교

| 항목 | Jackson                            | Gson |
|:-----|:-----------------------------------|:-----|
| 플러그인/모듈 지원 | 다양 (Java 8, Kotlin, Afterburner 등) | 거의 없음 |
| 데이터 형식 지원 | JSON, XML, YAML 등 다양한 포맷 지원        | JSON만 지원 |
| 설정 유연성 | 매우 높음                              | 기본적인 수준 |

- Jackson은 별도 모듈 추가로 다양한 기능 확장 가능
- Gson은 경량 구조라 확장성 자체가 제한적임

---

## POJO 매핑 커스터마이징 비교

| 항목 | Jackson | Gson |
|:-----|:--------|:-----|
| 필드명 매핑 변경(@JsonProperty) | 지원 | 지원 (@SerializedName) |
| 필터링(@JsonIgnore) | 강력 지원 | 일부 지원 |
| 복잡한 매핑 전략 | 쉽게 지원 (커스텀 Serializer/Deserializer 제작 편리) | 비교적 불편함 |
| 뷰/그룹별 직렬화(@JsonView) | 지원 | 없음 |

- Jackson은 @JsonProperty, @JsonIgnore, @JsonInclude 등 다양한 어노테이션 제공
- Gson은 @SerializedName 정도만 기본 제공, 복잡한 매핑은 직접 핸들링해야 함

---

## 요약

| 항목 | Jackson | Gson |
|:-----|:--------|:-----|
| 성능 | 빠름 | 느림 |
| 확장성 | 매우 높음 | 제한적 |
| POJO 커스터마이징 | 강력함 | 기본적 수준 |

- 실무에서는 Jackson을 더 선호 (성능, 확장성, 커스터마이징 모두 우수)
- Gson은 경량이고 단순한 JSON 변환이 필요할 때 적합
