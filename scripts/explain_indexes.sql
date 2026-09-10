-- Baseline: inspect the plan before adding an index.
EXPLAIN (ANALYZE, BUFFERS)
SELECT e.job_role, AVG(e.monthly_income)
FROM hr_employees e
JOIN hr_attrition_facts a USING (employee_id)
WHERE e.department = 'Sales' AND a.attrited = 1
GROUP BY e.job_role;

-- Candidate index for a repeatedly filtered dimension.
CREATE INDEX IF NOT EXISTS idx_hr_employees_department_role
ON hr_employees(department, job_role);

EXPLAIN (ANALYZE, BUFFERS)
SELECT e.job_role, AVG(e.monthly_income)
FROM hr_employees e
JOIN hr_attrition_facts a USING (employee_id)
WHERE e.department = 'Sales' AND a.attrited = 1
GROUP BY e.job_role;
