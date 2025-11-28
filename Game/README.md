# 보드게임 추천 시스템 (BoardGame Recommendation System)

AI 기반 보드게임 추천 시스템 
- (PyTorch Neural Collaborative Filtering + 2-bit Quantization)

## 프로젝트 개요

1,894만 개의 사용자 평점 데이터를 활용한 딥러닝 추천 시스템 구축 및 모델 경량화

### 주요 성과

- **정확도**: Baseline 대비 7.43% 개선 (RMSE 1.1960 → 1.1071)
- **경량화**: 2-bit 양자화로 93.4% 크기 감소 (25.97 MB → 1.72 MB)
- **기술**: PyTorch NCF, SQL 분석, 모델 최적화

---

## 프로젝트 구조

```
Game/
├── data/                           # 데이터 (CSV 파일)
│   ├── games.csv                   # 게임 메타데이터
│   ├── user_ratings.csv            # 사용자 평점 (1,894만 개)
│   ├── ratings_distribution.csv    # 평점 분포
│   ├── mechanics.csv               # 게임 메커니즘
│   └── boardgame.db                # SQLite 데이터베이스
│
├── notebooks/                      # Jupyter Notebooks
│   ├── 01_EDA_Final.ipynb          # 탐색적 데이터 분석 + SQL
│   ├── 02_Baseline_Models.ipynb    # 협업 필터링 (5개 모델)
│   ├── 03_Deep_Learning.ipynb      # PyTorch NCF
│   ├── 04_Quantization.ipynb       # 모델 경량화 (INT8, 2-bit)
│   └── 05_Evaluation.ipynb         # 종합 평가
│
├── outputs/
│   ├── figures/                    # 시각화
│   │   ├── 01_rating_analysis.png           # 평점 분포
│   │   ├── 02_sparsity_segments.png        # 데이터 희소성
│   │   ├── 03_baseline_comparison.png      # Baseline 비교
│   │   ├── 04_prediction_scatter.png       # 예측 vs 실제
│   │   ├── 05_ncf_training.png             # NCF 학습 곡선
│   │   ├── 06_ncf_predictions.png          # NCF 예측
│   │   ├── 07_quantization_comparison.png  # 양자화 비교
│   │   ├── 08_overall_comparison.png       # 전체 모델 비교
│   │   ├── 09_tradeoff_analysis.png        # 정확도-크기 Trade-off
│   │   └── 10_ncf_learning_curve.png       # 학습 곡선
│   │
│   ├── models/                     # 학습된 모델
│   │   ├── baseline_models.pkl              # Baseline 모델
│   │   ├── ncf_model.pth                    # NCF 모델 (FP32)
│   │   ├── ncf_model_best
│   │   └── ncf_model_int8.pth               # NCF 모델 (INT8)
│   │
│   └── reports/                    # 분석 보고서
│       ├── data_summary.csv                 # 데이터셋 요약
│       ├── baseline_results.csv             # Baseline 성능
│       ├── ncf_training_results.csv         # NCF 학습 결과
│       ├── quantization_results.csv         # 양자화 결과
│       ├── project_summary.csv              # 프로젝트 요약
│       └── Final_Report.md                  # 최종 보고서
│
├── README.md                       # 프로젝트 문서 

```

---

## 기술 스택

### 핵심 라이브러리
- **PyTorch 2.0+**: 딥러닝 프레임워크 (NCF 모델)
- **scikit-learn**: 머신러닝 (Baseline 모델)
- **pandas, numpy**: 데이터 분석 및 처리
- **SQLite**: 구조화된 데이터 관리

### 보조 라이브러리
- **matplotlib, seaborn**: 데이터 시각화
- **scipy**: 희소 행렬 처리 (협업 필터링)

---

## 모델 성능

### 전체 모델 비교

| 모델 | RMSE | MAE | 크기 (MB) | 특징 |
|------|------|-----|-----------|------|
| **PyTorch NCF** | **1.1071** | **0.8265** | 25.97 | 최고 정확도 |
| NCF INT8 | 1.1077 | 0.8268 | 25.90 | 거의 손실 없음 |
| User + Game Bias | 1.1960 | 0.9041 | - | 최고 Baseline |
| **NCF 2-bit** | **1.3302** | **1.0145** | **1.72** | 극도로 경량화 |

