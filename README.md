# HR Data Pipeline

IBM HR 데이터를 단순 분석 노트북에 머무르게 하지 않고, **데이터 품질 검증 → 변환 → PostgreSQL 적재 → Airflow 오케스트레이션 → FastAPI 제공**까지 확장한 데이터 엔지니어링 프로젝트입니다.

이 저장소의 목적은 "이직률을 분석했다"는 결과보다, **분석에 쓰이는 데이터가 어떤 규칙으로 검증되고, 어떤 스키마로 저장되며, 어떤 API로 재사용될 수 있는가**를 코드로 설명하는 데 있습니다.

> 원본 Notebook과 CSV는 초기 분석 증거로 보존하고, `src/hr_pipeline/`을 재현 가능한 파이프라인 계층으로 분리했습니다.

---

## 1. Executive Summary

초기 프로젝트에서는 IBM HR Analytics 데이터를 Notebook에서 정제하고 부서별 이직률, 급여, 업무 부담을 분석했습니다. 실제 집계 결과 Sales 부서의 이직률은 약 **20.63%**, Human Resources는 **19.05%**, Research & Development는 **13.84%**로 나타났습니다.

하지만 Notebook 중심 구조에는 세 가지 문제가 있었습니다.

1. 분석자가 셀을 어떤 순서로 실행했는지에 따라 결과가 달라질 수 있음
2. 잘못된 데이터가 들어와도 파이프라인 초기에 자동으로 차단되지 않음
3. 집계 결과를 다른 서비스가 사용하려면 다시 CSV나 Notebook을 직접 읽어야 함

그래서 프로젝트를 다음처럼 재설계했습니다.

```text
Raw HR CSV
    │
    ▼
Data Quality Gate
    │
    ├─ required columns
    ├─ duplicate employee id
    ├─ invalid income
    ├─ invalid attrition domain
    └─ required null
    │
    ▼
Transform
    │
    ├─ employee dimension
    ├─ attrition fact
    └─ department aggregate
    │
    ▼
PostgreSQL Transactional Load
    │
    ▼
Airflow DAG
    │
    ▼
FastAPI Analytics API
```

이 변화의 핵심은 **EDA 결과를 더 화려하게 만드는 것이 아니라, 동일한 입력에서 동일한 결과를 다시 만들 수 있는 데이터 시스템으로 발전시키는 것**입니다.

---

## 2. Problem Definition

### 2.1 분석 정확성보다 먼저 데이터 신뢰성이 필요하다

이직률 분석에서 `EmployeeNumber`가 중복되거나 `MonthlyIncome`이 음수이거나 `Attrition` 값이 `Yes/No` 이외의 값을 가진다면 이후 집계가 아무리 정확해도 결과를 신뢰할 수 없습니다.

따라서 V2에서는 분석 코드보다 앞에 **Data Quality Gate**를 두었습니다.

현재 검증 규칙은 다음과 같습니다.

| Rule | Failure condition | Why it matters |
|---|---|---|
| Schema | 필수 컬럼 누락 | downstream transform 계약 붕괴 방지 |
| Employee ID | 중복 `EmployeeNumber` | 동일 직원 중복 집계 방지 |
| Income | `MonthlyIncome < 0` | 비정상 수치 차단 |
| Attrition | `Yes/No` 이외 값 | binary fact 정합성 보장 |
| Required values | 필수 필드 null | DB 적재 실패를 조기에 발견 |

검증 실패 시 잘못된 값을 조용히 제거하지 않고 **pipeline 자체를 실패**시킵니다. 데이터가 누락된 채 성공하는 것보다 명시적으로 실패하는 편이 운영에서 더 안전하다고 판단했습니다.

---

## 3. Original Analysis and Verified Findings

원본 데이터는 IBM HR Analytics Employee Attrition & Performance 데이터셋이며 1,470명의 직원과 35개 변수를 포함합니다.

기존 분석 결과 중 저장소에 CSV로 남아 있는 부서별 집계는 다음과 같습니다.

| Department | Employees | Average Monthly Income | Attrition Rate |
|---|---:|---:|---:|
| Sales | 446 | 6,959.17 | **20.63%** |
| Human Resources | 63 | 6,654.51 | **19.05%** |
| Research & Development | 961 | 6,281.25 | **13.84%** |

