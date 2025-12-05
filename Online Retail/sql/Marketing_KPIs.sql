/******************************************************************
제품 클릭 행동 기반 마케팅 인사이트 분석
******************************************************************/

USE ecommerce_db;

-- 1. 전체 총 거래 수
SELECT COUNT(*) AS total_transactions 
FROM online_retail;

-- 2. 총 매출
SELECT SUM(TotalPrice) AS total_revenue 
FROM online_retail;

-- 3. 고객별 총 매출
SELECT CustomerID, SUM(TotalPrice) AS customer_revenue
FROM online_retail
GROUP BY CustomerID
ORDER BY customer_revenue DESC;

-- 4. 국가별 총 매출
SELECT Country, SUM(TotalPrice) AS country_revenue
FROM online_retail
GROUP BY Country
ORDER BY country_revenue DESC;

-- 5. 취소 거래 수
SELECT SUM(IsCancelled) AS total_cancellations 
FROM online_retail;

-- 6. 월별 매출
SELECT DATE_FORMAT(InvoiceDate, '%Y-%m') AS month, SUM(TotalPrice) AS month_revenue
FROM online_retail
GROUP BY month
ORDER BY month;

-- 7. 시간대별 구매 수
SELECT HOUR(InvoiceDate) AS hour, SUM(Quantity) AS total_quantity
FROM online_retail
GROUP BY hour
ORDER BY hour;

-- 8. 날짜별 고객 수
SELECT DATE(InvoiceDate) AS day, COUNT(DISTINCT CustomerID) AS unique_customers
FROM online_retail
GROUP BY day
ORDER BY day;

-- 11. 고객별 총 매출과 구매횟수
WITH customer_summary AS (
    SELECT CustomerID,
           COUNT(DISTINCT InvoiceNo) AS purchase_count,
           SUM(TotalPrice) AS total_revenue
    FROM online_retail
    GROUP BY CustomerID
)
SELECT *,
       CASE WHEN purchase_count > 1 
       THEN 'Repeat' 
       ELSE 'One-time' 
       END AS customer_type
FROM customer_summary
ORDER BY total_revenue DESC;

-- 12. 월별 총 매출 + 고객 수
WITH monthly_summary AS (
    SELECT DATE_FORMAT(InvoiceDate, '%Y-%m') AS month,
           SUM(TotalPrice) AS month_revenue,
           COUNT(DISTINCT CustomerID) AS num_customers
    FROM online_retail
    GROUP BY month
)
SELECT *,
       ROUND(month_revenue/num_customers,2) AS avg_per_customer
FROM monthly_summary
ORDER BY month;

-- 13. 매출 상위 5명의 고객
SELECT CustomerID, total_revenue
FROM (
    SELECT CustomerID, SUM(TotalPrice) AS total_revenue
    FROM online_retail
    GROUP BY CustomerID
) AS sub
ORDER BY total_revenue DESC
LIMIT 5;

-- 14. 하루에 가장 많이 팔린 상품
SELECT StockCode, SUM(Quantity) AS total_quantity
FROM online_retail
WHERE DATE(InvoiceDate) = '2010-12-01'
GROUP BY StockCode
ORDER BY total_quantity DESC
LIMIT 1;

-- 15. 시간대별 구매 세그먼트
SELECT HOUR(InvoiceDate) AS hour,
       CASE
           WHEN HOUR(InvoiceDate) BETWEEN 0 AND 6 THEN 'Late Night'
           WHEN HOUR(InvoiceDate) BETWEEN 7 AND 12 THEN 'Morning'
           WHEN HOUR(InvoiceDate) BETWEEN 13 AND 18 THEN 'Afternoon'
           ELSE 'Evening'
       END AS time_segment,
       COUNT(*) AS num_transactions,
       SUM(TotalPrice) AS total_revenue
FROM online_retail
GROUP BY hour, time_segment
ORDER BY hour;

----------------------------------------------------------------------------------------

