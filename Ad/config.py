# config.py
import os

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_PATH = os.path.join(DATA_DIR, 'advertising.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
PLOTS_DIR = os.path.join(OUTPUT_DIR, 'plots')

# 디렉토리 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# 실행 모드 설정
SHOW_PLOTS = False  
SAVE_PLOTS = True 

# 모델 파라미터
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# GridSearch 파라미터
PARAM_GRID = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# 세그먼트 정의
SEGMENT_AGE_THRESHOLD = 40
SEGMENT_TIME_THRESHOLD = 60
SEGMENT_INCOME_THRESHOLD = 40000
SEGMENT_INTERNET_THRESHOLD = 180

# 시각화 설정
PLOT_STYLE = 'whitegrid'
PLOT_PALETTE = 'Set2'
FIGURE_DPI = 100