USE classicmodels;
SHOW TABLES;

-- 각 테이블 레코드 수 
SELECT 'customers' AS table_name, COUNT(*) AS `rows` FROM customers
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'offices', COUNT(*) FROM offices
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'orderdetails', COUNT(*) FROM orderdetails
UNION ALL SELECT 'payments', COUNT(*) FROM payments
UNION ALL SELECT 'productlines', COUNT(*) FROM productlines
UNION ALL SELECT 'products', COUNT(*) FROM products;

-- 1.1 미국 고객 조회
-- 목적: 기본적인 필터링 조건 사용
SELECT customerNumber, customerName, city, state, country
FROM customers
WHERE country = 'USA';

-- 1.2 신용한도 높은 순으로 고객 정렬
-- 목적: 데이터 정렬 및 상위 고객 파악
SELECT customerName, creditLimit
FROM customers
ORDER BY creditLimit DESC;

-- 1.3 고객이 위치한 국가 목록
-- 목적: 중복 제거 및 고유값 추출
SELECT DISTINCT country
FROM customers
ORDER BY country;

-- 1.4 신용한도 상위 5명 고객
-- 목적: Top N 조회
SELECT customerName, creditLimit
FROM customers
ORDER BY creditLimit DESC
LIMIT 5;

-- 1.5 기본: 국가별 고객 수
-- 목적: 그룹별 집계 기초
SELECT country, COUNT(*) AS customer_count
FROM customers
GROUP BY country
ORDER BY customer_count DESC;

-- 1.6 주문 통계
-- 목적: 기본 집계 함수 활용
SELECT 
    COUNT(*) AS total_order_items,
    COUNT(DISTINCT orderNumber) AS total_orders,
    SUM(quantityOrdered * priceEach) AS total_sales,
    ROUND(AVG(quantityOrdered * priceEach), 2) AS avg_order_value
FROM orderdetails;

-- 1.7 주문과 고객 정보
-- 목적: 두 테이블 결합 기초
SELECT 
    o.orderNumber,
    o.orderDate,
    c.customerName,
    c.country
FROM orders o
INNER JOIN customers c ON o.customerNumber = c.customerNumber
LIMIT 10;

-- 1.8 모든 고객과 주문 여부 확인
-- 목적: 주문하지 않은 고객 포함하여 조회
SELECT 
    c.customerName,
    c.country,
    COUNT(o.orderNumber) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
GROUP BY c.customerNumber, c.customerName, c.country
ORDER BY order_count DESC;

-- 1.9 검색: 이름에 'Co'가 포함된 고객
-- 목적: 패턴 매칭 검색
SELECT customerName, city, country
FROM customers
WHERE customerName LIKE '%Co%';

-- 1.10 함수: 2004년 주문 조회
-- 목적: 날짜 함수를 활용한 필터링
SELECT 
    orderNumber,
    orderDate,
    YEAR(orderDate) AS order_year,
    MONTH(orderDate) AS order_month,
    DAY(orderDate) AS order_day
FROM orders
WHERE YEAR(orderDate) = 2004
LIMIT 10;