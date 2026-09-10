import pandas as pd

from hr_pipeline.transform import build_department_summary


def test_department_summary_uses_percentage_points():
    df = pd.DataFrame({
        "EmployeeNumber": [1, 2, 3, 4],
        "Department": ["Sales"] * 4,
        "JobRole": ["A"] * 4,
        "MonthlyIncome": [100, 100, 100, 100],
        "OverTime": ["No"] * 4,
        "Attrition": ["Yes", "No", "No", "No"],
    })
    result = build_department_summary(df)
    assert result.iloc[0]["attrition_rate"] == 25.0
