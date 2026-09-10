from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def build_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True)


def bootstrap_schema(engine: Engine) -> None:
    ddl = """
    CREATE TABLE IF NOT EXISTS hr_employees (
        employee_id INTEGER PRIMARY KEY,
        department VARCHAR(80) NOT NULL,
        job_role VARCHAR(120) NOT NULL,
        monthly_income INTEGER NOT NULL CHECK (monthly_income >= 0),
        overtime VARCHAR(3) NOT NULL,
        total_working_years INTEGER,
        years_at_company INTEGER
    );
    CREATE TABLE IF NOT EXISTS hr_attrition_facts (
        employee_id INTEGER PRIMARY KEY REFERENCES hr_employees(employee_id),
        attrited SMALLINT NOT NULL CHECK (attrited IN (0, 1))
    );
    CREATE TABLE IF NOT EXISTS hr_department_summary (
        department VARCHAR(80) PRIMARY KEY,
        employee_count INTEGER NOT NULL,
        average_income NUMERIC NOT NULL,
        attrition_rate NUMERIC NOT NULL
    );
    """
    with engine.begin() as connection:
        for statement in [item.strip() for item in ddl.split(";") if item.strip()]:
            connection.execute(text(statement))
