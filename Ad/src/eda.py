# src/eda.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
from config import PLOTS_DIR, SHOW_PLOTS, SAVE_PLOTS

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def plot_target_distribution(df):
    """타겟 변수 분포 시각화"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    df['Clicked on Ad'].value_counts().plot(kind='bar', ax=axes[0], 
                                             color=['#3b82f6', '#10b981'])
    axes[0].set_title('광고 클릭 여부 분포', fontsize=14, fontweight='bold')
    axes[0].set_xticklabels(['클릭 안함', '클릭함'], rotation=0)
    axes[0].set_ylabel('빈도')
    
    df['Clicked on Ad'].value_counts().plot(kind='pie', ax=axes[1], 
                                             autopct='%1.1f%%',
                                             colors=['#3b82f6', '#10b981'], 
                                             startangle=90)
    axes[1].set_title('클릭률 비율', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('')
    
    plt.tight_layout()
    
    if SAVE_PLOTS:
        save_path = os.path.join(PLOTS_DIR, 'target_distribution.png')
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"  저장됨: {save_path}")
    
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()

def analyze_numeric_features(df):
    """수치형 변수와 타겟의 관계 분석"""
    print("주요 변수와 클릭 여부의 관계 (t-test)")
    
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    numeric_cols = ['Daily Time Spent on Site', 'Age', 
                    'Area Income', 'Daily Internet Usage']
    
    results = {}
    
    for i, col in enumerate(numeric_cols):
        row, col_idx = i // 2, i % 2
        
        axes[row, col_idx].boxplot([df[df['Clicked on Ad']==0][col],
                                     df[df['Clicked on Ad']==1][col]],
                                    labels=['클릭 안함', '클릭함'])
        axes[row, col_idx].set_title(col, fontsize=12, fontweight='bold')
        axes[row, col_idx].set_ylabel('값')
        
        t_stat, p_value = stats.ttest_ind(
            df[df['Clicked on Ad']==0][col],
            df[df['Clicked on Ad']==1][col]
        )
        
        results[col] = {'t_stat': t_stat, 'p_value': p_value}
        
        print(f"{col:30s} | t-stat: {t_stat:8.3f} | "
              f"p-value: {p_value:.4f} {'***' if p_value < 0.001 else ''}")
    
    plt.tight_layout()
    
    if SAVE_PLOTS:
        save_path = os.path.join(PLOTS_DIR, 'numeric_features_analysis.png')
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"\n[그래프 저장됨] {save_path}")
    
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()
    
    return results

def segment_analysis(df):
    """ 고효율 타겟 세그먼트 분석"""
    
    # 연령대별 분석
    df['Age_Group'] = pd.cut(df['Age'], 
                              bins=[0, 25, 35, 45, 55, 100], 
                              labels=['18-25', '26-35', '36-45', '46-55', '56+'])
    age_click = df.groupby('Age_Group')['Clicked on Ad'].agg(['mean', 'count']).reset_index()
    age_click.columns = ['Age_Group', 'Click_Rate', 'Count']
    
    print("\n연령대별 클릭률:")
    print(age_click.to_string(index=False))
    
    # 소득 구간별 분석
    df['Income_Group'] = pd.cut(df['Area Income'], 
                                  bins=[0, 40000, 60000, 100000], 
                                  labels=['저소득(<4만)', '중소득(4-6만)', '고소득(>6만)'])
    income_click = df.groupby('Income_Group')['Clicked on Ad'].agg(['mean', 'count']).reset_index()
    income_click.columns = ['Income_Group', 'Click_Rate', 'Count']
    
    print("\n소득 구간별 클릭률:")
    print(income_click.to_string(index=False))
    
    # 시각화
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    x_age = np.arange(len(age_click))
    axes[0].bar(x_age, age_click['Click_Rate'], color='#3b82f6', alpha=0.7)
    axes[0].set_xlabel('연령대', fontsize=12)
    axes[0].set_ylabel('클릭률', fontsize=12)
    axes[0].set_title('연령대별 클릭률', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x_age)
    axes[0].set_xticklabels(age_click['Age_Group'])
    for i, v in enumerate(age_click['Click_Rate']):
        axes[0].text(i, v + 0.02, f'{v:.1%}', ha='center', fontweight='bold')
    
    axes[1].bar(income_click['Income_Group'], income_click['Click_Rate'], 
                color=['#10b981', '#3b82f6', '#8b5cf6'], alpha=0.7)
    axes[1].set_xlabel('소득 구간', fontsize=12)
    axes[1].set_ylabel('클릭률', fontsize=12)
    axes[1].set_title('소득 구간별 클릭률', fontsize=14, fontweight='bold')
    for i, v in enumerate(income_click['Click_Rate']):
        axes[1].text(i, v + 0.02, f'{v:.1%}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    
    if SAVE_PLOTS:
        save_path = os.path.join(PLOTS_DIR, 'segment_analysis.png')
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"\n[그래프 저장됨] {save_path}")
    
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()
    
    return age_click, income_click

def correlation_analysis(df):
    """상관관계 분석"""
    corr_cols = ['Daily Time Spent on Site', 'Age', 'Area Income', 
                 'Daily Internet Usage', 'Male', 'Clicked on Ad']
    corr_matrix = df[corr_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, 
                cbar_kws={"shrink": 0.8})
    plt.title('변수 간 상관관계 히트맵', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if SAVE_PLOTS:
        save_path = os.path.join(PLOTS_DIR, 'correlation_matrix.png')
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"\n[그래프 저장됨] {save_path}")
    
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()
    
    target_corr = corr_matrix['Clicked on Ad'].sort_values(ascending=False)
    print("\n타겟 변수와의 상관관계:")
    print(target_corr)
    
    return corr_matrix