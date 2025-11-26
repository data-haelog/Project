import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from config import DATA_PATH

def load_data(file_path=DATA_PATH):
    try:
        df = pd.read_csv(file_path)
        print(f"데이터 로드 성공: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"파일을 찾을 수 없음: {file_path}")
        raise

def get_data_info(df):
    print(f"데이터 크기: {df.shape}")
    print(f"결측치: {df.isnull().sum().sum()}개")
    print(f"전체 클릭률(CTR): {df['Clicked on Ad'].mean():.2%}")
    print(f"클래스 분포: {df['Clicked on Ad'].value_counts().to_dict()}")
    print(f"\n컬럼: {df.columns.tolist()}")
    print(f"\n기술 통계량:\n{df.describe()}")
    
    return {
        'shape': df.shape,
        'missing_values': df.isnull().sum().sum(),
        'ctr': df['Clicked on Ad'].mean(),
        'class_distribution': df['Clicked on Ad'].value_counts().to_dict()
    }