![Verified department attrition](docs/assets/department_attrition.svg)

초기 분석에서는 이 결과를 바탕으로 Sales 조직 안에서 JobRole, OverTime, MonthlyIncome 등 개입 가능한 변수를 더 세분화해 살펴봤습니다.

중요한 점은 이 프로젝트가 **"Sales 이직률이 높으므로 채용을 늘리면 해결된다"고 인과관계를 단정하지 않는다는 것**입니다. 데이터는 관찰 데이터이며, 분석 결과는 원인 확정이 아니라 추가 실험과 정책 검토를 위한 가설로 사용합니다.

---

## 4. Architecture

```text
┌───────────────────────┐
│ IBM HR Raw CSV        │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Quality Validation    │
│ quality.py            │
└──────────┬────────────┘
           │ pass only
           ▼
┌───────────────────────┐
│ Transformation        │
│ transform.py          │
├───────────────────────┤
│ hr_employees          │
│ hr_attrition_facts    │
│ department_summary    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ PostgreSQL            │
│ constraints + tx      │
└──────────┬────────────┘
           │
       ┌───┴───────────────┐
       ▼                   ▼
┌──────────────┐   ┌────────────────┐
│ Airflow DAG  │   │ FastAPI        │
│ scheduling   │   │ analytics API  │
└──────────────┘   └────────────────┘
```

---

## 5. Data Model

Notebook에서 하나의 DataFrame으로 사용하던 데이터를 서비스 관점에서 세 가지 모델로 분리했습니다.

### `hr_employees`

직원의 비교적 안정적인 속성을 보관하는 dimension 역할입니다.

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

이직 여부를 분석 fact로 분리합니다.

```text
employee_id PK/FK -> hr_employees
attrited CHECK IN (0, 1)
```

### `hr_department_summary`

API에서 자주 조회하는 집계 결과를 미리 저장합니다.

```text
department PK
employee_count
average_income
attrition_rate
```

이 구조를 사용한 이유는 원본 DataFrame을 그대로 DB 한 테이블에 복사하는 것보다 **조회 목적과 무결성 경계를 명확하게 만들기 위해서**입니다.

---

## 6. Transactional Load Design

초기 구현에서는 `pandas.to_sql(if_exists="replace")` 방식도 고려할 수 있습니다. 하지만 `replace`는 기존 테이블을 재생성하기 때문에 PostgreSQL에 설정한 `CHECK`, `FOREIGN KEY`, `PRIMARY KEY` 같은 제약을 잃을 수 있습니다.

따라서 현재 구현은 schema를 먼저 bootstrap하고, 하나의 transaction 안에서 기존 데이터를 비운 뒤 append합니다.

```text
BEGIN
  DELETE attrition facts
  DELETE employees
  DELETE department summary

  INSERT employees
  INSERT attrition facts
  INSERT department summary
COMMIT
```

적재 도중 하나라도 실패하면 전체 transaction을 rollback할 수 있고, DB schema는 그대로 유지됩니다.

이 결정은 프로젝트에서 가장 중요한 개선 중 하나입니다.

> 데이터 파이프라인은 "데이터를 넣는 데 성공했는가"뿐 아니라 **무결성 규칙을 유지한 채 넣었는가**까지 확인해야 합니다.

---

## 7. Pipeline API

FastAPI는 분석 모델을 직접 학습시키는 역할이 아니라 **정제된 aggregate를 다른 시스템이 사용할 수 있게 제공하는 serving layer**입니다.

### Health

```http
GET /health
```

### Department summary

```http
GET /api/v1/departments
```

Response concept:

```json
[
  {
    "department": "Sales",
    "employee_count": 446,
    "average_income": 6959.17,
    "attrition_rate": 20.63
  }
]
```

### Department detail

```http
GET /api/v1/departments/{department}/attrition
```

API와 ETL을 분리한 이유는 **분석 생성 책임과 조회 책임의 실행 특성이 다르기 때문**입니다. ETL은 batch로 실행해도 되지만 API는 짧고 안정적인 응답 시간이 중요합니다.

---

## 8. Airflow Orchestration

`orchestration/dags/hr_pipeline_dag.py`에 파이프라인 DAG를 분리했습니다.

Airflow를 도입한 목적은 "Airflow를 써봤다"는 기술 나열이 아니라 다음 요구를 표현하기 위해서입니다.

