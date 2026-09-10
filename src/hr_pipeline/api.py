from __future__ import annotations

import os

from fastapi import FastAPI
from sqlalchemy import text

from hr_pipeline.storage import build_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://hr:hr@localhost:5434/hr_pipeline")
engine = build_engine(DATABASE_URL)
app = FastAPI(title="HR Pipeline API", version="0.2.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/departments")
def departments():
    query = text("""
        SELECT department, employee_count, average_income, attrition_rate
        FROM hr_department_summary
        ORDER BY attrition_rate DESC
    """)
    with engine.connect() as connection:
        return [dict(row._mapping) for row in connection.execute(query)]


@app.get("/api/v1/departments/{department}/attrition")
def department_attrition(department: str):
    query = text("""
        SELECT department, employee_count, average_income, attrition_rate
        FROM hr_department_summary
        WHERE department = :department
    """)
    with engine.connect() as connection:
        row = connection.execute(query, {"department": department}).first()
        return dict(row._mapping) if row else {"department": department, "found": False}
