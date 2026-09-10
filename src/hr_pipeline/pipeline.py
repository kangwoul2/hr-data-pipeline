from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from hr_pipeline.quality import validate_frame
from hr_pipeline.storage import bootstrap_schema, build_engine
from hr_pipeline.transform import build_attrition_fact, build_department_summary, build_employee_dimension


def run_pipeline(source: str | Path, database_url: str) -> dict:
    df = pd.read_csv(source)
    report = validate_frame(df)
    if not report.passed:
        raise ValueError(f"data quality failed: {asdict(report)}")

    employees = build_employee_dimension(df)
    attrition = build_attrition_fact(df)
    departments = build_department_summary(df)

    engine = build_engine(database_url)
    bootstrap_schema(engine)
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM hr_attrition_facts"))
        connection.execute(text("DELETE FROM hr_employees"))
        connection.execute(text("DELETE FROM hr_department_summary"))
        employees.to_sql("hr_employees", connection, if_exists="append", index=False)
        attrition.to_sql("hr_attrition_facts", connection, if_exists="append", index=False)
        departments.to_sql("hr_department_summary", connection, if_exists="append", index=False)

    return {
        "quality": asdict(report),
        "employees": len(employees),
        "departments": len(departments),
    }
