# Python_Data_Analysis_HR_DATA
### 0️⃣ 팀 소개 및 구성원, 목차 소개

- 한영서: 직무별 이직률 감소를 위한 Sales 추가 고용 전략 및 시뮬, 발표자료 제작
- 이정화: 커리어단계별 학력수준 및 월급에 따른 이직여부 연관성 분석, 보고서 작성
- 임건우: 직무별 이직률 감소를 위한 Research & Development 부서 이직률 감소 전략 및 발표
- 조윤서: 커리어단계별 월급 및 고연차(Senior) 이직율 감소 전략, 발표자료 제작

  - 목차
    1. **활용 데이터 선정 및 수립**
        
        1.1. 프로젝트 목적
        
        1.2. 사용 데이터 소개 
        
        1.2.1. 활용 데이터 출처 
        
        1.2.2. 데이터 소개 
        
        1.2.3. 데이터 규모
        
        1.2.4. 주요 변수
        
        1.3. 분석 방법 및 도구
        
        1.3.1. 분석 도구
        
        1.3.2. 분석 접근 방식
        
        1.4. 데이터 전처리
        
        1.4.1. 전처리 대상 데이터 
        
        1.4.2. 추가 데이터 형성
        
    2. 개별 분석 주제
        
        2.0. 분석 목표
        
        2.1. 부서(Department)별 이직률 감소 전략
        
        2.1.1. Sales 부서 이직률 감소 전략
        
        2.1.2. Research & Development 부서 이직률 감소 전략
        
        2.2. 커리어단계(CareerStage)별 이직률 감소 전략
        
        2.2.1. 커리어단계별 학력수준과 이직여부의 연관성
        
        2.2.2. 커리어단계별 월급과 이직여부의 연관성
        
    
    3. 종합 결론 및 전략 제안
        
        3.1. 주요 공통 인사이트 요약
        
        3.2. 종합 인사 전략 제안


# 1️⃣ 활용 데이터 선정 및 수집

---

## 1.1. **프로젝트 목적**

본 프로젝트의 목표는 데이터 분석 플랫폼인 Kaggle의 데이터를 활용한 데이터 분석 및 시각화 작업을 직접 진행해보며 데이터 분석 일련의 과정을 경험하고 데이터 분석에서 자주 사용하는 Python 라이브러리에 대한 경험과 데이터 분석을 위한 프로그래밍 역량 강화한다. 구체적인 기술로는 Pandas, Matplotlib 등이 사용한다.

| **프로젝트 팀주제** | **세부 수행 내용**(과업) | **프로젝트 목적** | **습득 직무 역량** |
| --- | --- | --- | --- |
| Kaggle 데이터셋을 활용한 Python 데이터 분석 프로그래밍 | - Kaggle 데이터 수집
- Python 프로그래밍을 활용한 데이터 분석
- pandas, Matplotlib, Seaborn 패키지를 활용한 분석 시각화
- 프로젝트 결과 문서를 통해 데이터 분석 과정 및 시각화 결과 첨부 | Python 데이터 분석 패키지를 활용하여 데이터 분석을 진행한다 | Python Pandas, Matplotlib, Seaborn |

## 1.2. 사용 데이터 소개

### 1.2.1. 활용 데이터 출처 :

https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

### 1.2.2. 데이터 소개

본 프로젝트에선 Kaggle의 [IBM HR Analytics Employee Attrition & Performance] 을 활용하였다.

직원의 이직여부, 나이, 급여, 학력수준, 만족도 등의 변수를 포함하고 있는 IBM 데이터 과학자들이 만든 가상의 데이터 세트이다. 직원 이직을 유발하는 요인을 밝히기 위해 직무, 월급, 학력수준 등에 따른 이직률을 비교할 수 있다.

### 1.2.3. 데이터 규모

1. IBM의 HR 직원 이직 데이터: 35개의 변수, 1470개의 데이터를 포함하고 있다.

### 1.2.4. 주요 변수

- IBM의 HR 직원 이직 데이터

