from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="hr_daily_pipeline",
    schedule="0 7 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["portfolio", "hr"],
)
def hr_daily_pipeline():
    @task
    def quality_gate() -> str:
        return "validate required columns, nulls, duplicates and domain constraints"

    @task
    def transform(_: str) -> str:
        return "build employee dimension, attrition fact and department aggregate"

    @task
    def load(_: str) -> str:
        return "load validated tables into PostgreSQL"

    load(transform(quality_gate()))


hr_daily_pipeline()
