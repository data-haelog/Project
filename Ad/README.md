# 광고 클릭 예측 머신러닝 프로젝트

**프로젝트명**
광고 클릭 예측 시스템 (Ad Click Prediction System)

**개발개요**
- **프로젝트 기간**: 2025.01.01 ~ 2025.02.04 (5주)
- **프로젝트 인원**: 1명 (개인 프로젝트)
- **프로젝트 목적**: 
  - 사용자 행동 데이터 기반 광고 클릭 예측 머신러닝 모델 개발
  - 고효율 타겟 세그먼트 발굴 및 광고 캠페인 최적화 전략 수립
  - 데이터 기반 의사결정을 위한 비즈니스 인사이트 도출
- **프로젝트 성과**:
  - 모델 정확도 96.5%, ROC-AUC 0.993 달성
  - 고효율 세그먼트 발굴 (클릭률 98.4%, 전체 대비 +96.8%)
  - 예상 광고 효율(ROAS) 50% 이상 개선 가능


### 데이터 설명
이 데이터셋은 온라인 광고 클릭 데이터를 기반으로 하며, 다음과 같은 특성(features)을 포함합니다:

| 컬럼명                   | 설명 |
|---------------------------|------|
| `Daily Time Spent on Site` | 사용자가 사이트에서 머문 시간(분 단위) |
| `Age`                     | 고객 나이(년 단위) |
| `Area Income`             | 고객이 속한 지역의 평균 소득 |
| `Daily Internet Usage`    | 사용자의 하루 평균 인터넷 사용 시간(분 단위) |
| `Ad Topic Line`           | 광고 헤드라인 텍스트 |
| `City`                    | 고객이 거주하는 도시 |
| `Male`                    | 고객 성별(1: 남성, 0: 여성) |
| `Country`                 | 고객 국가 |
| `Timestamp`               | 광고 클릭 또는 창 닫은 시각 |
| `Clicked on Ad`           | 광고 클릭 여부(0: 클릭 X, 1: 클릭 O) |

> 이 데이터셋을 활용하여 광고 클릭과 관련된 패턴을 분석하고, 클릭 여부를 예측하는 모델을 구축할 수 있습니다.

### 폴더구성
Ad
│
├── data
│   └── advertising.csv
│
├── notebooks
│   └── ad_analysis.ipynb
│
├── src
│   ├── __init__.py
│   ├── data_loader.py
│   ├── eda.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── evaluation.py
│
├── main.py
├── config.py
├── requirements.txt
└── README.md

**구현기술**

**1. 개발 환경**
- Language: Python 3.13
- IDE: VS Code

**2. 데이터 분석**
- pandas: 데이터 전처리, 탐색적 데이터 분석
- numpy: 수치 연산 및 배열 처리
- scipy: 통계 검정 (t-test, chi-square test)

**3. 머신러닝**
- scikit-learn: 모델 학습 및 평가
  - 7개 모델: Random Forest, Logistic Regression, Gradient Boosting, SVM, KNN, Decision Tree, Naive Bayes
  - GridSearchCV: 하이퍼파라미터 최적화 (540개 조합)
  - Cross Validation: 5-Fold 교차 검증

**4. 시각화**
- matplotlib: 그래프 생성 (7종)
- seaborn: 통계적 시각화 (히트맵, 박스플롯)

**5. 프로젝트 구조**
- 모듈화 설계: config.py, data_loader.py, eda.py, feature_engineering.py, model_training.py, evaluation.py
- 자동화: main.py 통합 실행 파일

**담당업무**

**1. 데이터 수집 및 전처리**
- advertising.csv 데이터 확보 (1,000건, 10개 변수)
- 결측치 확인 및 데이터 품질 검증
- 클래스 균형 확인 (클릭 50%, 비클릭 50%)
- Train/Test 데이터 분할 (80:20 비율, Stratified Sampling)