| **COLUMN** | **Type** | **Description** |
| --- | --- | --- |
| Age | int64 | 나이 |
| Attrition | object | 이직 여부 (Yes/No) |
| BusinessTravel | object | 출장 빈도 |
| DailyRate | int64 | 일일 급여 |
| Department | object | 소속 부서 |
| DistanceFromHome | int64 | 집과 회사 간 거리 |
| Education | int64 | 학력 수준 |
| EducationField | object | 전공 분야 |
| EmployeeCount | int64 | 직원 수 |
| EmployeeNumber | int64 | 직원 ID |
| EnvironmentSatisfaction | int64 | 업무환경 만족도  (1~4) |
| Gender | object | 성별 (Male/Female) |
| HourlyRate | int64 | 시급 |
| JobInvolvement | int64 | 업무 관여도 (1~4) |
| JobLevel | int64 | 직급 레벨 |
| JobRole | object | 직무 |
| JobSatisfaction | int64 | 직무 만족도 (1~4) |
| MaritalStatus | object | 결혼 여부 (Single, Married, Divorced) |
| MonthlyIncome | int64 | 월급 |
| MonthlyRate | int64 | 월급여율 |
| NumCompaniesWorked | int64 | 경력 중 근무한 회사 수 |
| Over18 | object | 18세 이상 여부 (모두 Y) |
| OverTime | object | 야근 여부 (Yes/No) |
| PercentSalaryHike | int64 | 전년 대비 급여 인상률 |
| PerformanceRating | int64 | 성과 등급 (3 또는 4) |
| RelationshipSatisfaction | int64 | 상사와의 관계 만족도 (1~4) |
| StandardHours | int64 | 표준 근무 시간 (모두 80) |
| StockOptionLevel | int64 | 스톡옵션 보유 수준 (0~3) |
| TotalWorkingYears | int64 | 총 경력 연수 |
| TrainingTimesLastYear | int64 | 작년 연간 교육 횟수 |
| WorkLifeBalance | int64 | 일과 삶의 균형 만족도 (1~4) |
| YearsAtCompany | int64 | 현 회사 근속 연수 |
| YearsInCurrentRole | int64 | 현재 직무 근무 연수 |
| YearsSinceLastPromotion | int64 | 마지막 승진 이후 경과 연수 |
| YearsWithCurrManager | int64 | 현재 상사와 근무한 연수 |

### **1.3. 분석 방법 및 도구**

**1.3.1. 분석 도구**:

- Excel(데이터 필터링)
- Python Pandas(시각화 및 수치 비교용 그래프 제작)

**1.3.2. 분석 접근 방식**:

- 데이터 특징을 바탕으로 가설을 수립하고 관련 증거 수집 후 결론 도출
- 의미없는 변수를 삭제하여 데이터 복잡도 감소
- Pandas와 Numpy 등을 통해 기초적인 데이터 분석 수행
- Matplotlib 패키지와 Seaborn 패키지를 이용해 데이터 시각화 수행

### 1.4. 데이터 전처리

1. 변수 삭제
- 무의미한 변수 제거: Over18 변수는 모든 값이 ‘Y’이고, StandardHours 변수는 모든 값이 ‘80’이므로 무의미한 변수이기 때문에 변수 제거
1. 변수 추가
- 커리어단계(CareerStage) 변수: JobLevel 변수와 TotalWorkingYears 변수를 활용하여 새로운 변수 생성

<aside>

- 데이터 생성 시 사용한 가설
    
    JovLevel 변수는 직원의 직무 능력을 나타내고 TotalWorking Years 변수는 직원의 경험 능력을 나타낸다.
    
</aside>

| 커리어단계 | 조건 |
| --- | --- |
| Intern | JobLevel = 1 OR TotalWorkingYears ≤ 1  |
| Junior | JobLevel = 2 OR TotalWorkingYears ≤ 4  |
| Mid-level | JobLevel = 3 OR TotalWorkingYears ≤ 9  |
| Senior | JobLevel = 4 OR TotalWorkingYears ≤ 15  |
| Expert | JobLevel = 5 OR TotalWorkingYears > 15  |


# 2️⃣ 개별 분석 주제

---

## **2. 분석 주제**

