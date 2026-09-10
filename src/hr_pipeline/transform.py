from __future__ import annotations

import pandas as pd


def build_employee_dimension(df: pd.DataFrame) -> pd.DataFrame:
    return df[[
        "EmployeeNumber",
        "Department",
        "JobRole",
        "MonthlyIncome",
        "OverTime",
        "TotalWorkingYears",
        "YearsAtCompany",
    ]].rename(columns={
        "EmployeeNumber": "employee_id",
        "Department": "department",
        "JobRole": "job_role",
        "MonthlyIncome": "monthly_income",
        "OverTime": "overtime",
        "TotalWorkingYears": "total_working_years",
        "YearsAtCompany": "years_at_company",
    })


def build_attrition_fact(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "employee_id": df["EmployeeNumber"],
        "attrited": (df["Attrition"] == "Yes").astype(int),
    })


def build_department_summary(df: pd.DataFrame) -> pd.DataFrame:
    working = df.assign(attrited=(df["Attrition"] == "Yes").astype(int))
    summary = (
        working.groupby("Department", as_index=False)
        .agg(
            employee_count=("EmployeeNumber", "count"),
            average_income=("MonthlyIncome", "mean"),
            attrition_rate=("attrited", "mean"),
        )
        .rename(columns={"Department": "department"})
    )
    summary["attrition_rate"] = summary["attrition_rate"] * 100
    return summary
