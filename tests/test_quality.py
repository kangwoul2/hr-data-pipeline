import pandas as pd
import pytest

from hr_pipeline.quality import validate_frame


def base_frame():
    return pd.DataFrame({
        "EmployeeNumber": [1, 2],
        "Department": ["Sales", "Sales"],
        "JobRole": ["Executive", "Representative"],
        "MonthlyIncome": [5000, 3000],
        "OverTime": ["Yes", "No"],
        "Attrition": ["No", "Yes"],
        "TotalWorkingYears": [5, 2],
        "YearsAtCompany": [3, 1],
    })


def test_valid_frame_passes():
    report = validate_frame(base_frame())
    assert report.passed
    assert report.rows == 2


def test_duplicate_employee_fails_quality_gate():
    df = base_frame()
    df.loc[1, "EmployeeNumber"] = 1
    report = validate_frame(df)
    assert report.passed is False
    assert report.duplicate_employee_ids == 1


def test_missing_required_column_raises():
    df = base_frame().drop(columns=["Attrition"])
    with pytest.raises(ValueError):
        validate_frame(df)
