# src/feature_engineering.py
import pandas as pd
import numpy as np

def create_features(df):
    """
    파생 변수 생성
    
    Parameters:
    -----------
    df : DataFrame
        원본 데이터프레임
        
    Returns:
    --------
    df : DataFrame
        파생 변수가 추가된 데이터프레임
    """
    print("\n" + "="*70)
    print("Feature Engineering")
    print("="*70)
    
    # 파생 변수 생성
    df['Engagement_Score'] = (df['Daily Time Spent on Site'] + 
                               df['Daily Internet Usage']) / 2
    
    df['Ad_Affinity_Score'] = (df['Age'] * 0.3) - \
                               (df['Daily Time Spent on Site'] * 0.4) - \
                               (df['Area Income'] / 1000 * 0.3)
    
    df['Income_Age_Ratio'] = df['Area Income'] / df['Age']
    
    df['Low_Engagement_High_Age'] = (
        (df['Age'] >= 40) & 
        (df['Daily Time Spent on Site'] <= 60)
    ).astype(int)
    
    df['Time_Income_Interaction'] = (df['Daily Time Spent on Site'] * 
                                      df['Area Income'] / 1000000)
    
    df['Age_Squared'] = df['Age'] ** 2
    df['Is_Senior'] = (df['Age'] >= 50).astype(int)
    df['Is_Low_Income'] = (df['Area Income'] < 40000).astype(int)
    df['High_Usage'] = (df['Daily Internet Usage'] > 
                         df['Daily Internet Usage'].median()).astype(int)
    
    print("\n생성된 파생변수 (9개):")
    print("1. Engagement_Score | 2. Ad_Affinity_Score | 3. Income_Age_Ratio")
    print("4. Low_Engagement_High_Age | 5. Time_Income_Interaction | 6. Age_Squared")
    print("7. Is_Senior | 8. Is_Low_Income | 9. High_Usage")
    
    return df

def get_feature_columns():
    """학습에 사용할 피처 컬럼 반환"""
    return [
        'Daily Time Spent on Site', 'Age', 'Area Income', 
        'Daily Internet Usage', 'Male', 'Engagement_Score', 
        'Income_Age_Ratio', 'Low_Engagement_High_Age',
        'Time_Income_Interaction', 'Age_Squared', 'Is_Senior',
        'Is_Low_Income', 'High_Usage'
    ]