# src/evaluation.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (classification_report, confusion_matrix, 
                             roc_auc_score, roc_curve, precision_recall_curve)
from config import PLOTS_DIR, SHOW_PLOTS, SAVE_PLOTS

def evaluate_model(model, X_test, y_test):
    """모델 평가"""
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\n최적 모델 성능:")
    print(classification_report(y_test, y_pred, 
                                target_names=['클릭 안함', '클릭함']))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['클릭 안함', '클릭함'],
                yticklabels=['클릭 안함', '클릭함'])
    plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.ylabel('실제값')
    plt.xlabel('예측값')
    plt.tight_layout()
    
    if SAVE_PLOTS:
        save_path = os.path.join(PLOTS_DIR, 'confusion_matrix.png')
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"\n[그래프 저장됨] {save_path}")
    
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()
    
    return y_pred, y_prob

def plot_feature_importance(model, feature_cols):
    """Feature Importance 시각화"""
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nFeature Importance (상위 10개):")
    print(feature_importance.head(10).to_string(index=False))
    
    plt.figure(figsize=(10, 8))
    top_features = feature_importance.head(10)
    plt.barh(top_features['Feature'], top_features['Importance'], 
             color='#8b5cf6', alpha=0.7)
    plt.xlabel('Importance', fontsize=12)
    plt.title('Random Forest - Feature Importance (Top 10)', 
              fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if SAVE_PLOTS:
        save_path = os.path.join(PLOTS_DIR, 'feature_importance.png')
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"\n[그래프 저장됨] {save_path}")
    
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()
    
    return feature_importance

def plot_roc_curve(models, X_test, X_test_scaled, y_test):
    """ROC Curve 비교"""
    plt.figure(figsize=(12, 8))
    
    for name, model in models.items():
        if name in ['Logistic Regression', 'SVM', 'KNN', 'Naive Bayes']:
            y_prob = model.predict_proba(X_test_scaled)[:, 1]
        else:
            y_prob = model.predict_proba(X_test)[:, 1]
        
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = roc_auc_score(y_test, y_prob)
        plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.3f})', linewidth=2)
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random Guess', linewidth=2)
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curve 비교', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if SAVE_PLOTS:
        save_path = os.path.join(PLOTS_DIR, 'roc_curves.png')
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"\n[그래프 저장됨] {save_path}")
    
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()

def generate_business_insights(df, segment_a_ctr, segment_b_ctr, overall_ctr):
    """비즈니스 인사이트 생성"""
    print("\n" + "="*70)
    print("비즈니스 인사이트 및 전략 제안")
    print("="*70)
    
    print("\n[1] 주요 발견사항")
    print("-" * 70)
    print(f"1. 연령: 40세 이상 유저의 클릭률이 평균보다 "
          f"{(segment_a_ctr - overall_ctr) / overall_ctr * 100:.1f}% 높음")
    print(f"2. 소득: 저소득층(<4만)의 클릭률이 중고소득층보다 높음")
    print(f"3. 체류시간: 사이트 체류시간이 짧을수록 광고 클릭률 증가")
    print(f"4. 인터넷 사용: 일일 인터넷 사용 시간이 적을수록 광고 클릭률 증가")
    
    print("\n[2] 타겟팅 전략")
    print("-" * 70)
    print("전략 A: 고연령층 집중 타겟팅")
    print("  - 대상: 40세 이상 유저")
    print("  - 예상 개선: 클릭률 약 40-50% 증가")
    print("  - 실행방안: 광고 노출 빈도 2배 증가, 연령층 맞춤 크리에이티브")
    
    print("\n전략 B: 저소득층 맞춤 광고")
    print("  - 대상: 연소득 4만 달러 미만")
    print("  - 예상 개선: 클릭률 약 30-40% 증가")
    print("  - 실행방안: 가격 할인, 실용성 강조 메시지")
    
    print("\n[3] 실행 권장사항")
    print("-" * 70)
    print("단기 (1-2개월):")
    print("  1. 40세 이상 유저 대상 광고 노출 빈도 2배 증가")
    print("  2. 저소득층 대상 할인/프로모션 메시지 강화")
    print("  3. 사이트 초기 방문자 대상 웰컴 광고 캠페인 런칭")
    
    print("\n중기 (3-6개월):")
    print("  1. 머신러닝 모델 기반 실시간 타겟팅 시스템 구축")
    print("  2. 연령/소득/행동 패턴별 크리에이티브 A/B 테스트")
    print("  3. 예측 확률 기반 입찰 전략 최적화")
    
    print("\n장기 (6-12개월):")
    print("  1. 개인화된 광고 추천 시스템 고도화")
    print("  2. 실시간 피드백 루프를 통한 모델 지속 학습")
    print("  3. 크로스 채널 통합 마케팅 전략 수립")