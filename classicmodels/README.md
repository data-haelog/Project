## 📁 파일 구조
```
classicmodels-sql-analysis/
├── sql/
│   ├── 01_data_exploration_fundamentals.sql      # 데이터 탐색 및 기초 쿼리
│   ├── 02_customer_sales_analysis.sql            # 고객 및 매출 분석
│   └── 03_rfm_cohort_profitability_analysis.sql  # RFM, 코호트, 수익성 분석
└── docs/
    └── classicmodels_erd.png                     # 데이터베이스 ERD
```

## SQL 파일
####  01_data_exploration_fundamentals.sql
- 테이블 구조 및 레코드 수 확인
- SELECT, WHERE, ORDER BY, LIMIT
- 기본 집계 함수 (COUNT, SUM, AVG)
- INNER JOIN, LEFT JOIN
- LIKE 패턴 검색, DATE 함수

####  02_customer_sales_analysis.sql
- 고객별/국가별/제품별 매출 집계
- HAVING을 활용한 우수 고객 추출
- 서브쿼리 및 CTE 활용
- 신용한도별 고객 등급 분류 (CASE WHEN)
- 파레토 법칙 검증 (상위 20% 고객 매출 비중)
- 월별/연도별 매출 트렌드 분석

####  03_rfm_cohort_profitability_analysis.sql
- **RFM 분석**: 고객 세그먼테이션 (VIP, Loyal, At Risk, Regular)
- **코호트 분석**: 첫 구매 시점별 고객 그룹 재구매 패턴
- **재구매율 분석**: 구매 빈도별 고객 분포
- **수익성 분석**: 제품 라인별 이익률 계산
- **윈도우 함수**: 국가별 고객 랭킹 (RANK, PARTITION BY)
- **Funnel 분석**: 고객 이탈 지점 파악
- **장기 미구매 고객** 식별 및 리타겟팅 전략

