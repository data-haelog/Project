# main.py
# -*- coding: utf-8 -*-
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_data, get_data_info
from src.eda import (plot_target_distribution, analyze_numeric_features,
                     segment_analysis, correlation_analysis)
from src.feature_engineering import create_features, get_feature_columns
from src.model_training import prepare_data, train_models, optimize_random_forest
from src.evaluation import (evaluate_model, plot_feature_importance,
                            plot_roc_curve, generate_business_insights)
from config import SEGMENT_AGE_THRESHOLD, SEGMENT_TIME_THRESHOLD

def main():
    """메인 실행 함수"""
    
    print("="*70)
    print("광고 클릭 분석 및 예측 모델 실행")
    print("="*70)
    
    # 1. 데이터 로드
    print("\n[Step 1/11] 데이터 로드")
    print("-" * 70)
    df = load_data()
    info = get_data_info(df)
    
    # 2. EDA - 타겟 변수 분포
    print("\n[Step 2/11] 타겟 변수 분포 분석")
    print("-" * 70)
    plot_target_distribution(df)
    
    # 3. 수치형 변수 분석
    print("\n[Step 3/11] 수치형 변수 분석")
    print("-" * 70)
    analyze_numeric_features(df)
    
    # 4. 세그먼트 분석
    print("\n[Step 4/11] 세그먼트 분석")
    print("-" * 70)
    age_click, income_click = segment_analysis(df)
    
    # 5. 상관관계 분석
    print("\n[Step 5/11] 상관관계 분석")
    print("-" * 70)
    correlation_analysis(df)
    
    # 6. Feature Engineering
    print("\n[Step 6/11] Feature Engineering")
    print("-" * 70)
    df = create_features(df)
    feature_cols = get_feature_columns()
    
    # 7. 세그먼트 정의 및 CTR 계산
    print("\n[Step 7/11] 타겟 세그먼트 정의")
    print("-" * 70)
    segment_a = df[(df['Age'] >= SEGMENT_AGE_THRESHOLD) & 
                   (df['Daily Time Spent on Site'] <= SEGMENT_TIME_THRESHOLD)]
    segment_a_ctr = segment_a['Clicked on Ad'].mean()
    
    segment_b = df[(df['Area Income'] <= 40000) & 
                   (df['Daily Internet Usage'] <= 180)]
    segment_b_ctr = segment_b['Clicked on Ad'].mean()
    
    overall_ctr = df['Clicked on Ad'].mean()
    
    print(f"전체 클릭률(CTR): {overall_ctr:.2%}")
    print(f"세그먼트 A (40세+ & 체류시간 <=60분):")
    print(f"  - 표본 수: {len(segment_a)}명")
    print(f"  - 클릭률: {segment_a_ctr:.2%}")
    print(f"  - 개선율: +{(segment_a_ctr - overall_ctr) / overall_ctr * 100:.1f}%")
    
    print(f"\n세그먼트 B (저소득 & 인터넷 사용 <=180분):")
    print(f"  - 표본 수: {len(segment_b)}명")
    print(f"  - 클릭률: {segment_b_ctr:.2%}")
    print(f"  - 개선율: +{(segment_b_ctr - overall_ctr) / overall_ctr * 100:.1f}%")
    
    # 8. 데이터 준비
    print("\n[Step 8/11] 데이터 전처리 및 분할")
    print("-" * 70)
    X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler = \
        prepare_data(df, feature_cols)
    
    # 9. 모델 학습
    print("\n[Step 9/11] 모델 학습 및 비교")
    print("-" * 70)
    results_df, trained_models = train_models(
        X_train, X_test, y_train, y_test,
        X_train_scaled, X_test_scaled
    )
    
    # 10. Random Forest 최적화
    print("\n[Step 10/11] Random Forest 하이퍼파라미터 최적화")
    print("-" * 70)
    best_rf = optimize_random_forest(X_train, y_train)
    
    # 11. 모델 평가
    print("\n[Step 11/11] 최적 모델 평가")
    print("-" * 70)
    y_pred, y_prob = evaluate_model(best_rf, X_test, y_test)
    
    # Feature Importance
    print("\n" + "="*70)
    print("Feature Importance 분석")
    print("="*70)
    feature_importance = plot_feature_importance(best_rf, feature_cols)
    
    # ROC Curve
    print("\n" + "="*70)
    print("ROC Curve 생성")
    print("="*70)
    plot_roc_curve(trained_models, X_test, X_test_scaled, y_test)
    
    # 비즈니스 인사이트
    generate_business_insights(df, segment_a_ctr, segment_b_ctr, overall_ctr)
    
    # 최종 요약
    print("\n" + "="*70)
    print("분석 완료!")
    print("="*70)
    
    best_model_name = results_df.iloc[0]['Model']
    best_roc_auc = results_df.iloc[0]['ROC-AUC']
    best_accuracy = results_df.iloc[0]['Accuracy']
    
    print(f"\n[최종 결과 요약]")
    print(f"  - 전체 데이터: {df.shape[0]:,}개")
    print(f"  - 전체 클릭률: {overall_ctr:.2%}")
    print(f"  - 최고 성능 모델: {best_model_name}")
    print(f"  - 모델 정확도: {best_accuracy:.2%}")
    print(f"  - ROC-AUC: {best_roc_auc:.4f}")
    
    print(f"\n[출력 파일]")
    output_path = os.path.abspath('output/plots/')
    print(f"  저장 위치: {output_path}")
    
    try:
        plot_files = sorted(os.listdir('output/plots/'))
        if plot_files:
            print(f"  생성된 그래프 ({len(plot_files)}개):")
            for i, file in enumerate(plot_files, 1):
                print(f"    {i}. {file}")
        else:
            print("  생성된 그래프가 없습니다.")
    except FileNotFoundError:
        print("  output/plots 폴더를 찾을 수 없습니다.")
    
    print("\n" + "="*70)
    print("프로그램 종료")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[오류 발생] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)