# 보드게임 추천 시스템 - 최종 보고서

## 프로젝트 개요

### 목표
사용자의 평가 데이터를 기반으로 보드게임을 추천하는 AI 시스템 개발

### 데이터셋
- **전체 평점 데이터**: 18,942,215개
- **필터링 후**: 14,733,960개
- **사용자 수**: 93,637명
- **게임 수**: 12,302개
- **희소성**: 98.98%

---

## 모델 개발 과정

### 1. Baseline 모델 (협업 필터링)

| 모델 | RMSE | MAE |
|------|------|-----|
| User + Game Bias | 1.1960 | 0.9041 |
| Game Average | 1.2923 | 0.9792 |
| User Average | 1.3535 | 1.0203 |
| Global Average | 1.4977 | 1.1138 |
| NMF (k=50) | 5.6870 | 5.4159 |


**최고 성능**: User + Game Bias (RMSE: 1.1960)

### 2. 딥러닝 모델 (PyTorch NCF)

**모델 구조**:
- User Embedding: 93,637 x 64
- Game Embedding: 12,302 x 64
- Hidden Layers: [128, 64, 32]
- 총 파라미터: 6,806,977개

**학습 결과**:
- Epochs: 10
- 최종 RMSE: 1.1071
- 최종 MAE: 0.8265
- Baseline 대비 개선: 7.43%

### 3. 모델 경량화

| 모델 | RMSE | MAE | 크기 (MB) |
|------|------|-----|----------|
| FP32 (Original) | 1.1071 | 0.8265 | 25.97 |
| INT8 (Dynamic) | 1.1077 | 0.8268 | 25.90 |
| 2-bit (Simulated) | 1.3302 | 1.0145 | 1.72 |


**2-bit 양자화 성과**:
- 모델 크기: 25.97 MB → 1.72 MB (93.4% 감소)
- RMSE: 1.1071 → 1.3302 (+0.2231)
- 정확도-크기 Trade-off 달성

---

## 핵심 성과

### 1. 정확도 개선
- Baseline 최고 RMSE: 1.1960
- PyTorch NCF RMSE: 1.1071
- **개선율: 7.43%**

### 2. 모델 경량화
- 원본 모델 크기: 25.97 MB
- 2-bit 모델 크기: 1.72 MB
- **압축률: 93.4%**

### 3. 기술 스택
- **언어**: Python 3.13
- **프레임워크**: PyTorch
- **데이터 처리**: pandas, numpy
- **머신러닝**: scikit-learn
- **데이터베이스**: SQLite
- **시각화**: matplotlib, seaborn

---

## 프로젝트 구조

```
Game/
├── data/                   # 원본 데이터
├── notebooks/              # Jupyter Notebooks
│   ├── 01_EDA.ipynb
│   ├── 02_Baseline_Models.ipynb
│   ├── 03_Deep_Learning.ipynb
│   ├── 04_Quantization.ipynb
│   └── 05_Evaluation.ipynb
├── outputs/
│   ├── figures/            # 시각화 (10개 그래프)
│   ├── models/             # 학습된 모델
│   └── reports/            # 분석 보고서
└── README.md
```

---

## 결론

### 주요 기여
1. **대규모 데이터** (1,894만 개 평점) 처리 및 분석
2. **딥러닝 기반 추천 시스템** 구현 (PyTorch NCF)
3. **2-bit 양자화** 기술로 모델 경량화 (93.4% 크기 감소)
4. **SQL 활용** 데이터 분석 (5개 쿼리)

### 실무 적용 가능성
- 모바일/웹 환경 배포 가능 (경량화 모델)
- 확장 가능한 아키텍처
- 실시간 추천 시스템 구현 가능

---

**작성일**: 2025년  
**프로젝트 기간**: 5주  
**사용 기술**: Python, PyTorch, SQL, scikit-learn, pandas
