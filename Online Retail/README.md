# Online Retail 

Online Retail 고객 행동 분석 프로젝트

### 프로젝트 개요

Online Retail Dataset(UCI)을 기반으로 고객 구매 행동을 분석하고 매출 인사이트를 도출하는 것을 목표로 합니다.
Python을 활용해 대규모 원본 데이터를 전처리
MySQL에 적재하고, SQL 분석으로 모든 지표를 생성

### 기술 스택
Language: Python (Pandas)
Database: MySQL
ETL Interface: SQLAlchemy 기본 연결 (자동 파이프라인 구성 없음)
Analysis: 모든 분석은 MySQL SQL 스크립트로 수행

### 데이터 전처리

CustomerID → 숫자 변환
InvoiceDate → datetime 변환
Description 결측치 → ‘Unknown Product’
TotalPrice = Quantity × UnitPrice 생성
InvoiceNo가 ‘C’로 시작하면 IsCancelled = 1
데이터 품질 검사(행 수, 고객 수, 날짜 범위)

```python

file_path = r"...data\Online Retail.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)

df['CustomerID'] = pd.to_numeric(df['CustomerID'], errors='coerce')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
df['Description'] = df['Description'].fillna('Unknown Product')
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['IsCancelled'] = df['InvoiceNo'].str.startswith('C', na=False).astype(int)

```

### 데이터베이스 적재
데이터베이스(MySQL) 적재

```python
df.to_sql("online_retail", engine, index=False, if_exists="append")
```

#### 포함된 주요 분석 항목
전체 거래 수
총 매출
고객별 매출
국가별 매출
취소 거래 비율
월별 매출 추이
시간대별 구매량
날짜별 고객수
반복 구매 고객 세그먼트
매출 상위 고객
특정 날짜 최고 판매 상품
시간대별 매출 세그먼트