```text
수동 Notebook 실행
      ↓
재실행 순서가 사람에게 의존
      ↓
정기 실행 / 실패 상태 / 재시도 필요
      ↓
Workflow Orchestrator
```

현재 프로젝트 규모에서는 단일 DAG로 충분합니다. 파이프라인이 복잡하지 않은데 Kafka나 분산 처리 엔진을 추가하지 않은 이유도 같은 원칙입니다.

---

## 9. Index Experiment

Data Engineering에서도 저장 이후의 조회 비용을 고려해야 합니다.

`scripts/explain_indexes.sql`은 조회 조건에 index를 적용하기 전과 후를 PostgreSQL `EXPLAIN ANALYZE`로 비교하기 위한 실험입니다.

검증 항목:

```text
Planning Time
Execution Time
Seq Scan / Index Scan
rows scanned
```

현재 저장소에서는 **실측하지 않은 개선 퍼센트를 README에 적지 않습니다.** 실제 PostgreSQL 환경에서 실행한 raw plan을 확보한 뒤에만 성능 수치를 추가하는 정책을 사용합니다.

---

## 10. Testing Strategy

테스트는 그래프 모양이 아니라 **파이프라인 계약**을 검증합니다.

### Data quality tests

- 정상 데이터가 validation을 통과하는가
- 중복 employee ID를 검출하는가
- 비정상 income을 검출하는가
- 잘못된 attrition domain을 검출하는가
- 필수 컬럼이 없을 때 즉시 실패하는가

### Transform tests

- employee dimension column mapping
- attrition `Yes/No → 1/0`
- department aggregate 생성

### CI

GitHub Actions에서 Python 3.11 기준으로 설치 후 다음 명령을 실행합니다.

```bash
python -m compileall -q src tests orchestration
pytest -q
```

현재 main의 CI가 성공하도록 유지합니다.

---

## 11. Why Not Other Technologies?

### Why PostgreSQL instead of a document database?

직원, attrition fact, department aggregate는 관계와 constraint가 분명합니다. flexible schema보다 FK/CHECK/transaction이 더 중요한 데이터이므로 PostgreSQL을 선택했습니다.

### Why Airflow instead of Kafka?

이 데이터는 지속적으로 발생하는 event stream이 아니라 주기적으로 적재하는 batch dataset입니다. Kafka는 E-commerce event 프로젝트에서 사용하는 것이 더 자연스럽고, 이 프로젝트에서는 orchestration 문제에 집중했습니다.

### Why FastAPI?

Python/Pandas transformation 코드와 같은 언어로 가벼운 serving API를 구성할 수 있고, 분석 결과 제공이라는 프로젝트 범위에서 충분합니다.

---

## 12. Failure Scenarios

### Case 1. Duplicate employee

```text
Raw input
EmployeeNumber=10
EmployeeNumber=10
      ↓
Quality Gate
      ↓
Pipeline FAIL
```

중복 데이터를 자동 삭제하지 않습니다. 어느 row가 맞는지 시스템이 임의로 판단할 수 없기 때문입니다.

### Case 2. DB load 중 실패

```text
employees inserted
attrition insert fails
      ↓
ROLLBACK
```

부분 성공 상태를 남기지 않는 것이 목표입니다.

### Case 3. API와 ETL 동시 실행

현재 프로젝트는 batch reload 동안 read consistency를 완전히 무중단으로 보장하는 blue/green table swap까지 구현하지 않았습니다. 데이터 규모가 커지고 무중단 refresh가 필요해지면 staging table → atomic rename/swap 방식이 다음 개선 후보입니다.

---

## 13. Observability and Operational Criteria

데이터 파이프라인에서 보고 싶은 운영 지표는 다음과 같습니다.

```text
pipeline_success_total
pipeline_failure_total
quality_rejected_rows
source_rows
loaded_rows
pipeline_duration
API p95 latency
```

현재 구현은 구조와 검증에 우선순위를 두고 있으며, production monitoring stack을 사용했다고 과장하지 않습니다.

---

## 14. Repository Structure

