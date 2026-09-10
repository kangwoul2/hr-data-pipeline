# HR Data Pipeline Interview Guide

이 문서는 기술 이름을 외우기 위한 문서가 아니라, 프로젝트를 **문제 → 대안 → 선택 → trade-off → 검증** 순서로 설명하기 위한 면접 대비 자료입니다.

## 1. 왜 Notebook 분석을 별도 Python package로 옮겼나요?

Notebook은 탐색과 시각화에는 좋지만 실행 순서와 상태가 사람에게 의존하기 쉽습니다. 동일한 입력에서 동일한 결과를 반복해서 만들어야 하는 파이프라인에서는 명시적인 함수와 모듈 경계가 더 적합합니다. 그래서 원본 Notebook은 탐색 증거로 보존하고, 운영 가능한 경로는 `quality → transform → storage → api`로 분리했습니다.

## 2. 왜 잘못된 row를 drop하지 않고 pipeline을 실패시키나요?

중복 employee ID나 비정상 attrition 값은 어느 row가 정답인지 시스템이 임의로 판단할 수 없습니다. 잘못된 row를 조용히 제거하면 데이터는 줄었지만 pipeline은 성공한 것처럼 보일 수 있습니다. 따라서 현재 범위에서는 fail-fast가 더 안전합니다. 실제 운영에서는 quarantine table을 추가해 reject된 row를 별도로 보관할 수 있습니다.

## 3. DB constraint가 있는데 애플리케이션 Data Quality Gate가 왜 필요한가요?

둘의 책임이 다릅니다. 애플리케이션 검증은 입력 전체를 적재 전에 빠르게 검사하고 오류 원인을 설명하기 좋습니다. DB constraint는 어떤 적재 경로가 들어오더라도 마지막 무결성 경계가 됩니다. 따라서 quality gate와 constraint를 중복이 아니라 서로 다른 방어선으로 사용합니다.

## 4. 왜 `to_sql(if_exists="replace")`를 사용하지 않았나요?

`replace`는 테이블을 삭제하고 다시 만들 수 있어 미리 정의한 PK, FK, CHECK constraint를 잃을 수 있습니다. 그래서 schema는 유지하고 transaction 안에서 기존 데이터를 비운 뒤 append합니다. 적재 중 실패하면 rollback되어 부분 적재 상태도 줄일 수 있습니다.

## 5. 왜 PostgreSQL을 선택했나요?

employee, attrition fact, department aggregate는 관계가 명확하고 integrity constraint가 중요합니다. flexible schema보다 FK, CHECK, transaction이 더 큰 가치가 있어 RDB가 적합합니다.

## 6. 왜 Airflow를 쓰고 Kafka를 쓰지 않았나요?

이 프로젝트의 입력은 지속적인 event stream이 아니라 batch CSV입니다. 핵심 문제는 이벤트 전달이 아니라 `언제, 어떤 순서로, 실패 시 어떻게 다시 실행할 것인가`이므로 scheduler/orchestrator가 더 자연스럽습니다. Kafka는 Commerce Events 프로젝트에서 event-driven 문제에 사용합니다.

## 7. ETL transaction 범위는 어떻게 잡았나요?

외부 파일 읽기와 transformation 전체를 DB transaction 안에 넣지 않습니다. DB mutation 구간만 transaction으로 묶습니다. 네트워크나 CPU 작업이 긴 구간까지 transaction을 유지하면 connection과 lock을 불필요하게 오래 점유할 수 있기 때문입니다.

## 8. 왜 aggregate table을 미리 저장하나요?

API의 주 조회가 부서별 집계이고 원본 fact를 매번 계산할 필요가 없다면 materialized aggregate가 단순하고 빠릅니다. 데이터 변경 주기가 batch 단위라 refresh 시점도 명확합니다. 실시간성이 요구되면 전략이 달라질 수 있습니다.

## 9. Index는 어떻게 판단하나요?

"조회가 있으니 index를 만든다"가 아니라 실제 query pattern을 기준으로 `EXPLAIN ANALYZE`를 비교합니다. Seq Scan/Index Scan, execution time, rows scanned를 보고 index의 이익과 write overhead를 함께 판단합니다.

## 10. 데이터가 1억 건이면 어떻게 바꾸겠나요?

현재 구조를 그대로 scale-up하지 않습니다. 우선 full reload를 incremental load로 바꾸고, source partitioning과 staging table을 검토합니다. transformation이 단일 머신 메모리를 넘는 경우에만 Spark 같은 분산 처리 엔진을 검토합니다. 먼저 데이터 크기와 SLA를 측정하고 기술을 선택합니다.

## 11. 무중단 refresh가 필요하면요?

현재는 단일 transaction full reload입니다. 대용량에서는 staging table에 새 데이터를 완성한 뒤 view/table swap 또는 versioned snapshot 방식으로 reader가 부분 상태를 보지 않게 하는 전략을 검토합니다.

## 12. 이 프로젝트에서 가장 중요한 개선은 무엇인가요?

분석 알고리즘 추가보다 **데이터 계약을 코드로 명시한 것**입니다. 입력이 잘못되면 pipeline이 실패하고, DB constraint가 유지되며, 동일 transformation을 CI에서 검증할 수 있게 만든 것이 핵심입니다.

## 30-second answer

> IBM HR 데이터를 처음에는 Notebook으로 분석했지만, 동일 결과를 반복 생성하기 어렵고 입력 품질을 자동으로 보장하지 못한다는 문제가 있었습니다. 그래서 required schema, duplicate ID, invalid domain을 검증하는 quality gate를 만들고, employee/fact/aggregate 모델로 변환해 PostgreSQL에 transaction으로 적재했습니다. `to_sql(replace)`가 DB constraint를 제거할 수 있다는 문제도 발견해 schema를 유지한 append 방식으로 수정했습니다. 이후 Airflow로 batch 실행 책임을 분리하고 FastAPI로 집계 결과를 제공했습니다. 이 프로젝트에서는 Kafka 같은 기술을 억지로 넣기보다 batch 데이터의 재현성과 무결성에 집중했습니다.
