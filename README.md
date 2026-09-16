# HR Data Pipeline

노트북에서 한 번 분석하던 IBM HR 데이터를 반복해서 검증하고 적재할 수 있도록 Python 코드, PostgreSQL, Airflow, FastAPI로 확장한 데이터 파이프라인입니다.

이 프로젝트의 핵심은 이직률 분석 결과 자체보다 **어떤 데이터가 들어와야 하는지, 잘못된 데이터는 어디서 막는지, DB에 어떻게 안전하게 적재하고 다시 같은 결과를 만들 수 있는지**를 코드로 설명하는 것입니다.

---

## 1. 프로젝트 핵심

초기 프로젝트에서는 IBM HR 데이터를 노트북에서 정제하고 부서별 이직률, 급여, 업무 부담을 분석했습니다.

저장소의 실제 집계 결과:

| 부서 | 직원 수 | 평균 월급 | 이직률 |
|---|---:|---:|---:|
| Sales | 446 | 6,959.17 | **20.63%** |
| Human Resources | 63 | 6,654.51 | **19.05%** |
| Research & Development | 961 | 6,281.25 | **13.84%** |

![부서별 이직률](docs/assets/department_attrition.svg)

하지만 노트북 중심 구조에는 다음 문제가 있었습니다.

1. 셀 실행 순서에 따라 결과가 달라질 수 있음
2. 잘못된 데이터가 들어와도 초기에 자동 차단되지 않음
3. 결과를 다른 서비스가 사용하려면 CSV나 노트북을 다시 직접 읽어야 함

그래서 다음 구조로 바꿨습니다.

```text
원본 HR CSV
  ↓
데이터 품질 검사
  ├─ 필수 열 확인
  ├─ 직원 ID 중복 확인
  ├─ 잘못된 급여 값 확인
  ├─ 이직 여부 값 범위 확인
  └─ 필수값 누락 확인
  ↓
데이터 변환
  ├─ 직원 차원 테이블
  ├─ 이직 사실 테이블
  └─ 부서별 집계 테이블
  ↓
PostgreSQL 트랜잭션 적재
  ↓
Airflow 실행 관리
  ↓
FastAPI 조회 API
```

---

## 2. 왜 데이터 품질 검사를 앞에 두었는가

이직률 계산식이 맞더라도 원본 데이터가 잘못되어 있으면 결과를 신뢰할 수 없습니다.

예:
- 같은 `EmployeeNumber`가 두 번 존재
- `MonthlyIncome`이 음수
- `Attrition`에 `Yes/No`가 아닌 값 존재
- 필수 열 또는 필수값 누락

현재 검사 규칙:

| 검사 대상 | 실패 조건 | 목적 |
|---|---|---|
| 스키마 | 필수 열 누락 | 이후 변환 단계 오류 방지 |
| 직원 ID | `EmployeeNumber` 중복 | 동일 직원 중복 집계 방지 |
| 급여 | `MonthlyIncome < 0` | 비정상 값 차단 |
| 이직 여부 | `Yes/No` 외 값 | 이직 지표 정합성 유지 |
| 필수값 | NULL 존재 | DB 적재 전에 오류 발견 |

검사에 실패한 행을 임의로 버리고 계속 진행하지 않습니다. 어느 값이 맞는지 시스템이 알 수 없는 경우에는 **파이프라인 전체를 실패시켜 원본 데이터를 확인하도록 하는 편이 안전하다**고 판단했습니다.

---

## 3. 분석 결과를 인과관계로 과장하지 않음

Sales 부서의 이직률이 다른 부서보다 높게 나타났지만, 이것만으로 특정 변수가 이직의 원인이라고 단정하지 않습니다.

이 데이터는 관찰 데이터이므로 분석 결과는 **추가 검증이 필요한 가설을 만드는 근거**로 사용합니다.

예를 들어 초과근무, 직무, 급여와 이직률 사이의 관계를 볼 수는 있지만 그것이 직접적인 원인이라는 결론에는 추가 실험이나 인과 분석이 필요합니다.

---

## 4. 데이터 모델

노트북에서는 하나의 DataFrame으로 사용하던 데이터를 조회 목적과 무결성 기준에 따라 세 테이블로 나눴습니다.

### `hr_employees`

