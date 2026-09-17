# README와 구현의 검증 기록

검증일은 **2026-09-17**이며, 대상 코드는 `2d793bbea1a08273b63f33a140ce1f09b3a73a3d`입니다. 검증 시 GitHub의 HEAD와 로컬 커밋이 일치했습니다. 이 문서와 README의 수정은 해당 코드의 동작을 설명하며, 발견한 구현 공백을 수정한 것으로 간주하지 않습니다.

## 1. 검증 결론

**핵심 ETL과 API는 실제 PostgreSQL에서 동작했지만, 기존 README가 암시하던 Airflow 연동과 자동 테스트 범위는 구현보다 넓었습니다.** 설명을 실제 구현 범위에 맞추고, 확인된 성과와 남은 과제를 구분했습니다.

| 구분 | 결과 | 근거 |
|---|---|---|
| 기존 단위 테스트 | 통과했습니다. | `pytest -q`: **4 passed**입니다. |
| Python 문법 | 통과했습니다. | `compileall`로 `src`, `tests`, `orchestration`, `scripts`를 검사했습니다. |
| 원본·집계 정합성 | 일치했습니다. | 원본 재집계와 `department_summary.csv`의 인원·평균 급여·이직률을 대조했습니다. |
| PostgreSQL 적재 | 통과했습니다. | 직원 1,470행, 이직 정보 1,470행, 부서 집계 3행을 확인했습니다. |
| 동일 입력 재실행 | 통과했습니다. | 두 차례 적재 후 세 테이블을 키 순서로 조회하여 전체 내용이 같은지 비교했습니다. |
| 실패 시 롤백 | 통과했습니다. | 이직 값 `2`를 주입해 CHECK 위반을 발생시키고 기존 세 테이블의 전체 내용이 보존되는지 비교했습니다. |
| HTTP API | 통과했습니다. | 상태, 전체 부서, Sales 부서, 없는 부서의 응답을 검사했습니다. |
| Airflow 실제 ETL | 구현되지 않았습니다. | 세 태스크 모두 설명 문자열을 반환하며 실제 처리 함수를 호출하지 않습니다. |
| 인덱스 성능 | 측정하지 않았습니다. | 비교용 SQL은 존재하지만 개선율의 근거로 사용할 측정 결과는 없습니다. |
| 노트북 전체 재실행 | 수행하지 않았습니다. | 셀 소스와 저장된 출력·산출물을 검토했습니다. 모델 적합 결과 전체를 재검증한 것은 아닙니다. |

## 2. 검증 환경과 범위

기존 환경에 영향을 주지 않도록 별도 Python 가상환경과 검증 전용 PostgreSQL 컨테이너를 사용했습니다. 검증 후 임시 API 프로세스와 컨테이너를 종료했습니다.

| 항목 | 실제 확인한 환경 |
|---|---|
| Python | Windows / 3.11.9입니다. |
| pandas / SQLAlchemy | 2.3.3 / 2.0.54입니다. |
| psycopg / pytest | 3.3.5 / 8.4.2입니다. |
| FastAPI / Uvicorn | 0.141.1 / 0.53.0입니다. |
| PostgreSQL | Docker의 `postgres:17-alpine`, 실제 서버 버전 17.11입니다. |
| DB 격리 | 이 검증을 위해 생성한 `hr_review` 데이터베이스만 사용했습니다. |
| API 호출 | Uvicorn을 로컬에서 실행하고 실제 HTTP 요청을 보냈습니다. |

위 버전은 이번 실행의 환경 기록입니다. `pyproject.toml`이 모든 패키지의 정확한 버전을 고정한 것은 아니므로 이후 설치 결과는 달라질 수 있습니다.

**기존 CI가 자동으로 수행하는 것은 단위 테스트 4개와 문법 검사입니다.** DB·API 검증은 이번 검토에서 임시 검증 스크립트로 수행했으며 저장소의 자동 테스트를 추가한 것은 아닙니다. 아래에 핵심 재현 절차를 남깁니다.

## 3. 데이터와 집계 확인

원본 크기는 1,470행·35열이며, 직원 ID 중복·음수 급여·잘못된 이직 값·필수값 누락은 각각 0건이었습니다. 이직 여부가 `Yes`인 행은 237개로, 전체 비율은 약 16.12%입니다.

| 부서 | 직원 수 | 이직자 수 | 평균 MonthlyIncome | 이직률 |
|---|---:|---:|---:|---:|
| Sales | 446 | 92 | 6,959.17 | 20.63% |
| Human Resources | 63 | 12 | 6,654.51 | 19.05% |
| Research & Development | 961 | 133 | 6,281.25 | 13.84% |