```text
.
├── WA_Fn-UseC_-HR-Employee-Attrition.csv
├── department.ipynb
├── strategy.ipynb
├── simul.ipynb
├── department_summary.csv
│
├── src/hr_pipeline/
│   ├── quality.py
│   ├── transform.py
│   ├── storage.py
│   ├── pipeline.py
│   └── api.py
│
├── orchestration/dags/
│   └── hr_pipeline_dag.py
│
├── scripts/
│   ├── run_pipeline.py
│   └── explain_indexes.sql
│
├── tests/
│   ├── test_quality.py
│   └── test_transform.py
│
├── docs/
│   ├── ARCHITECTURE_DECISIONS.md
│   ├── INTERVIEW_GUIDE.md
│   └── assets/department_attrition.svg
│
├── docker-compose.yml
├── pyproject.toml
└── .github/workflows/ci.yml
```

---

## 15. Run Locally

### Install

```bash
python -m venv .venv
source .venv/bin/activate     # macOS / Linux
# source .venv/Scripts/activate  # Git Bash / Windows
pip install -e '.[test]'
```

### PostgreSQL

```bash
docker compose up -d
```

### Pipeline

```bash
python scripts/run_pipeline.py
```

### API

```bash
uvicorn hr_pipeline.api:app --app-dir src --reload
```

### Test

```bash
pytest -q
```

---

## 16. What Changed from the Original Project?

```text
Before
Notebook
→ manual cleaning
→ CSV aggregate
→ presentation

After
Raw CSV
→ explicit quality contract
→ reusable transform package
→ constrained PostgreSQL schema
→ transactional load
→ Airflow orchestration
→ FastAPI serving
→ CI tests
```

이 변화가 이 프로젝트의 핵심 성과입니다.

---

## 17. What This Project Demonstrates

이 프로젝트는 Data Engineer 또는 Data Backend 관점에서 다음 경험을 설명하기 위한 프로젝트입니다.

- Notebook 분석을 재현 가능한 Python package로 전환
- 데이터 입력 계약과 quality gate 설계
- PostgreSQL constraint와 transaction을 이용한 무결성 보장
- batch orchestration과 API serving 책임 분리
- 분석 결과를 서비스에서 재사용 가능한 형태로 모델링
- 실측하지 않은 성능 수치를 작성하지 않는 검증 중심 개발 방식

---

## 18. Interview Topics

면접에서는 다음 질문을 코드와 함께 설명할 수 있도록 구성했습니다.

- 왜 `to_sql(replace)`를 사용하지 않았는가?
- 데이터 검증을 DB constraint만으로 처리하지 않은 이유는?
- Quality Gate에서 invalid row를 drop하지 않고 fail-fast한 이유는?
- Airflow와 Kafka의 역할 차이는?
- ETL transaction 범위는 어디까지 잡아야 하는가?
- aggregate table을 materialize한 이유는?
- index가 실제로 필요한지 어떻게 검증할 것인가?
- 대용량으로 확장되면 full reload를 어떻게 개선할 것인가?

상세 답변은 [`docs/INTERVIEW_GUIDE.md`](docs/INTERVIEW_GUIDE.md)에 정리했습니다.

---

## 19. Limitations and Next Decisions

현재 구현의 의도적인 한계는 다음과 같습니다.

- 1,470 row 규모이므로 분산 처리 엔진이 필요하지 않음
- 전체 reload 방식이며 CDC는 사용하지 않음
- Airflow deployment 자체의 production HA는 범위 밖
- API authentication은 구현하지 않음
- index 실험 수치는 실제 DB 환경에서 재측정 후 기록 예정

이 한계를 숨기지 않는 이유는 **기술을 많이 사용하는 것보다 문제 규모에 맞는 기술을 선택하는 것이 더 중요하기 때문**입니다.

---

## 20. Portfolio Position

이 프로젝트는 전체 포트폴리오에서 `Data Engineering / Data Backend` 역할을 담당합니다.

다른 프로젝트와의 역할을 분리했습니다.

```text
LLM Chat Platform   -> Async / RAG / Reliability
Loan Service        -> Transaction / Lock / Consistency
Commerce Events     -> Kafka / Event-driven / Idempotent Consumer
HR Data Pipeline    -> ETL / Data Quality / Airflow / PostgreSQL
Research            -> Experiment Design / Reproducibility
```

**핵심 메시지: 분석 결과를 만드는 것에서 끝나지 않고, 분석을 반복 가능하고 검증 가능한 데이터 시스템으로 바꿨습니다.**