**2. 탐색적 데이터 분석 (EDA)**
- 기술 통계량 분석 및 변수 분포 확인
- t-test를 통한 변수별 클릭 여부 차이 검정 (p < 0.001)
- 상관관계 분석 (Pearson Correlation)
  - Daily Internet Usage ↔ 클릭: -0.79 (강한 음의 상관관계)
  - Age ↔ 클릭: +0.49 (중간 양의 상관관계)
- 세그먼트 분석
  - 연령대별 클릭률: 18-25세 28.6% → 56세+ 100%
  - 소득 구간별 클릭률: 저소득 93.2%, 중소득 57.1%, 고소득 27.6%

**3. Feature Engineering**
- 9개 파생변수 생성
  - Engagement_Score: 사이트 체류시간 + 인터넷 사용시간
  - Ad_Affinity_Score: 연령, 체류시간, 소득 기반 광고 친화도
  - Income_Age_Ratio: 소득/연령 비율
  - Low_Engagement_High_Age: 저체류시간 & 고연령 플래그
  - Time_Income_Interaction: 체류시간 × 소득 상호작용
  - Age_Squared: 연령 제곱항
  - Is_Senior: 50세 이상 플래그
  - Is_Low_Income: 저소득층 플래그
  - High_Usage: 높은 인터넷 사용 플래그

**4. 머신러닝 모델 개발**
- 7개 모델 학습 및 성능 비교
  - Naive Bayes: ROC-AUC 0.993
  - Random Forest: ROC-AUC 0.993 (최종 선택)
  - Logistic Regression: ROC-AUC 0.992
  - KNN: ROC-AUC 0.988
  - Gradient Boosting: ROC-AUC 0.987
  - SVM: ROC-AUC 0.986
  - Decision Tree: ROC-AUC 0.949
- Random Forest 하이퍼파라미터 튜닝
  - GridSearchCV 활용 (540개 조합 탐색)
  - 최적 파라미터: n_estimators=50, max_depth=15, min_samples_leaf=4
  - CV ROC-AUC: 0.9925

**5. 모델 평가 및 검증**
- 성능 지표 분석
  - Accuracy: 96.5% (193/200)
  - Precision: 97.0%
  - Recall: 97.0%
  - F1-Score: 97.0%
  - ROC-AUC: 0.9905
- Confusion Matrix 분석
  - True Negative: 96건, True Positive: 97건
  - False Positive: 4건, False Negative: 3건
- Feature Importance 분석
  - Engagement_Score: 32.5% (가장 중요)
  - Time_Income_Interaction: 16.6%
  - Daily Internet Usage: 16.0%
- 5-Fold Cross Validation으로 모델 안정성 검증

**6. 고효율 타겟 세그먼트 발굴**
- 세그먼트 A (40세 이상 & 체류시간 60분 이하)
  - 표본 수: 185명
  - 클릭률: 98.38%
  - 개선율: +96.8%
- 세그먼트 B (저소득 & 인터넷 사용 180분 이하)
  - 표본 수: 120명
  - 클릭률: 100%
  - 개선율: +100%

**7. 시각화 및 리포트 작성**
- 7종 그래프 생성
  - target_distribution.png: 타겟 변수 분포
  - numeric_features_analysis.png: 수치형 변수 박스플롯
  - segment_analysis.png: 세그먼트별 클릭률
  - correlation_matrix.png: 상관관계 히트맵
  - confusion_matrix.png: 혼동 행렬
  - feature_importance.png: 변수 중요도
  - roc_curves.png: ROC 곡선 비교
- HTML 종합 리포트 생성 (report.html)
- 비즈니스 인사이트 및 권장사항 작성
  - 단기 전략: 40세 이상 광고 노출 2배 증가
  - 중기 전략: 실시간 타겟팅 시스템 구축
  - 장기 전략: 개인화 광고 추천 시스템 고도화

**8. 코드 모듈화 및 문서화**
- 재사용 가능한 모듈 구조 설계 (src 폴더)
- config.py를 통한 설정 관리
- main.py 통합 실행 파일 작성

- README.md 및 주석 작성
