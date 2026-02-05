## NumPy
- ndarray (np.array): 넘파이를 통해 생성되는 N차원 배열, 파이썬 리스트와 유사하지만 수치 연산에 최적화됨

## Pandas
- Series: 1차원 데이터 배열 (index + value)
- DataFrame: 행과 열로 구성된 2차원 데이터 테이블

## 파일 입출력 옵션
- index_col: 파일 로드시 특정 열을 인덱스로 설정
- usecols: 특정 컬럼만 불러오기
- crosstab: 교차표(빈도표) 생성

## DataFrame 속성/메서드
- shape: (행, 열) 반환
- columns: 컬럼명 확인
- info(): 데이터 요약 (컬럼, 결측치, 타입)
- describe(): 통계량 요약 (수치형 기준)
- dtypes: 각 컬럼 데이터 타입
- value_counts(): 특정 컬럼 값의 빈도수 집계

## 인덱싱
- 팬시 인덱싱: 리스트/배열로 다중 선택
- slicing: 범위 선택
- loc: 라벨 기반 인덱싱
- iloc: 정수 기반 인덱싱

## 데이터 조작
- drop: 행/열 삭제
- inplace=True: 원본에 적용
- groupby: 그룹별 연산
- set_index: 특정 컬럼을 인덱스로 설정
- aggregate(agg): 여러 통계량 연산

## 피벗
- pivot: 단일 값 변환 (중복 불가)
- pivot_table: 집계 가능 (중복 허용, aggfunc 사용)

## stack/unstack
- stack(): 열 → 행 변환
- unstack(): 행 → 열 변환

## 데이터 결합
- concat: 행/열 방향으로 이어붙이기
- join: 인덱스 기준 결합
- merge: SQL 방식 결합 (on, how 옵션 사용)
- verify_integrity: 중복 인덱스 발생 시 오류 체크 옵션
