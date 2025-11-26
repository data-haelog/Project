# src/model_training.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score)
from config import RANDOM_STATE, TEST_SIZE, PARAM_GRID, CV_FOLDS

def prepare_data(df, feature_cols):
    """데이터 전처리 및 분할"""
    print("\n" + "="*70)
    print("데이터 전처리")
    print("="*70)
    
    X = df[feature_cols]
    y = df['Clicked on Ad']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    print(f"\nTrain 데이터: {X_train.shape}")
    print(f"Test 데이터: {X_test.shape}")
    print(f"Train 클릭률: {y_train.mean():.2%}")
    print(f"Test 클릭률: {y_test.mean():.2%}")
    
    # 스케일링
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler

def train_models(X_train, X_test, y_train, y_test, 
                 X_train_scaled, X_test_scaled):
    """여러 모델 학습 및 비교"""
    print("\n" + "="*70)
    print("머신러닝 모델 학습 및 비교")
    print("="*70)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=RANDOM_STATE, 
                                                   max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=RANDOM_STATE, 
                                                 max_depth=10),
        'Random Forest': RandomForestClassifier(n_estimators=100, 
                                                random_state=RANDOM_STATE, 
                                                max_depth=10),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, 
                                                         random_state=RANDOM_STATE, 
                                                         max_depth=5),
        'SVM': SVC(probability=True, random_state=RANDOM_STATE),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB()
    }
    
    results = []
    trained_models = {}
    
    for name, model in models.items():
        if name in ['Logistic Regression', 'SVM', 'KNN', 'Naive Bayes']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_prob = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        
        results.append({
            'Model': name,
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'ROC-AUC': roc_auc
        })
        
        trained_models[name] = model
        
        print(f"\n{name}:")
        print(f"  Accuracy: {accuracy:.4f} | Precision: {precision:.4f} | "
              f"Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f} | ROC-AUC: {roc_auc:.4f}")
    
    results_df = pd.DataFrame(results).sort_values('ROC-AUC', ascending=False)
    
    print("\n" + "="*70)
    print("모델 성능 비교 (ROC-AUC 기준 정렬)")
    print("="*70)
    print(results_df.to_string(index=False))
    
    return results_df, trained_models

def optimize_random_forest(X_train, y_train):
    """Random Forest 하이퍼파라미터 튜닝"""
    print("\n" + "="*70)
    print("Random Forest 하이퍼파라미터 튜닝 (GridSearchCV)")
    print("="*70)
    
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=RANDOM_STATE),
        PARAM_GRID,
        cv=CV_FOLDS,
        scoring='roc_auc',
        n_jobs=-1,
        verbose=1
    )
    
    rf_grid.fit(X_train, y_train)
    
    print(f"\n최적 파라미터: {rf_grid.best_params_}")
    print(f"최적 ROC-AUC (CV): {rf_grid.best_score_:.4f}")
    
    return rf_grid.best_estimator_