- 2.1. **부서(Department)별 이직률 감소 전략**
    - 2.1.1. Sales 부서 이직률 감소 전략
        
        전략
        
        <aside>
        
        - 추가적인 Sales 부서 인원 고용이나 직원 교육으로 야근을 줄이면 이직률 감소에 도움이 될 것이다.
        - 추가적인 월급으로 업무 만족도를 높인다면 이직률을 감소시킬 수 있을 것이다.
        </aside>
        
        ---
        
        **시각화와 분석 결과**
        
        1. Sales 총 인원 446명, Research & Development 인원 961명 
            
      <img width="630" height="408" alt="image" src="https://github.com/user-attachments/assets/f14e868e-8ddd-4779-9018-0f77d7f636f7" />

            
        
        <aside>
        
        - Research 부서의 사람수가 Sales 부서의 사람수보다 2.15배로 많지만 전체 직원중 이직 여부 비율은 9.0%와 6.3%로 크게 차이나지 않음.
        - Sales 에서 이직률이 높고, 그 비중이 전체 이직자 중에서도 꽤 큰 비율이다.
        - 따라서 Sales 부서에서 이직률을 낮추면 회사 전체에서 의미있는 비중으로 이직률을 감소시킬 수 있을 것이고, 연차가 쌓인 사람(뛰어난 역량을 가진 사람) 보유 확률이 증가할 것이다.
        </aside>
        
       <img width="651" height="460" alt="image" src="https://github.com/user-attachments/assets/b8afcec7-de94-4817-acb3-bbdeb7abbd26" />

        
        <aside>
        
        - 실제로 Sales 부서의 이직률이 가장 높고, Research & Development 부서보다 이직률이 높다.
        </aside>
        
       <img width="652" height="232" alt="image" src="https://github.com/user-attachments/assets/2c9c01ea-1e32-448f-8f9a-77d7e34a62dd" />

        
        Sales vs Research & Development 월급 비교
        
        <aside>
        
        1. 관리직
        
        Research 부서 : 
        
        Manufacturing Director 월급 = 7295$
        
        Research Director 월급 = 16033$
        
        Sales 부서 :
        
        Sales Executive 월급 = 6924$
        
        Sales 관리자의 평균 월급이 더 낮다.
        
        </aside>
        
        <aside>
        
        1. 일반직
        
        Research 부서 :
        
        Laboratory Technician 월급 = 3237$
        
        Sales 부서 :
        
        Sales Representative 월급 = 2626$
        
        평범한 사원들의 평균 월급도 Sales 부서가 더 낮음.
        
        </aside>
        
        <aside>
        
        생각 1.
        
        - Sales 부서 이직률을 감소시키면 전체 인원의 이직률 감소에 도움이 될 것이다.
        - Sales 부서 사람의 월급이 비교적 낮아 추가적인 고용에 있어서도 다른 전체 부서에 비해 덜 부담스럽다. (비용 대비 고용 인원 증대 효율 좋음)
        </aside>
        
       <img width="652" height="612" alt="image" src="https://github.com/user-attachments/assets/c2190742-192a-4985-b6ec-46687d2897b3" />

        
        <aside>
        
        다음과 같이 Sales 부서의 직책을 가진 사람이 이직률이 높은 것으로 관찰된다.
        
        </aside>
        
        초과근무 여부별 이직률
        
         <img width="651" height="444" alt="image" src="https://github.com/user-attachments/assets/753c2e6b-0fbc-4772-ba7b-411569f3391b" />

        
        <aside>
        
        초과 근무를 경험한(Yes) 사람의 이직률이 경험하지 않은(No)인 사람의 이직률보다 모든 부서에서의 이직률이 높다. 야근하는 직무나 부서에서 이직하는 사람이 많다.
        
        </aside>
        
        <img width="657" height="188" alt="image" src="https://github.com/user-attachments/assets/a2ddb287-5561-4397-9f15-786f796815f8" />

        
        <img width="651" height="825" alt="image" src="https://github.com/user-attachments/assets/f8109c15-717f-42b6-ae9c-fcda474afb9c" />

        
        <aside>
        
        비교적 직무 레벨이 낮은 Sales 부서. JobLevel이 낮은 업무에서 이직률이 높다.
        
        단순 노동은 직무 교육을 통해서 효율성을 증대시키기 어렵다. 효율을 증대시켜 워라벨을 챙겨주는 전략은 비효율적이다.
        
        </aside>
        
        <img width="653" height="387" alt="image" src="https://github.com/user-attachments/assets/a6e5b078-7d5d-42d9-887c-b7d5d4df966b" />

        
        <aside>
        
        각 직무별 이직률이 높은 순서로 나열했을 때 월급 그래프를 보면 낮은 월급을 받는 쪽에서 이직률이 높다는 사실을 볼 수 있다. 특히 매니저나 연구 소장 같은 책임자나 관리직은 낮은 이직률을 보인다.
        
        생각 2.
        
        영업직에게 직무 교육을 통해 효율을 높이기엔 무리가 있다. 때문에 이는 월급 같은 보상을 주거나, 추가적인 고용을 활용해 업무를 분담하여 야근을 줄이게 만들어 이직률을 감소시키는 방법이 현실적일 것이라 판단된다. 업무 만족도를 높이는 것에 영향을 미치는 것이 좋다. 
        
        </aside>
        
        <img width="652" height="513" alt="image" src="https://github.com/user-attachments/assets/f17150b9-066c-40cd-a5cf-d93656b46af3" />

        
        <aside>
        
        업무 만족도가 낮은 사람의 이직률이 가장 높다.
        
        </aside>
        
        <aside>
        
        총정리!
        
        1. Sales 부서의 이직률이 가장 높고 이 비율을 낮춘다면 전체 이직률을 줄일 수 있을 것이다.
        2. 이직률이 높은 부서의 JobLevel은 1에 가까운 단순 노동이다. 이는 교육을 통해 효율을 증가시키기 어려운 파트이다. 따라서 추가적인 고용이나 업무 만족도 증가를 통해 이직률을 감소시켜야한다.
        3. 야근하는 사람이 이직률이 매우 높았고, 이들이 야근을 하지 않게 추가적인 고용으로 업무를 분담해 준다면 이직률을 감소시킬 수 있을 것이다.
        4. 이직률이 높은 순서대로 직책을 나열했을 때, 그들의 월급이 낮은순과 그 순서가 거의 동일했다.
        5. 따라서 추가적인 월급으로 업무 만족도 증대, 추가적인 업무 분담을 통해 야근을 줄여 업무 만족도를 증대시켜 이직률을 감소시킬 수 있을 것이다.
        </aside>
        
        시뮬레이션!!!
        
        한국을 기준으로 생각했을 때, 주 40시간 기준으로 야근하지 않는 사람과 야근 하는 사람의 일하는 시간은 다음과 같다.
        
        <img width="654" height="180" alt="image" src="https://github.com/user-attachments/assets/615a751a-4824-4a82-b792-7da3d34676b0" />

        
        Sales 부서에서 사람을 추가적으로 고용해 야근 하는 사람을 야근 하지 않기 위해 필요한 추가 고용 인원을 계산하면 다음과 같다. 
        
        <img width="655" height="356" alt="image" src="https://github.com/user-attachments/assets/e46b00f7-e10a-4f9f-a836-c4b355277456" />

        
        추가 고용을 통해 Sales 야근 했을 때의 이직률인  38% 와 야근 안할때의 이직률인 17%로 개선 시키게 된다면 추가 인원에 따라 이직률이 다음과 같이 감소할 것이다. 
        
        <img width="650" height="401" alt="image" src="https://github.com/user-attachments/assets/5850a5cd-e26d-481b-8845-6b1c256b1929" />

        
        시뮬레이션을 통해 바라본 이 전략의 기대 효과
        
        <aside>
        
        1. 처음 1000명의 사람을 고용한다. (이들의 연차는 1년차)
        2. 교체 비율 x%에 따라 그 비율만큼 노드를 삭제한다.
        3. 그 이후 다시 인원수가 1000이 되게끔 추가 노드를 추가해준다.
        4. 기존에 있었던 노드들의 연차는 +1, 추가한 노드의 연차는 다시 1년차가 된다.
        5. 이를 총 15턴까지 진행한다.
        6. 이 게임을 총 1000번 반복해서 각 연차별 노드 숫자를 계산한다.
        </aside>
        
        추가 고용이 완전히 다 됐을 때 이직률인 17%에선 처음에 고용했던 인원이 15년이 지나도 꽤 많은 비율로 남아 있었다. (높은 경험치가 있는 사람 보유 가능성 증가)
        
        <img width="652" height="356" alt="image" src="https://github.com/user-attachments/assets/06f3bd89-782d-48fd-85d0-67602736a337" />

        
        추가 고용이 없었을 때의 이직률인 38%에선 처음에 고용했던 인원이 거의 남지 않았다.
        
        <img width="651" height="356" alt="image" src="https://github.com/user-attachments/assets/cfb66be7-8ccd-484c-bf8b-53ad7a30d80b" />

        
        <aside>
        
        추가 고용을 통해 이직률을 낮일 수 있다면, 더 높은 년차의 사람을 보유한 기업이 될 것이다.
        
        Sales 부서는 년차별 연봉 증가도 크지 않으므로 월급 소비 대비 더 높은 능력을 보유하게 될 것이다.
        
        </aside>
        
    - 2.1.2. Research & Development 부서 이직률 감소 전략
        - 사용 변수
        
        <aside>
        
        Attrition
        
        Department
        
        EmployeeNumber
        
        JobRole
        
        MonthlyIncome
        
        OverTime
        
        TrainingTimesLastYear
        
        CareerStage
        
        </aside>
        
        - 주요 사용 변수 설명
        
        <img width="670" height="652" alt="image" src="https://github.com/user-attachments/assets/f0bc508a-8536-4617-87ec-7c17a6da5527" />

        
        - 인사이트 및 가설 정리
        
        <aside>
        
        *Laboratory Technician, Research Scientist 직무의 이직률이 가장 높다. 
        
         그러므로 두 직무의 이직률을 감소시키는 것을 목표로 분석 및 전략을 수립해야 한다.
        
        - 가설 정리
        1. 비율이 높은 두 직무들의 이직자들은 평균 월급도 낮고 경력 단계가 낮을 것이다.
        2. 비율이 높은 두 직무들의 이직자들은 야근 비율이 높고 경력 단계도 낮을 것이다.
        3. 비율이 높은 두 직무들의 이직자들은 교육 횟수가 낮을 것이다.
        </aside>
        
        - 분석 결과
            - 두 직무 내 이직자들의 커리어단계와 연차에 비례한 월급 상승률의 연관성
            
            <img width="639" height="341" alt="image" src="https://github.com/user-attachments/assets/9de1a7c7-eb1a-42b1-900a-2652b887ca19" />

            
            <aside>
            
            1. 두 직무 모두 인턴 단계의 전체 비중이 높고 이직 수 또한 인턴 단계에서 대다수의 이직 인원들이 나오고 있다.
            2. 두 직무 모두 인턴과 주니어 단계에서 상위 경력 단계로 넘어간 인원이 거의 없다.
            3. 두 직무 모두 10년 이상의 연차 전까지는 월급 상승률이 미미하다.
            
            → 인턴 단계의 인원들 이직률을 감소시키기 위해서 인턴 단계의 복지 및 관련된 전략을 수립해야 한다.
            
            </aside>
            
            - 두 직무 내 이직자들의 야근 비율과 경력 단계의 연관성
            
            <img width="631" height="427" alt="image" src="https://github.com/user-attachments/assets/3c2dd7b3-31fa-4dc7-8403-05d63ca9bb81" />

            
            <aside>
            
            1. 야근 인원에서 인턴 단계의 비중이 대부분을 차지하고 있다.
            2. 인턴 단계의 많은 인원들이 야근을 경험하고 이직하고 있다.
            3. 두 직무의 인턴 단계의 인원들이 적은 월급에 비해 야근 비율이 높다.
            
            → 이직률을 감소시키기 위해서는 인턴과 주니어 단계같이 낮은 경력의 인원들에게 야근에 맞는 보상 정책 또는 복지 전략을 세워야 한다.
            
            </aside>
            
            - 두 직무 내 이직자들의 이직률과 교육 횟수의 연관성
                
                <img width="626" height="791" alt="image" src="https://github.com/user-attachments/assets/dd10d6cc-0efe-4750-ad0a-8052d9ad8878" />

            
        
        <aside>
        
        1. 두 직무 모두 전체 이직자 중 상당수가 2회 이하의 교육을 받았었다.
        
        → 가장 교육이 필요한 인턴 인원의 교육 및 양성 시스템을 더 강화하는 전략을 수립해야 한다. 
        
        </aside>
        
        ---
        
        - 인사이트 도출 및 제안
        
        <aside>
        
        - 개발 부서에서 가장 이직률이 높은 직무는 Laboratory Technician와 Research Scientist이다.
        - 개발 부서 내에서 두 직무의 평균 월급은 가장 낮고 야근율은 가장 높다.
        - 두 직무의 대부분 인원은 인턴 단계로 구성되어 있다.
        - 두 직무 인원의 상당수가 인턴과 주니어 단계에서 상위 단계로 넘어가지 못 하고 이직한다.
        - 두 직무의 이직자 중 상당수의 인원이 야근을 경험했고 그 중 대다수가 인턴 단계이다.
        - 두 직무의 이직자 중 상당수의 인원이 2회 이하의 교육을 받고 이직했다.
        - 이직 인원들의 대다수는 월급도 낮고 높은 야근율을 가진 인턴 단계 인원들이다. 심지어 충분한 횟수의 교육을 받지 못 하는 상황에서 연차가 쌓여도 월급 상승율이 높지 않기 때문에 버티지 못하고결국 이직을 선택하는 것으로 보인다.
        
        - 두 직무의 이직률을 감소시키기 위한 전략
            - 인턴 단계 인원들의 초기 교육 강화 및 시니어 또는 전문가 단계의 인원과 사수 부사수 형식의  멘토링 프로그램
            - 높은 야근율에 맞는 야근 수당 및 추가 보상 제도
            - 높은 성과에 맞는 승진 시스템 개선
        </aside>
        
