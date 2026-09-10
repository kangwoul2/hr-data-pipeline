from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

REQUIRED_COLUMNS = {
    "EmployeeNumber",
    "Department",
    "JobRole",
    "MonthlyIncome",
    "OverTime",
    "Attrition",
}


@dataclass(frozen=True)
class QualityReport:
    rows: int
    duplicate_employee_ids: int
    invalid_income_rows: int
    invalid_attrition_rows: int
    missing_required_values: int

    @property
    def passed(self) -> bool:
        return not any(
            [
                self.duplicate_employee_ids,
                self.invalid_income_rows,
                self.invalid_attrition_rows,
                self.missing_required_values,
            ]
        )


def validate_frame(df: pd.DataFrame) -> QualityReport:
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"missing required columns: {sorted(missing_columns)}")

    required = list(REQUIRED_COLUMNS)
    return QualityReport(
        rows=len(df),
        duplicate_employee_ids=int(df["EmployeeNumber"].duplicated().sum()),
        invalid_income_rows=int((df["MonthlyIncome"] < 0).sum()),
        invalid_attrition_rows=int((~df["Attrition"].isin(["Yes", "No"])).sum()),
        missing_required_values=int(df[required].isna().any(axis=1).sum()),
    )
