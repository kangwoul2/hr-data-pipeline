<div align="center">

# 👥 HR Attrition Analysis

### IBM HR 데이터를 활용한 부서별 이직 원인 분석과 인력 운영 시뮬레이션

![Python](https://img.shields.io/badge/Python-Data%20Analysis-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=flat-square&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=flat-square)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)

**Role · 한영서 — Sales 부서 이직률 분석 · 추가 고용 전략 시뮬레이션 · 발표 자료 제작**

</div>

---

## 1. Project Overview

IBM HR Analytics 데이터셋을 활용해 직원의 **부서, 직무, 급여, 초과근무, 경력 등과 이직 여부의 관계**를 분석한 프로젝트입니다.

단순히 “어떤 변수가 이직과 상관이 있는가”에서 끝내지 않고 다음 단계까지 연결하는 것을 목표로 했습니다.

```text
이직 패턴 발견
      ↓
원인 후보 비교
      ↓
개입 가능한 변수 선정
      ↓
인력 운영 전략 설계
      ↓
시뮬레이션
```

제가 담당한 핵심 질문은 다음과 같았습니다.

> **Sales 조직의 높은 이직률을 줄이기 위해 추가 채용과 업무부담 완화가 어떤 전략적 의미를 가질 수 있을까?**

---

## 2. Dataset

**IBM HR Analytics Employee Attrition & Performance**

- 1,470 employees
- 35 variables
- 주요 변수
  - `Department`
  - `JobRole`
  - `MonthlyIncome`
  - `OverTime`
  - `JobSatisfaction`
  - `TotalWorkingYears`
  - `YearsAtCompany`
  - `Attrition`

분석 전에 모든 값이 동일해 정보량이 없는 변수 등을 제거하고, 기존 변수로부터 추가 분석용 파생 변수를 구성했습니다.

---

## 3. My Contribution

### 3.1 Sales 조직 이직률 분석

부서별 인원과 이직 비율을 비교한 뒤 Sales 부서 내 직무 단위로 범위를 좁혔습니다.

```text
Company
  │
  ├── Sales
  │     ├── Sales Executive
  │     └── Sales Representative
  │
  └── Research & Development
```

단순 부서 평균만 비교하지 않고 직무별 급여와 초과근무 등 **실제 조직 운영에서 개입 가능한 변수**를 중심으로 분석했습니다.

### 3.2 추가 채용 전략 시뮬레이션

분석 결과를 바탕으로 단순히 “야근을 줄여야 한다”는 결론 대신, **추가 인력 투입을 가정한 시나리오를 구성하여 이직률 감소 전략을 검토**했습니다.

이 과정에서 분석을 다음처럼 연결했습니다.

```text
Attrition
   ↑
Workload / Overtime
   ↑
Staffing Level
   ↓
Hiring Scenario
```

### 3.3 결과 정리 및 발표

팀 전체 분석 중 제 담당 결과를 시각화하고 발표 자료로 구성했습니다. 분석 결과를 기술적 결과가 아니라 조직 의사결정 관점으로 설명하는 역할을 맡았습니다.

---

## 4. Analysis Pipeline

```text
Raw CSV
  │
  ▼
Data Cleaning
  │
  ├── constant columns 제거
  └── category / derived variables 생성
  │
  ▼
Department Analysis
  │
  ▼
JobRole Analysis
  │
  ▼
Workload / Salary Comparison
  │
  ▼
Hiring Scenario Simulation
  │
  ▼
Business Recommendation
```

---

## 5. Repository Structure

```text
.
├── WA_Fn-UseC_-HR-Employee-Attrition.csv
├── department.ipynb
├── strategy.ipynb
├── simul.ipynb
├── first.ipynb
├── a.ipynb
│
├── department_summary.csv
├── department_means.csv
├── department_jobrole_salary_summary.csv
├── department_jobrole_workload_summary.csv
├── jobrole_workload_summary.csv
└── dept_attrition_significant_vars.csv
```

분석 Notebook과 중간 집계 결과 CSV를 함께 남겨 **분석 과정과 결과를 다시 확인할 수 있도록** 구성했습니다.

---

## 6. Technical Skills Used

### Python

- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook

### Analysis

- 데이터 정제
- 그룹별 집계
- 파생 변수 생성
- 부서 / 직무별 비교
- 시나리오 기반 시뮬레이션
- 결과 시각화

---

## 7. Engineering Takeaways

이 프로젝트에서 얻은 경험은 이후 백엔드 개발에서도 이어졌습니다.

### 7.1 평균값 하나로 전체 시스템을 설명할 수 없다

부서 평균만으로 판단하면 실제 문제가 발생하는 특정 `JobRole`을 놓칠 수 있습니다. 백엔드 성능 분석에서도 평균 latency만 보는 대신 `p95 / p99`, endpoint별 latency를 나눠 봐야 한다는 사고와 연결됩니다.

### 7.2 분석 가능한 데이터 구조가 중요하다

원본 데이터를 그대로 사용하는 것보다 질문에 맞는 derived dataset을 만드는 과정이 중요했습니다. 이후 DB schema나 API response를 설계할 때도 **사용자가 어떤 방식으로 데이터를 읽고 사용할지**를 먼저 생각하는 습관으로 이어졌습니다.

### 7.3 가설은 수치로 검증해야 한다

```text
Observation
→ Hypothesis
→ Data
→ Comparison
→ Decision
```

이라는 흐름을 경험했고, 현재 백엔드 프로젝트에서는 이를 다음처럼 발전시키고 있습니다.

```text
Performance Problem
→ Hypothesis
→ Baseline
→ Optimization
→ Load Test
→ Before / After
```

---

## 8. What this project demonstrates

- 데이터에서 문제를 정의하고 분석 단위를 좁혀가는 능력
- Python으로 데이터를 가공하고 재현 가능한 결과를 만드는 과정
- 결과를 단순 통계가 아닌 **실행 가능한 전략**으로 연결하는 사고
- 팀 분석 결과 안에서 자신의 분석 범위를 책임지고 설명하는 경험

---

<div align="center">

**From analysis to an actionable hypothesis.**

</div>