급여는 원본 `MonthlyIncome` 값의 평균이며 별도의 환산을 하지 않았습니다. 이직률은 해당 부서 직원 수를 분모로 계산했습니다. 부서별 이직률을 단순 평균하여 전체 이직률로 사용하지 않았습니다.

## 4. 실패를 주입해 확인한 동작

중복 직원 ID, 음수 급여, `Attrition=Unknown`, `Department=NULL`을 원본 복사본에 각각 주입했습니다. 각 사례에서 품질 검사가 실패했으며, `pipeline.build_engine`이 호출되기 전에 `run_pipeline()`이 예외로 종료되는지 확인했습니다.

롤백 검증에서는 먼저 정상 데이터를 적재한 뒤, `build_attrition_fact()`의 결과 중 한 행만 `attrited=2`로 바꾸었습니다. 직원 테이블의 삽입 이후 이직 테이블의 CHECK 제약조건에서 `IntegrityError`가 발생했습니다. 그 뒤 세 테이블 전체를 다시 읽어 오류 주입 전 내용과 동일한 것을 확인했습니다. 제약조건 메타데이터에서도 기본키 3개, 외래키 1개, CHECK 2개가 유지되는 것을 확인했습니다. 이 검증으로 모든 제약조건의 모든 위반 사례를 시험했다고 해석하지는 않습니다.

| API 요청 | 확인한 응답 |
|---|---|
| `GET /health` | HTTP 200, `{"status": "ok"}`입니다. |
| `GET /api/v1/departments` | HTTP 200, Sales → Human Resources → Research & Development 순서의 3개 부서이며 직원 수 합계는 1,470명입니다. |
| `GET /api/v1/departments/Sales/attrition` | HTTP 200, 직원 수 446명이며 이직률은 `92 / 446 × 100`과 일치했습니다. |
| `GET /api/v1/departments/Unknown/attrition` | HTTP 200, `{"department": "Unknown", "found": false}`입니다. |

## 5. 발견한 공백과 우선순위

### 먼저 보완해야 할 입력 계약

- **빈 입력:** 원본과 같은 열을 가진 0행 DataFrame이 `validate_frame()`을 통과했습니다. 적재 코드가 전체 삭제 후 삽입하는 구조이므로 빈 파일로 기존 데이터가 비워질 가능성이 있습니다. 이번 검증에서는 빈 입력의 품질 검사 통과까지 확인했으며 실제 빈 입력 적재는 수행하지 않았습니다.
- **필수 열 불일치:** `TotalWorkingYears` 또는 `YearsAtCompany`를 제거해도 품질 검사는 통과했지만 `build_employee_dimension()`에서 `KeyError`가 발생했습니다. 현재 실행 순서에서는 DB 변경 전에 멈추지만, 입력 검사 단계에서 설명 가능한 오류로 거절하도록 보완할 필요가 있습니다.
- **자료형·값 범위:** 숫자가 아닌 급여에 대한 명시적인 검증, 공백 문자열, `OverTime` 값 범위, 근속연수 관계 등은 현재 계약에 없습니다. 이 부분은 코드 검토로 확인했으며 모든 변형 입력을 실행해 검사하지는 않았습니다.

### 실행 자동화와 서비스 준비 상태

- **Airflow:** DAG의 의존 관계와 일정만 정의되어 있습니다. 실제 ETL 연결, 입력 파일 배치, DB 연결 설정, 타임존, 재시도, 동시 실행 정책을 추가해야 합니다.
- **자동 테스트:** 현재 `tests/`에는 음수 급여·NULL·잘못된 이직 값, 직원 차원과 이직 사실 변환, 롤백·API 테스트가 없습니다. 이번 수동 통합 검증과 CI의 보장 범위를 구분해야 합니다.
- **상태 확인:** `/health`는 DB 연결을 검사하지 않습니다. DB가 사용 가능한지 확인하는 준비 상태 경로가 추가로 필요합니다.
- **환경 설정:** CLI는 `--database-url`, API는 `DATABASE_URL`을 사용합니다. 서로 다른 DB를 바라보지 않도록 실행 절차에 명시해야 합니다.
- **동시성·운영:** 복수 배치 동시 실행, 갱신 도중 API 조회, 장애 재시도, 백업 복원, 부하와 지연시간은 검증하지 않았습니다.

