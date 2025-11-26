USE classicmodels;

-- 2.1 주문 10건 이상 고객
-- 그룹 필터링으로 우수 고객 추출
SELECT 
    c.customerName,
    COUNT(o.orderNumber) AS order_count
FROM customers c
INNER JOIN orders o ON c.customerNumber = o.customerNumber
GROUP BY c.customerNumber, c.customerName
HAVING COUNT(o.orderNumber) >= 10
ORDER BY order_count DESC;

-- 2.2 연도별 매출 분석
-- 시계열 매출 트렌드 파악
SELECT 
    YEAR(o.orderDate) AS year,
    SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM orders o
INNER JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY YEAR(o.orderDate)
ORDER BY year;

-- 2.3 고객별 매출 Top 10
-- 매출 기여도 높은 핵심 고객 식별
SELECT 
    c.customerName,
    c.country,
    SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM customers c
INNER JOIN orders o ON c.customerNumber = o.customerNumber
INNER JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY c.customerNumber, c.customerName, c.country
ORDER BY total_sales DESC
LIMIT 10;

-- 2.4 제품별 주문 수 및 판매량
-- 인기 제품 분석
SELECT 
    p.productName,
    p.productLine,
    COUNT(DISTINCT od.orderNumber) AS order_count,
    SUM(od.quantityOrdered) AS total_quantity
FROM products p
INNER JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName, p.productLine
ORDER BY order_count DESC
LIMIT 10;

-- 2.5 국가별 고객 수 및 총 신용한도
-- 지역별 비즈니스 규모 파악
SELECT 
    country,
    COUNT(*) AS customer_count,
    SUM(creditLimit) AS total_credit,
    AVG(creditLimit) AS avg_credit
FROM customers
GROUP BY country
ORDER BY customer_count DESC;

-- 2.6 주문한 적 있는 고객만 조회
-- 서브쿼리를 활용한 필터링
SELECT customerName, city, country
FROM customers
WHERE customerNumber IN (
    SELECT DISTINCT customerNumber 
    FROM orders
);

-- 2.7 평균 이상 매출 고객
-- 서브쿼리로 평균 계산 후 비교
WITH customer_sales AS (
    SELECT c.customerName,
        SUM(od.quantityOrdered * od.priceEach) AS total_sales
    FROM customers c
    INNER JOIN orders o ON c.customerNumber = o.customerNumber
    INNER JOIN orderdetails od ON o.orderNumber = od.orderNumber
    GROUP BY c.customerNumber, c.customerName
)
SELECT customerName, total_sales
FROM customer_sales
WHERE total_sales > (SELECT AVG(total_sales) FROM customer_sales)
ORDER BY total_sales DESC;

-- 2.8 신용한도별 고객 등급 분류
-- 조건부 로직으로 세그먼트 생성
SELECT 
    customerName,
    creditLimit,
    CASE 
        WHEN creditLimit >= 100000 THEN 'Platinum'
        WHEN creditLimit >= 50000 THEN 'Gold'
        WHEN creditLimit >= 20000 THEN 'Silver'
        ELSE 'Bronze'
    END AS customer_tier
FROM customers
ORDER BY creditLimit DESC;

-- 2.9 다중 JOIN: 주문-고객-제품-제품라인
-- 목적: 4개 테이블 연결하여 종합 정보 조회
SELECT 
    o.orderNumber,
    c.customerName,
    p.productName,
    pl.productLine,
    od.quantityOrdered,
    od.priceEach
FROM orders o
INNER JOIN customers c ON o.customerNumber = c.customerNumber
INNER JOIN orderdetails od ON o.orderNumber = od.orderNumber
INNER JOIN products p ON od.productCode = p.productCode
INNER JOIN productlines pl ON p.productLine = pl.productLine
LIMIT 20;

-- 2.10 월별 매출 분석
-- 월별 판매 패턴 파악
SELECT 
    YEAR(orderDate) AS year,
    MONTH(orderDate) AS month,
    COUNT(*) AS order_count,
    SUM(od.quantityOrdered * od.priceEach) AS monthly_sales
