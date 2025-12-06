USE ecommerce_db;

-- 상품 취소율
SELECT StockCode,
       COUNT(*) AS total_orders,
       SUM(IsCancelled) AS cancelled_orders,
       ROUND(SUM(IsCancelled) / COUNT(*) * 100, 2) AS cancel_rate_pct
FROM online_retail
GROUP BY StockCode
ORDER BY cancel_rate_pct DESC;

-- 고객별 취소율
SELECT CustomerID,
       COUNT(*) AS total_orders,
       SUM(IsCancelled) AS cancelled_orders,
       ROUND(SUM(IsCancelled) / COUNT(*) * 100, 2) AS cancel_rate_pct
FROM online_retail
GROUP BY CustomerID
HAVING total_orders > 5
ORDER BY cancel_rate_pct DESC;

-- Top 5 상품의 월별 매출
WITH top5 AS (
    SELECT StockCode
    FROM (
        SELECT StockCode, SUM(TotalPrice) AS revenue
        FROM online_retail
        GROUP BY StockCode
        ORDER BY revenue DESC
        LIMIT 5
    ) t
)
SELECT DATE_FORMAT(InvoiceDate, '%Y-%m') AS month,
       StockCode,
       SUM(TotalPrice) AS revenue
FROM online_retail
WHERE StockCode IN (SELECT StockCode FROM top5)
GROUP BY month, StockCode
ORDER BY month, revenue DESC;

-- 평균 장바구니 크기(Basket Size)
SELECT CustomerID,
       AVG(quantity_sum) AS avg_basket_size
FROM (
    SELECT CustomerID, InvoiceNo, SUM(Quantity) AS quantity_sum
    FROM online_retail
    GROUP BY CustomerID, InvoiceNo
) sub
GROUP BY CustomerID
ORDER BY avg_basket_size DESC;

-- 고객별 평균 구매 금액
SELECT CustomerID,
       ROUND(AVG(order_value),2) AS avg_order_value
FROM (
    SELECT CustomerID, InvoiceNo, SUM(TotalPrice) AS order_value
    FROM online_retail
    GROUP BY CustomerID, InvoiceNo
) t
GROUP BY CustomerID
ORDER BY avg_order_value DESC;

-- 요일별 매출 
SELECT DAYNAME(InvoiceDate) AS weekday,
       SUM(TotalPrice) AS revenue
FROM online_retail
GROUP BY weekday
ORDER BY revenue DESC;

-- 시간대·요일 조합 매출 테이블
SELECT DAYNAME(InvoiceDate) AS weekday,
       HOUR(InvoiceDate) AS hour,
       SUM(TotalPrice) AS revenue
FROM online_retail
GROUP BY weekday, hour
ORDER BY weekday, hour;

-- 고가 제품과 저가 제품 매출 구간 분석
SELECT
    CASE
        WHEN UnitPrice < 5 THEN 'Low Price'
        WHEN UnitPrice BETWEEN 5 AND 20 THEN 'Mid Price'
        ELSE 'High Price'
    END AS price_segment,
    SUM(TotalPrice) AS revenue
FROM online_retail
GROUP BY price_segment
ORDER BY revenue DESC;

-- 신규 고객 vs 기존 고객 월별 매출
WITH first_purchase AS (
    SELECT CustomerID, MIN(DATE(InvoiceDate)) AS first_day
    FROM online_retail
    GROUP BY CustomerID
)
SELECT DATE_FORMAT(r.InvoiceDate, '%Y-%m') AS month,
       CASE WHEN DATE(r.InvoiceDate) = f.first_day THEN 'New' ELSE 'Existing' END AS customer_type,
       SUM(TotalPrice) AS revenue
FROM online_retail r
JOIN first_purchase f USING(CustomerID)
GROUP BY month, customer_type
ORDER BY month;
