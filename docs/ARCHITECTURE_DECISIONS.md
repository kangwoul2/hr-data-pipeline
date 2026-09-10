# Architecture Decisions

이 문서는 HR Data Pipeline의 기술 선택을 `문제 → 대안 → 선택 → trade-off` 순서로 기록합니다.

## ADR-001. Notebook을 버리지 않고 Pipeline을 별도 계층으로 추가

### Context

기존 프로젝트는 탐색적 분석에 적합한 Jupyter Notebook 중심이었습니다. Notebook은 가설을 빠르게 검증하는 데 좋지만, 운영 데이터 파이프라인의 실행 단위로 사용하면 다음 문제가 생깁니다.

- 실행 순서가 cell state에 의존할 수 있음
- 입력/출력 경계가 불명확함
- 테스트와 재사용이 어려움
- scheduler에서 재실행하기 어려움

### Decision

기존 Notebook은 분석 근거로 보존하고, 재현 가능한 로직은 `src/hr_pipeline/` Python package로 분리합니다.

```text
Exploration → Notebook
Reusable processing → Python package
Scheduling → Airflow
Serving → FastAPI
```

기존 작업의 근거를 지우지 않으면서 시스템화 과정을 보여주기 위한 선택입니다.

---

## ADR-002. Load 전에 Data Quality Gate 실행

### Context

잘못된 row가 DB까지 적재된 뒤 탐지되면 downstream aggregate와 API 결과까지 오염됩니다.

### Decision

적재 전에 다음을 검증합니다.

- required columns
- required value null
- duplicate employee ID
- negative monthly income
- invalid Attrition domain

검증 실패 시 load를 시작하지 않습니다.

### Trade-off

엄격한 fail-fast 정책은 일부 정상 row도 함께 적재하지 못하게 만들 수 있습니다. 실제 대규모 파이프라인에서는 quarantine table / partial acceptance가 필요할 수 있지만, 현재 batch snapshot은 **전체 snapshot이 일관되게 유효한가**를 우선합니다.

---

## ADR-003. `to_sql(replace)`를 사용하지 않음

### Context

초기 V2 구현에서 `DataFrame.to_sql(..., if_exists="replace")`를 사용할 수 있었지만, 이 방식은 기존 테이블을 drop/create할 수 있어 DB에서 선언한 PK/FK/CHECK constraint를 잃을 수 있습니다.

### Decision

schema는 `bootstrap_schema()`가 관리하고, reload는 하나의 transaction에서:

```text
DELETE old facts
DELETE old dimension
DELETE old aggregate
APPEND new dimension
APPEND new facts
APPEND new aggregate
COMMIT
```

순서로 수행합니다.

### Why this matters

애플리케이션 코드가 데이터 품질을 검사하더라도 DB constraint는 마지막 무결성 경계입니다. Reload 구현 때문에 그 경계를 제거하면 설계 의도와 코드가 충돌합니다.

---

## ADR-004. Snapshot reload를 하나의 DB Transaction으로 묶음

### Context

employee dimension만 새 데이터로 바뀌고 attrition fact 적재가 실패하면 서로 다른 snapshot이 동시에 노출될 수 있습니다.

### Decision

삭제와 append를 `engine.begin()` transaction으로 묶습니다.

```text
old snapshot
     ↓
BEGIN
 delete + insert
COMMIT
     ↓
new snapshot
```

중간 단계가 정상 commit되지 않게 합니다.

### Limitation

데이터 규모가 매우 커지면 full reload가 lock/WAL/latency 측면에서 비효율적일 수 있습니다. 그 단계에서는 staging table + atomic swap, incremental load, CDC를 검토합니다.

---

## ADR-005. Raw row와 Aggregate를 분리

### Context

API가 매 요청마다 1,470개 employee row를 GROUP BY해도 현재 데이터에서는 충분히 빠를 수 있습니다. 하지만 사용 목적이 명확한 집계 결과라면 API query마다 계산을 반복할 이유가 없습니다.

### Decision

다음 세 구조로 분리합니다.

```text
hr_employees
→ employee dimension

hr_attrition_facts
→ attrition event/fact

hr_department_summary
→ serving aggregate
```

분석 row와 serving read model의 책임을 분리합니다.

---

## ADR-006. Airflow는 계산 엔진이 아니라 Orchestrator

Airflow DAG 안에 데이터 변환 로직을 길게 작성하지 않습니다.

DAG의 역할은:

```text
schedule
→ task lifecycle
→ dependency
→ retry / observation boundary
```

실제 transform/quality/load 로직은 Python package가 담당합니다. 이렇게 해야 scheduler 없이도 같은 pipeline을 CLI/test에서 실행할 수 있습니다.

---

## ADR-007. Index는 `EXPLAIN ANALYZE` 후 판단

인덱스를 컬럼마다 추가하지 않습니다.

인덱스의 장점:
- read scan 감소 가능

비용:
- storage
- insert/update overhead
- planner가 사용하지 않을 수 있음

따라서 `scripts/explain_indexes.sql`을 통해 query plan을 비교하고, 실제 조회 패턴에 필요한 index만 유지하는 방향을 사용합니다.

---

## ADR-008. 성능 수치는 측정 전 작성하지 않음

성능 실험은 다음 계약을 따릅니다.

```text
same data
same PostgreSQL version
same query
warmup
EXPLAIN (ANALYZE, BUFFERS)
index change
repeat
```

측정 전에는 `N% faster`와 같은 표현을 README에 기재하지 않습니다.