직원의 비교적 안정적인 속성을 보관하는 **직원 차원 테이블**입니다.

```text
employee_id PK
department
job_role
monthly_income CHECK >= 0
overtime
total_working_years
years_at_company
```

### `hr_attrition_facts`

직원별 이직 여부를 보관하는 **이직 사실 테이블**입니다.

```text
employee_id PK/FK -> hr_employees
attrited CHECK IN (0, 1)
```

### `hr_department_summary`

API에서 자주 조회하는 부서별 집계 결과를 미리 저장합니다.

```text
department PK
employee_count
average_income
attrition_rate
```

원본 데이터를 그대로 한 테이블에 복사하기보다 **조회 목적과 무결성 경계를 명확하게 만들기 위해 분리**했습니다.

---

## 5. 왜 `to_sql(replace)`를 사용하지 않았는가

`pandas.to_sql(if_exists="replace")`는 편하지만 기존 테이블을 다시 만들기 때문에 PostgreSQL의 기본키, 외래키, CHECK 제약조건이 사라질 수 있습니다.

현재 방식은 DB 스키마를 먼저 만들고 하나의 트랜잭션 안에서 데이터를 다시 적재합니다.

```text
BEGIN
  기존 이직 사실 삭제
  기존 직원 삭제
  기존 부서 집계 삭제

  직원 데이터 적재
  이직 데이터 적재
  부서 집계 적재
COMMIT
```

중간에 하나라도 실패하면 전체를 롤백하므로 **일부 테이블만 새 데이터로 바뀐 상태를 남기지 않습니다.**

핵심은 데이터를 넣는 것보다 **DB 무결성 규칙을 유지한 채 적재하는 것**입니다.

---

## 6. FastAPI의 역할

FastAPI는 분석을 새로 수행하지 않고, **정제하고 집계한 결과를 다른 시스템이 조회할 수 있게 제공하는 역할**을 맡습니다.

### 상태 확인

```http
GET /health
```

### 부서별 요약

```http
GET /api/v1/departments
```

### 부서별 이직 정보

```http
GET /api/v1/departments/{department}/attrition
```

ETL과 API를 분리한 이유는 실행 특성이 다르기 때문입니다.

```text
ETL
→ 일정 주기로 실행 가능
→ 처리시간이 상대적으로 길어도 됨

조회 API
→ 짧고 안정적인 응답시간 필요
```

---

## 7. 왜 Airflow를 사용했는가

초기에는 사람이 노트북을 직접 실행해야 했습니다.

```text
수동 노트북 실행
  ↓
실행 순서가 사람에게 의존
  ↓
정기 실행 / 실패 확인 / 재시도 필요
  ↓
Airflow로 작업 순서와 실행 상태 관리
```

Airflow를 사용한 이유는 기술 목록을 늘리기 위해서가 아니라 **정해진 순서의 배치 작업을 반복 실행하고 실패 상태를 확인하기 위해서**입니다.

현재 규모에서는 하나의 DAG로 충분합니다.

---

## 8. 왜 Kafka를 사용하지 않았는가

이 프로젝트의 데이터는 계속 들어오는 실시간 이벤트 흐름이 아니라 주기적으로 전체 데이터를 읽어 적재하는 배치 데이터입니다.

따라서 현재 핵심 문제는 이벤트 전달보다 **작업 순서, 데이터 품질, 적재 트랜잭션, 재현성**입니다.

Kafka는 여러 소비자가 실시간 이벤트를 독립적으로 처리해야 하는 `commerce-event-pipeline`에서 별도로 다룹니다.

---

## 9. 인덱스 실험

`scripts/explain_indexes.sql`에서 PostgreSQL `EXPLAIN ANALYZE`로 인덱스 적용 전후를 비교할 수 있게 했습니다.

확인 항목:

```text
계획 시간
실행 시간
Seq Scan / Index Scan
읽은 행 수
```

인덱스가 있다고 무조건 빠른 것이 아니므로 실제 조회 조건과 데이터 크기에서 실행 계획을 확인합니다. 실측하지 않은 개선율은 README 성과로 적지 않습니다.

---

## 10. 장애 상황

### 중복 직원 ID

```text
원본 데이터
EmployeeNumber=10
EmployeeNumber=10
  ↓
데이터 품질 검사
  ↓
파이프라인 실패
```