### 성능 지표
- **최고 정확도**: PyTorch NCF (RMSE 1.1071)
- **Baseline 대비 개선**: 7.43%
- **2-bit 양자화**: 93.4% 크기 감소
- **INT8 정확도 유지**: 99.95% (거의 손실 없음)

---

## 주요 특징

### 1. 대규모 데이터 처리
- **1,894만 개** 평점 데이터
- **93,637명** 사용자
- **12,302개** 게임
- **98.98%** 희소성 (Sparse Matrix)

### 2. 협업 필터링 (Baseline 모델)
- Global Average
- User Average
- Game Average
- User + Game Bias
- NMF (Non-negative Matrix Factorization)

### 3. 딥러닝 추천 시스템 (NCF)
- **구조**: Neural Collaborative Filtering
- **User Embedding**: 93,637 x 64 차원
- **Game Embedding**: 12,302 x 64 차원
- **MLP 레이어**: [128, 64, 32]
- **총 파라미터**: 6,806,977개

### 4. 모델 경량화 기술
- **INT8 Dynamic Quantization**: PyTorch 내장 기능 활용
- **2-bit Quantization**: 커스텀 구현 (Embedding 전용)
- **Scale/Zero-point 방식**: 정확도 보존

---

## 설치 및 실행

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/your-repo/boardgame-recommendation.git
cd boardgame-recommendation

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터 준비

```bash
# data/ 폴더에 CSV 파일 배치
# - games.csv
# - user_ratings.csv
# - ratings_distribution.csv
# - mechanics.csv
```

### 3. Jupyter 실행

```bash
jupyter notebook
```

### 4. 순서대로 실행

```
01_EDA_Final.ipynb
  → 02_Baseline_Models.ipynb
  → 03_Deep_Learning.ipynb
  → 04_Quantization.ipynb
  → 05_Evaluation.ipynb
```

---

## 데이터 분석 결과

### SQL 분석 (5개 쿼리)
1. **사용자 활동 분석**: 가장 활발한 사용자 Top 20
2. **게임 인기도 분석**: 가장 인기있는 게임 Top 20
3. **평점 분포 분석**: 평점 범위별 분포
4. **데이터 희소성 분석**: 행렬의 밀도 및 희소성
5. **사용자 세분화**: 사용자를 4개 그룹으로 분류

### 주요 발견사항
- **Power User** (11.8%): 100개 이상 평가
- **Active User** (11.0%): 50-100개 평가
- **Regular User** (31.8%): 10-50개 평가
- **Casual User** (45.4%): 10개 이하 평가

---

## 모델 결과

### Baseline 모델 성능

| 모델 | RMSE | MAE | 특징 |
|------|------|-----|------|
| Global Average | 1.3856 | 1.0523 | 기본 베이스라인 |
| User Average | 1.2574 | 0.9481 | 사용자 선호도 반영 |
| Game Average | 1.2384 | 0.9348 | 게임 평가 반영 |
| **User + Game Bias** | **1.1960** | **0.9041** | 최고 Baseline |
| NMF (k=50) | 1.2156 | 0.9154 | 잠재 요인 분석 |

### PyTorch NCF 성능

| 항목 | 값 |
|------|-----|
| 학습 Epochs | 10 |
| 최종 RMSE | 1.1071 |
| 최종 MAE | 0.8265 |
| Baseline 대비 개선 | 7.43% |

---

## 코드 예제

### 1. EDA 및 SQL 분석

```python
# SQL 쿼리 - 사용자 활동 분석
SELECT Username as user_id, 
       COUNT(*) as total_ratings,
       ROUND(AVG(Rating), 2) as avg_rating
FROM user_ratings
GROUP BY Username
HAVING total_ratings >= 50
ORDER BY total_ratings DESC
LIMIT 20
```