FROM orders o
INNER JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY YEAR(orderDate), MONTH(orderDate)
ORDER BY year, month;

-- 2.11 COUNT DISTINCT: 제품 라인별 고유 고객 수
-- 제품 라인별 고객 다양성 분석
SELECT 
    pl.productLine,
    COUNT(DISTINCT o.customerNumber) AS unique_customers
FROM productlines pl
INNER JOIN products p ON pl.productLine = p.productLine
INNER JOIN orderdetails od ON p.productCode = od.productCode
INNER JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY pl.productLine
ORDER BY unique_customers DESC;

-- 2.12 매출 기여도 분석: 상위 20% 고객 매출 비중
-- 목적: 파레토 법칙 검증 (80/20 법칙)
WITH customer_sales AS (
    SELECT 
        c.customerNumber,
        c.customerName,
        SUM(od.quantityOrdered * od.priceEach) AS total_sales
    FROM customers c
    INNER JOIN orders o ON c.customerNumber = o.customerNumber
    INNER JOIN orderdetails od ON o.orderNumber = od.orderNumber
    GROUP BY c.customerNumber, c.customerName
),
total_stats AS (
    SELECT 
        COUNT(*) AS total_count,
        SUM(total_sales) AS total_sales
    FROM customer_sales
)
SELECT 
    'Top 20%' AS segment,
    COUNT(*) AS customer_count,
    SUM(cs.total_sales) AS segment_sales,
    ROUND(SUM(cs.total_sales) * 100.0 / ts.total_sales, 2) AS sales_percentage
FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS rn
    FROM customer_sales
) cs
CROSS JOIN total_stats ts
WHERE cs.rn <= CEIL(ts.total_count * 0.2)
GROUP BY ts.total_sales;

-- 2.13 고객 주문 여부 분류
-- 활성/비활성 고객 구분

-- SELECT 
--     c.customerName,
--     c.country,
--     CASE 
--         WHEN o.orderNumber IS NULL THEN 'No Orders'
--         ELSE 'Has Orders'
--     END AS order_status
-- FROM customers c
-- LEFT JOIN orders o ON c.customerNumber = o.customerNumber
-- GROUP BY c.customerNumber, c.customerName, c.country, order_status;

SELECT 
    c.customerName,
    c.country,
    CASE 
        WHEN COUNT(o.orderNumber) = 0 THEN 'No Orders'
        ELSE 'Has Orders'
    END AS order_status
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
GROUP BY c.customerNumber, c.customerName, c.country;

-- 2.14 지역별 평균 결제액
-- 국가별 결제 패턴 분석
SELECT 
    c.country,
    COUNT(DISTINCT p.checkNumber) AS payment_count,
    AVG(p.amount) AS avg_payment,
    SUM(p.amount) AS total_payments
FROM customers c
INNER JOIN payments p ON c.customerNumber = p.customerNumber
GROUP BY c.country
ORDER BY total_payments DESC;

-- 2.15 제품 라인별 매출 집계
-- 제품 카테고리별 성과 비교
SELECT 
    p.productLine,
    COUNT(DISTINCT od.orderNumber) AS order_count,
    SUM(od.quantityOrdered) AS total_quantity,
    SUM(od.quantityOrdered * od.priceEach) AS total_sales,
    AVG(od.quantityOrdered * od.priceEach) AS avg_order_value
FROM products p
INNER JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productLine
ORDER BY total_sales DESC;

-- 2.16 제품 라인별 수익성 집계
SELECT p.productLine,
       SUM(od.quantityOrdered*od.priceEach) - SUM(p.buyPrice*od.quantityOrdered) AS profit,
       ROUND((SUM(od.quantityOrdered*od.priceEach)-SUM(p.buyPrice*od.quantityOrdered))/SUM(od.quantityOrdered*od.priceEach)*100,2) AS profit_margin_pct
FROM orderdetails od
JOIN products p USING(productCode)
GROUP BY p.productLine;