### 분석 기록의 재현성과 해석

- `first.ipynb`의 마지막 셀에는 저장된 `NameError: name 'df' is not defined`가 있습니다. 이는 저장된 실행 기록의 문제이며, 이번 검토에서 노트북을 다시 실행해 같은 오류를 재현했다는 의미는 아닙니다.
- `first.ipynb`의 로지스틱 회귀 설명에서 `exp(계수)`를 확률 배수로 표현한 부분은 오즈비로 해석해야 합니다. p값이 크다는 사실만으로 영향이 없다고 단정할 수도 없습니다.
- `strategy.ipynb`는 이미 집계된 이직률을 단순 평균하는 부분이 있습니다. 전체 직원 기준의 비율과 혼동하지 않도록 분모와 가중치를 명시해야 합니다.
- `department.ipynb`에는 같은 파일명을 여러 열 구성으로 덮어쓰는 셀이 있습니다. 저장된 산출물만으로 모든 셀의 실행 순서가 재현 가능하다고 판단하지 않았습니다.
- 업무량 CSV 2개의 최초 생성 코드는 저장소의 Python 파일과 노트북 셀에서 확인되지 않았습니다. 추가 인원·비용 지표는 생성 코드와 가정이 보완되기 전까지 실측 성과로 제시하지 않습니다.
- `simul.ipynb`의 교체율 38%와 17%는 시뮬레이션 입력 조건이며 실제 개선 성과가 아닙니다.

## 6. 핵심 검증을 재현하는 방법

저장소 루트에서 프로젝트의 테스트 의존성을 설치한 가상환경을 사용합니다.

```bash
pip install -e '.[test]'
python -m compileall -q src tests orchestration scripts
python -m pytest -q
```

원본 집계와 저장된 분석 CSV의 일치 여부는 다음 Python 코드로 재확인할 수 있습니다.

```python
import pandas as pd
from hr_pipeline.quality import validate_frame
from hr_pipeline.transform import build_department_summary

source = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")
assert source.shape == (1470, 35)
assert validate_frame(source).passed
assert (source["Attrition"] == "Yes").sum() == 237
actual = build_department_summary(source).sort_values("department").reset_index(drop=True)
saved = pd.read_csv("department_summary.csv").rename(columns={
    "Department": "department", "인원수": "employee_count",
    "평균월급": "average_income", "이직률": "attrition_rate",
})
expected = saved[actual.columns].sort_values("department").reset_index(drop=True)
pd.testing.assert_frame_equal(actual, expected)
```

재적재·롤백 검증에는 **비어 있는 검증 전용 PostgreSQL DB**를 준비하고 그 URL을 `HR_REVIEW_DATABASE_URL`에 지정합니다. 아래 코드는 해당 DB의 프로젝트 테이블을 전체 재적재하므로 서비스 DB에 실행하지 않습니다.

```python
import os
from unittest.mock import patch
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from hr_pipeline.pipeline import run_pipeline
from hr_pipeline.storage import build_engine
from hr_pipeline.transform import build_attrition_fact

url = os.environ["HR_REVIEW_DATABASE_URL"]
source = "WA_Fn-UseC_-HR-Employee-Attrition.csv"
engine = build_engine(url)
tables = ("hr_employees", "hr_attrition_facts", "hr_department_summary")

def snapshot():
    with engine.connect() as connection:
        return {
            table: [tuple(row) for row in connection.execute(
                text(f"SELECT * FROM {table} ORDER BY 1")
            )]
            for table in tables
        }

run_pipeline(source, url)
before = snapshot()
assert [len(before[table]) for table in tables] == [1470, 1470, 3]
run_pipeline(source, url)
assert snapshot() == before

def invalid_fact(frame):
    result = build_attrition_fact(frame)
    result.loc[0, "attrited"] = 2
    return result

with patch("hr_pipeline.pipeline.build_attrition_fact", side_effect=invalid_fact):
    try:
        run_pipeline(source, url)
    except IntegrityError:
        pass
    else:
        raise AssertionError("CHECK 위반으로 적재가 실패해야 합니다.")

assert snapshot() == before
engine.dispose()
print("재적재 결과 일치 및 롤백을 확인했습니다.")
```

API 검증은 `DATABASE_URL`을 같은 검증 DB로 지정하고 `uvicorn hr_pipeline.api:app --app-dir src`를 실행한 뒤 위 표의 네 경로를 요청하여 확인합니다. 이 절차는 기능 확인이며 성능 측정 절차는 아닙니다.