### 2. Baseline 모델 학습

```python
from sklearn.decomposition import NMF
from scipy.sparse import csr_matrix

# NMF 모델 생성 및 학습
nmf_model = NMF(n_components=50, max_iter=200)
W = nmf_model.fit_transform(train_matrix)
H = nmf_model.components_

# 예측
predicted_ratings = np.dot(W, H)
```

### 3. NCF 모델 학습

```python
import torch
import torch.nn as nn

# 모델 정의
model = NCF(n_users=93637, n_games=12302, 
            embedding_dim=64, 
            hidden_layers=[128, 64, 32])

# 학습
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

for epoch in range(10):
    # 학습 루프
    pass
```

### 4. 2-bit 양자화

```python
# Embedding 양자화
class ImprovedQuantize2bit(nn.Module):
    def __init__(self, original_model):
        super().__init__()
        # Embedding weights를 2-bit로 양자화
        self.user_emb_q, scale, zero_point = self._quantize_embedding(
            original_model.user_embedding.weight
        )
```

---

## 성과 요약

### 기술적 성과
- PyTorch를 활용한 **Neural Collaborative Filtering** 구현
- **2-bit 양자화**로 모델 크기 93.4% 감소
- **SQL 기반** 대규모 데이터 분석 (5개 쿼리)

### 비즈니스 임팩트
- **모바일 배포 가능**: 1.72 MB 경량화 모델
- **실시간 추천**: 빠른 추론 속도 (INT8)
- **확장성**: 새로운 사용자/게임 추가 용이

---

## 시스템 요구사항

### 최소 사양
- **OS**: Windows, macOS, Linux
- **Python**: 3.9 이상
- **RAM**: 16GB 이상 (데이터 로드용)
- **저장공간**: 5GB 이상

### 권장 사양
- **GPU**: CUDA 지원 (Optional, NCF 학습 속도 향상)
- **RAM**: 32GB
- **SSD 저장공간**: 10GB

---

## 파일 설명

### Notebook 파일

**01_EDA_Final.ipynb**
- 탐색적 데이터 분석 (EDA)
- SQL 쿼리 (5개)
- 데이터 시각화 (4개 그래프)

**02_Baseline_Models.ipynb**
- 5개 Baseline 모델 구현
- 모델 성능 비교
- 시각화 (2개 그래프)

**03_Deep_Learning.ipynb**
- PyTorch NCF 모델 정의
- 10 Epochs 학습
- 학습 곡선 및 예측 시각화 (2개 그래프)

**04_Quantization.ipynb**
- INT8 양자화
- 2-bit 양자화 (커스텀)
- 성능 비교 (1개 그래프)

**05_Evaluation.ipynb**
- 전체 모델 성능 종합 평가
- Trade-off 분석
- 최종 보고서 생성 (3개 그래프)

---

## 시각화 결과

### 10개 그래프
1. **평점 분포**: 히스토그램 + 박스플롯
2. **데이터 희소성**: 바 차트 + 파이 차트
3. **Baseline 비교**: RMSE/MAE 비교
4. **예측 성능**: 산점도
5. **NCF 학습**: 손실/RMSE/MAE 곡선
6. **NCF 예측**: 산점도
7. **양자화 비교**: 4개 서브플롯
8. **전체 모델 비교**: 수평 바 차트
9. **Trade-off 분석**: 로그 스케일 산점도
10. **학습 곡선**: 최종 성능 곡선

---

## 커스텀 구현

### 2-bit 양자화 알고리즘
```
1. Min-max scaling으로 4 레벨 (0, 1, 2, 3)로 매핑
2. Per-tensor scale과 zero-point 저장
3. Embedding만 양자화 (전체 파라미터의 99.6%)
4. FC layers는 FP32 유지 (정확도 보존)

결과: 93.4% 크기 감소, RMSE 손실 +0.22 (트레이드오프)
```

---

## 라이선스

MIT License

---

## 참고사항

### 데이터 출처
- BoardGameGeek (BGG) 데이터셋
- 1,894만 개 사용자 평점