어느 행이 맞는지 알 수 없기 때문에 자동 삭제하지 않습니다.

### DB 적재 중 실패

```text
직원 데이터 적재 성공
이직 데이터 적재 실패
  ↓
ROLLBACK
```

부분 성공 상태를 남기지 않습니다.

### 적재 중 API 조회

현재는 전체 재적재 중에도 완전한 무중단 조회를 보장하는 테이블 교체 방식을 구현하지 않았습니다. 데이터 규모가 커지고 무중단 갱신이 필요하다면 임시 테이블에 적재한 뒤 짧은 순간에 테이블을 교체하는 방식을 검토할 수 있습니다.

---

## 11. 테스트

### 데이터 품질 테스트

- 정상 데이터가 검사를 통과하는가
- 중복 직원 ID를 검출하는가
- 음수 급여를 검출하는가
- 잘못된 이직 여부 값을 검출하는가
- 필수 열이 없으면 즉시 실패하는가

### 변환 테스트

- 직원 차원 테이블 열 변환
- `Attrition`의 `Yes/No → 1/0` 변환
- 부서별 집계 생성

GitHub Actions에서는 Python 3.11 기준으로 다음을 실행합니다.

```bash
python -m compileall -q src tests orchestration
pytest -q
```

---

## 12. 운영에서 확인할 지표

실제 운영 단계로 확장한다면 다음 값을 관찰할 수 있습니다.

```text
파이프라인 성공 횟수
파이프라인 실패 횟수
품질 검사 거절 건수
원본 행 수
적재 행 수
전체 처리시간
API p95 지연시간
```

현재 구현에 없는 운영 관찰 시스템을 사용했다고 과장하지 않습니다.

---

## 13. 프로젝트 구조

```text
.
├── WA_Fn-UseC_-HR-Employee-Attrition.csv
├── department.ipynb
├── strategy.ipynb
├── simul.ipynb
├── department_summary.csv
├── src/hr_pipeline/
│   ├── quality.py
│   ├── transform.py
│   ├── storage.py
│   ├── pipeline.py
│   └── api.py
├── orchestration/dags/
│   └── hr_pipeline_dag.py
├── scripts/
│   ├── run_pipeline.py
│   └── explain_indexes.sql
├── tests/
│   ├── test_quality.py
│   └── test_transform.py
├── docs/
│   ├── ARCHITECTURE_DECISIONS.md
│   ├── INTERVIEW_GUIDE.md
│   └── assets/
├── docker-compose.yml
└── pyproject.toml
```

---

## 14. 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
docker compose up -d
python scripts/run_pipeline.py
```

API 실행:

```bash
uvicorn hr_pipeline.api:app --app-dir src --reload
```

테스트:

```bash
pytest -q
```

---

## 15. 기존 프로젝트에서 바뀐 점

```text
기존
노트북
→ 수동 정제
→ CSV 집계
→ 발표 자료

현재
원본 CSV
→ 명시적인 데이터 품질 규칙
→ 재사용 가능한 Python 변환 코드
→ 제약조건이 있는 PostgreSQL
→ 트랜잭션 적재
→ Airflow 실행 관리
→ FastAPI 조회 API
→ 자동 테스트
```

핵심 성과는 **분석 결과를 한 번 만드는 데서 끝나지 않고 같은 입력으로 같은 결과를 반복해서 만들 수 있는 구조로 바꾼 것**입니다.

---

## 16. 현재 한계

- 데이터가 1,470행 규모라 분산 처리 엔진이 필요하지 않음
- 현재는 전체 재적재 방식이며 CDC는 사용하지 않음
- Airflow 자체의 고가용성 운영은 범위 밖
- API 인증은 구현하지 않음
- 인덱스 성능 수치는 실제 PostgreSQL 환경에서 측정 후 기록해야 함

기술을 많이 사용하는 것보다 문제 규모에 맞는 구조를 선택하는 것을 우선합니다.

---

## 설계 원칙

> **분석 결과의 정확성만큼 그 결과가 어떤 입력과 규칙으로 만들어졌는지 다시 재현할 수 있는지가 중요합니다.**

원본 데이터가 정해진 규칙을 통과한 경우에만 변환과 적재를 진행하고, 적재가 완료된 결과만 API로 제공합니다.