- **2.2. 커리어단계(CareerStage)별 이직률 감소 전략**
    - 2.2.1.  커리어단계별 학력수준과 이직여부의 연관성
        - 사용 변수
        
        <aside>
        
        Attrition
        
        Department
        
        Education
        
        EducationField
        
        CareerStage
        
        </aside>
        
        - 주요 사용 변수 설명
            
      <img width="593" height="989" alt="image" src="https://github.com/user-attachments/assets/8ddde08f-d8fe-4b25-8891-5dfefc541323" />

        
        <aside>
        
        1. 이직 여부에 따라 커리어단계별 학력수준에는 차이가 있다.
        2. 이직자 중 Junior인 사람들은 전공분야에 따라 교육 수준의 차이가 있다.
        3. 이직여부 및 부서별 커리어단계에 따라 학력수준에 차이가 있다.
        </aside>
        
        - 분석결과
            - 이직여부에 따른 커리어단계와 학력수준의 연관성
                
                <img width="540" height="244" alt="image" src="https://github.com/user-attachments/assets/01729b5a-f7e1-409b-a9a5-ea584db93391" />

                
            
            <aside>
            
            1. 이직여부에 상관없이 대부분 학력수준이 3 > 4 > 2 > 1> 5 순으로 많다. 
            2. 이직자 중 Junior 학력수준이 4인 사람이 가장 많다.
            
            → Junior의 이직률을 감소하기 위해서는 고학력자들을 대상으로 전략을 수립해야 한다.
            
            </aside>
            
            - 이직자 중 Junior인 사람들의 학력수준과 전공분야의 연관성
                
                <img width="539" height="430" alt="image" src="https://github.com/user-attachments/assets/82176e42-efda-47b6-ad9a-679d67c0a78b" />

                
            
            <aside>
            
            1. 대부분 전공분야와 상관없이 고학력자의 이직률이 높다.
            2. Life Science 전공자는 학력수준이 낮은 사람들의 이직률이 높다. 
            
            → Junior 단계의 Life Science 전공자는 저학력자들을 중점으로 전략을 수립해야 한다.
            
            </aside>
            
            - 이직여부/부서별 커리어단계와 학력수준의 연관성
            
                   <img width="569" height="407" alt="image" src="https://github.com/user-attachments/assets/974f3345-26c3-426a-9ce9-8d603652ef62" />

            
            <aside>
            
            1. Research & Development 부서는 Junior, Mid-level의 학력수준이 4인 사람의 이직률이 높다.
            2. Sales 부서는 Junior의 학력수준이 4인 사람의 이직률이 높다.
            3. HR 부서는 Intern의 학력수준이 4~5인 사람이,  Mid-level의 학력수준이 2~3인 사람의 이직률이 높다.
            
            → 부서별로 특정 커리어단계의 학력수준에 따른 이직률 감소 전략을 세워야 한다.
            
            </aside>
            
        
        ---
        
        - 인사이트 도출 및 제안
        
        <aside>
        
        - 이직자는 커리어단계가 Intern > Junior > Mid-level > Senior > Expert 순으로 분포한다.
        - 이직여부에 상관없이 대부분 학력수준이 3 > 4 > 2 > 1> 5 순으로 많다.
        - 이직자 중 Junior 학력수준이 4인 사람이 가장 많다.
        - Junior 중 Life Science 전공자는 학력수준이 낮은 사람들의 이직률이 높다.
        - Research & Development 부서는 Mid-level의 학력수준이 4인 사람의 이직률이 높다.
        - Sales 부서는 Junior의 학력수준이 4인 사람의 이직률이 높다.
        - HR 부서는 Intern의 학력수준이 4~5인 사람이,  Mid-level의 학력수준이 2~3인 사람의 이직률이 높다.
        - 이직률을 감소하기 위한 전략 제안:
            - 인턴의 이직률이 가장 높기는 하지만, 투자 대비 손실 규모와 업무 공백을 최소화하기 위해서는 인턴보다는 주니어, 미드 등의 이직률을 감소하는 것이 중요하다.
            - 주니어의 경우 고학력자의 이직이 많은데, 그 이유는 성장 기회, 학습 및 발전 가능성에 대한 기대감이 높기 때문이다. 그러므로 명확한 커리어 로드 맵을 제공하거나 멘토링 제도를 실시한다.(관련논문: *Overqualified Employees’ Actual Turnover: The Role of Growth Dissatisfaction and the Contextual Effects of Age and Pay* (Mah, Huang, Yun, 2024)
            - 주니어 중에 전공분야에 따른 학력수준에 약간의 차이가 있다.
            
                  - Life Science 전공자는 학력수준이 낮은 사람들의 이직률이 높기 때문에 장학금 제도를 실시하거나 학교와 연계하여 야간 수업을 들을 수 있도록 환경을 조성한다.
            
            - 부서별로 커리어단계에 따른 학력수준 차이가 존재하므로 각각에 맞는 전략을 수행한다.
        </aside>
        
    - 2.2.2.  커리어단계별 월급과 이직여부의 연관성
        - 사용 변수
        
        <aside>
        
        Attrition
        
        MonthlyIncome
        
        EnvironmentSatisfaction
        
        CareerStage
        
        OverTime
        
        </aside>
        
        - 주요 사용 변수 설명
        
            <img width="609" height="455" alt="image" src="https://github.com/user-attachments/assets/f6643b4b-e061-4785-b79a-4a5a4915d96e" />

        
        <aside>
        
        1. 이직 여부에 따라 커리어단계별 월급에는 차이가 있다.
        2. 이직자 중 Senior인 사람들은 근무만족환경도에 따라 월급의 차이가 있다.
        3. 이직여부에 따라 커리어단계별 초과근무 여부의 월급에는 차이가 있다.
        </aside>
        
        - 분석결과
            - 이직여부에 따른 커리어단계와 월급의 연관성
                
                <img width="434" height="307" alt="image" src="https://github.com/user-attachments/assets/b7179bc1-3a14-4463-8f08-2ea9867efdf1" />

                
            
            <aside>
            
            1. 이직여부에 상관없이 커리어단계가 높아질수록 월급도 올라간다.
            2. Senior 단계의 사람들은 이직자의 월급이 비이직자의 월급보다 확연히 적다.
            
            → Senior의 이직률을 감소하기 위해서는 월급과 관련된 전략을 수립해야 한다.
            
            </aside>
            
            - 이직자 중 Senior인 사람들의 근무환경만족도와 월급의 연관성
            
            <img width="564" height="365" alt="image" src="https://github.com/user-attachments/assets/6e4fe371-d5d0-4d1e-aacf-96cf458da6d6" />

            
            <aside>
            
            1.  이직자는 대부분의 월급이 상대적으로 낮고, 환경 만족도가 낮은 사람들의 분포가 많다. 
            2. 비이직자는 높은 월급을 받는 사람들은 환경 만족도가 낮더라도 이직하지 않는 경우가 있다 
            
            → 월급과 환경 만족도가 낮은 직원이 가장 높은 이직 위험군이다.
            
            </aside>
            
            - 이직여부에 따른 Mid-level 사람들의 초과근무, 월급의 연관성
                
                <img width="542" height="559" alt="image" src="https://github.com/user-attachments/assets/7a5fc4ad-7f2d-40bb-b9bb-df01aa48c324" />

                
            
            <aside>
            
            1. 이직자는 비이직자에 비해 초과근무 비율이 상대적으로 높다.
            2. 초과근무별 월급 분포의 중연차 인력인 Mid-level 이직자는 초과근무 여부에 따른 월급 차이는 뚜렷하지 않다.
            
            → 보상과 초과근무 간의 불균형이 이직의 원인이 될 수 있다.
            
            </aside>
            
            ---
            
        - 인사이트 도출 및 제안
            
            <aside>
            
            - 이직자는 비이직자보다 월급이 적다.
            - Senior 단계의 사람들은 이직자의 월급이 비이직자의 월급보다 확연히 적다.
            - 시니어 중 이직자는 대부분의 월급이 상대적으로 낮고, 근무환경만족도가 낮은 사람들의 분포가 많다.
            - 이직자는 비이직자보다 초과근무를 경험한 비율이 높다.
            - 이직률을 감소하기 위한 전략 제안:
                - 월급을 올리면 이직률이 감소하지만, 전체 직원의 월급을 올리는 것은 현실적으로 불가능하다. 그러므로 일부 그룹을 선정하여 월급을 올린다.
                
                    - 이직자와 비이직자의 월급 차이가 큰 시니어 단계의 월급을 올린다.
                
                    - 시니어는 월급이 낮고 근무환경만족도가 낮은 직원을 이직 가능성이 높은 위험군으로 분류하여 월급을 올리거나 근무 환경을 개선할 필요성이 있다.
                
                - 미드는 근무시간 관리 강화와 월급 인상 외의 실질적인 초과근무 보상제도(수당, 휴가 등)를 고려해야한다.
            </aside>
            

# 3️⃣ 종합 결론 및 전략 제안

---

## 3.1. 주요 공통 인사이트 요약

<aside>

1. 부서별 이직률 감소 전략
    
     Human Resources 부서는 다른 부서에 비해 직원 수가 너무 적기 때문에 분석 결과가 일반화될 우려가 있기에 데이터 수가 충분한 Sales부서와 Research & Development 부서를 중점적으로 분석한다.
    
- Sales 부서
    1. Sales부서는 JobLevel이 1(단순 노동)인 직원이 많다. 단순 노동 업무는 교육을 통한 효율 증가가 어려운 업무이다. 그러므로 추가적인 직원 고용이나 업무 만족도 증가를 통해 이직률을 감소해야한다.
    2. Sales 부서의 초과근무 경험이 있는 사람의 이직률이 매우 높았기 때문에 초과근무를 하지 않도록 추가적인 직원 고용을 통해 업무를 분담해 준다면 이직률을 감소할 수 있다..
    3. Sales 부서의 직무를 이직률이 높은 순서대로 나열했을 때 판매직이 가장 이직률이 높고, 매니저나 감독자의 이직률이 가장 낮았다. 또한 이직률이 높은 직무일수록 월급이 적었다. 그러므로 월급을 올리거나 할당된 직무보다 JobLevel이 높은 직무를 할당하여 성취감을 고조시키는 등의 방법을 통해 이직률을 감소할 수 있다.
    4. Sales 부서는 업무만족도가 낮을수록 이직률이 높기 때문에 업무 분배를 재할당하여 이직률을 감소할 수 있다.
- Research & Development 부서
    1. 개발 부서에서 이직률이 높은 직무는 Laboratory Technician와 Research Scientist이다. 
        - 두 직무의 평균 월급은 가장 낮고 야근율은 가장 높다.
        - 두 직무의 대부분 인원은 인턴 단계로 구성되어 있다.
        - 두 직무 인원의 상당수가 인턴과 주니어 단계에서 상위 단계로 넘어가지 못 하고 이직한다.
        - 두 직무의 이직자 중 상당수의 인원이 야근을 경험했고 그 중 대다수가 인턴 단계이다.
        - 두 직무의 이직자 중 상당수의 인원이 2회 이하의 교육을 받고 이직했다.
            
            → 이직자들의 대다수는 월급도 낮고 높은 야근율을 가진 인턴 단계 인원들이다. 심지어 충분한 횟수의 교육을 받지 못 하는 상황에서 연차가 쌓여도 월급 상승율이 높지 않기 때문에 버티지 못하고 결국 이직을 선택하는 것으로 보인다.
            
        
        그러므로 인턴 단계의 초기 교육을 강화하거나 고연차 인력들과의 사수/부사수 형식의 멘토링 프로그램을 통해 이직률을 감소할 수 있다.
        
1. 커리어별 이직률 감소 전략
    
    인턴의 이직률이 가장 높기는 하지만, 투자 대비 손실 규모와 업무 공백을 최소화하기 위해서는 인턴보다는 주니어 이상 단계의 중고연차 인력들의 이직률을 감소하는 것이 중요하다. 또한 전문가의 경우 데이터 수가 너무 작기 때문에 일반화의 오류를 최소화하기 위해 분석에서 제외한다.
    
- 중연차(Junior & Mid-level) 이직율 감소 전략
    1. 주니어는 학력수준이 4인 고학력을 보유한 직원이 가장 많은데, 그 이유는 성장 기회, 학습 및 발전 가능성에 대한 기대감이 높기 때문이다. 그러므로 명확한 커리어 로드 맵을 제공하거나 멘토링 제도를 실시하여 이직률을 감소할 수 있다.
        - 주니어는 대부분의 전공분야에 따른 이직률은 학력수준이 높은 직원이 많았는데, 예외적으로 Life Science 전공자는 학력수준이 낮은 직원의 이직률이 높았다. 그러므로 주니어 중 Life Science 전공자를 대상으로 학력을 높일 수 있는 제도를 지원하면 이직률을 감소할 수 있다.
    2. 미드는 Research & Development 부서 내에 학력수준이 4인 사람의 이직률이 높은 반면, Human Resources 부서 내에 학력수준은 2~3인 사람의 이직률이 높다. 그러므로 각 부서별로 다른 전략을 세워야한다.
    3. 전체 직원을 대상으로 했을 때, 이직자는 비이직자에 비해 초과근무 비율이 상대적으로 높다. 그러나 미드의 이직자의 경우, 초과근무 여부에 따른 월급 차이는 뚜렷하지 않기 때문에 초과근무에 대한 적절한 보상이 이뤄지지 않다고 볼 수 있다. 그러므로 초과근무 보상제도를 개선한다면 이직률을 감소할 수 있다.
- 고연차(Senior) 이직율 감소 전략
    1. 시니어는  이직자의 월급이 비이직자의 월급보다 확연히 적다.
        - 시니어 중 월급이 낮고 근무환경만족도가 낮은 직원을 이직 가능성이 높은 위험군으로 분류하여 월급을 올리거나 근무 환경을 개선하면 이직률을 감소할 수 있다.
</aside>

## 3.2. 종합 인사 전략 제안

<aside>

- Sales 부서
    - 단순 노동 업무 비중이 높지만, 해당 업무는 교육을 통한 효율 증가가 어렵기 때문에 추가적으로 직원을 고용하는 전략
    - 초과근무 감소를 위해 추가적으로 직원을 고용하는 전략
    - 업무 만족도 증가를 위한 업무 분배를 재할당하는 전략
    - 이직률이 높은 직무(판매직)을 대상으로 월급을 올리거나 할당된 직무보다 JobLevel이 높은 직무를 할당하여 성취감을 고조시키는 전략
- Research & Development 부서
    - 이직률이 높은 직무(Laboratory Technician, Research Scientist)을 대상으로 월급을 올리거나 야근에 맞는 보상 정책 또는 복지를 개선하는 전략
    - 이직률이 높은 직무 중 비중이 높은 인턴을 대상으로 초기 교육을 강화하거나 고연차 인력들과의 사수/부사수 형식의 멘토링 프로그램을 실시하는 전략
- 중연차(Junior & Mid-level) 이직율 감소 전략
    - 주니어는 고학력자들을 대상으로 명확한 커리어 로드 맵을 제공하거나 멘토링 제도를 실시하는 전략
    - 주니어 중 Life Science 전공자를 대상으로 학력을 높일 수 있는 장학금 제도나 학교와 연계하여 야간 학습을 위한 분위기를 조성하는 전략
    - 미드를 대상으로 초과근무에 대해 금전적으로 보상하는 제도를 개선하는 전략
    - 미드 중 Research & Development 부서 직원을 대상으로 고학력자를 위한 명확한 커리어 로드 맵을 제공하거나 멘토링 제도를 실시하는 전략
    - 미드 중 Human Resources 부서 직원을 대상으로 저학력자를 위한 장학금 제도나 학교와 연계하여 야간 학습을 위한 분위기를 조성하는 전략
- 고연차(Senior) 이직율 감소 전략
    - 시니어 중 월급이 낮고 근무환경만족도가 낮은 직원을 대상으로 월급을 올리거나 근무 환경을 개선하는 전략
</aside>
