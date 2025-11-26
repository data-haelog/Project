USE classicmodels;

/* =====================================================
   고객 세그먼트 분석 
     - VIP 및 High-Value 고객 식별
	 → 맞춤형 마케팅 및 고객 유지 전략 수립
===================================================== */
SELECT 
       c.country,
       c.customerName,
       SUM(p.amount) AS total_purchase,
       RANK() OVER(PARTITION BY c.country ORDER BY SUM(p.amount) DESC) AS rank_by_country
FROM payments p
JOIN customers c USING (customerNumber)
GROUP BY c.customerNumber, c.customerName, c.country
HAVING SUM(p.amount) > 5000
ORDER BY c.country, rank_by_country;

/* =====================================================
   제품 라인별 수익성 분석
     - 고가 제품 라인 수익성 평가
	 → 재고 조정 및 프로모션 전략 수립
===================================================== */
SELECT p.productLine,
       SUM(od.quantityOrdered * od.priceEach) AS total_sales,
       SUM(od.quantityOrdered * p.buyPrice) AS total_cost,
       SUM(od.quantityOrdered * od.priceEach) - SUM(p.buyPrice * od.quantityOrdered) AS profit,
       ROUND((SUM(od.quantityOrdered * od.priceEach) - SUM(p.buyPrice * od.quantityOrdered)) 
             / SUM(od.quantityOrdered * od.priceEach) * 100, 2) AS profit_margin_pct
FROM orderdetails od
JOIN products p USING (productCode)
GROUP BY p.productLine
ORDER BY profit DESC;

/* =====================================================
   Funnel 분석 (주문 회전율)
     - 고객 주문 과정에서 이탈 지점을 확인
	 → 마케팅/UX 개선 전략 수립
===================================================== */

WITH total_orders AS (
    SELECT customerNumber,
           COUNT(*) AS orders_count
    FROM orders
    GROUP BY customerNumber
),
total_customers AS (
    SELECT customerNumber
    FROM customers
)
SELECT c.customerNumber,
       COALESCE(o.orders_count, 0) AS orders_count
FROM total_customers c
LEFT JOIN total_orders o USING (customerNumber)
ORDER BY orders_count DESC;


/* =====================================================
   RFM 분석 (고객 가치 평가)
     - 고객 재구매 성향 분석
	 → VIP, 잠재 이탈 고객 파악
===================================================== */
WITH rfm AS (
    SELECT 
        c.customerNumber,
        c.customerName,
        DATEDIFF(CURRENT_DATE, MAX(o.orderDate)) AS recency,
        COUNT(DISTINCT o.orderNumber) AS frequency,
        SUM(p.amount) AS monetary
    FROM customers c
    LEFT JOIN orders o USING (customerNumber)
    LEFT JOIN payments p USING (customerNumber)
    GROUP BY c.customerNumber, c.customerName
)
SELECT *,
       CASE 
           WHEN recency <= 90 AND monetary >= 50000 THEN 'VIP'
           WHEN recency <= 180 AND frequency >= 5 THEN 'Loyal'
           WHEN recency > 365 THEN 'At Risk'
           ELSE 'Regular'
       END AS customer_segment
FROM rfm
ORDER BY monetary DESC, frequency DESC;

/* =====================================================
   월별 매출 추이 분석
     - 월별 매출 패턴 확인
	 → 시즌별 재고 및 프로모션 계획 수립
===================================================== */
SELECT DATE_FORMAT(o.orderDate, '%Y-%m') AS month,
       COUNT(DISTINCT o.orderNumber) AS order_count,
       SUM(od.quantityOrdered * od.priceEach) AS monthly_sales
FROM orders o
JOIN orderdetails od USING (orderNumber)
GROUP BY month
ORDER BY month;

/* =====================================================
  국가별 고객 매출 비교
     - 국가별 매출 집중도 확인
	 → 지역별 마케팅/영업 전략 수립
===================================================== */
SELECT country,
       COUNT(DISTINCT customerNumber) AS customer_count,
       SUM(amount) AS total_sales
FROM customers c
JOIN payments p USING (customerNumber)
GROUP BY country
ORDER BY total_sales DESC;


/* =====================================================
   TOP 제품별 매출 기여도 분석
     - 상위 제품군 매출 기여도 분석
	 → 핵심 제품 집중 전략 수립
===================================================== */
WITH product_sales AS (
    SELECT productCode,
           SUM(quantityOrdered * priceEach) AS total_sales
    FROM orderdetails
    GROUP BY productCode
)
SELECT productCode,
       total_sales,
       RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM product_sales
ORDER BY total_sales DESC;


/* =====================================================
   고객 지역별 주문 분석
     - 지역별 주문 특성 파악
	 → 지역 마케팅/재고 전략 수립
===================================================== */
SELECT state, city,
       COUNT(o.orderNumber) AS total_orders,
       SUM(od.quantityOrdered*od.priceEach) AS total_sales
FROM orders o
JOIN orderdetails od USING (orderNumber)
JOIN customers c USING (customerNumber)
GROUP BY state, city
ORDER BY total_sales DESC;


/* =====================================================
  장기 미구매 고객 식별
     - 오랜 기간 구매 없는 고객 식별
	 → 리타겟팅/재활성화 캠페인 설계
===================================================== */
SELECT customerNumber,
       MAX(orderDate) AS last_order,
       DATEDIFF(CURRENT_DATE, MAX(orderDate)) AS days_since_last_order
FROM orders
GROUP BY customerNumber
HAVING days_since_last_order > 365
ORDER BY days_since_last_order DESC;

/* =====================================================
   신제품 런칭 효과 분석
     - 신제품 출시 후 매출 효과 분석
	 → 마케팅 ROI 평가 및 전략 수정
===================================================== */
SELECT p.productName,
       SUM(od.quantityOrdered*od.priceEach) AS total_sales,
       COUNT(DISTINCT o.orderNumber) AS total_orders
FROM products p
JOIN orderdetails od USING (productCode)
JOIN orders o USING (orderNumber)
WHERE o.orderDate >= '2005-01-01'
GROUP BY p.productName
ORDER BY total_sales DESC;

/* =====================================================
   재구매율 분석
     - 고객 구매 빈도별 분포 파악
	 → 고객 충성도 평가 및 재구매 유도 전략 수립
===================================================== */
WITH order_counts AS (
    SELECT 
        customerNumber,
        COUNT(*) AS total_orders
    FROM orders
    GROUP BY customerNumber
)
SELECT 
    CASE 
        WHEN total_orders = 1 THEN '1회 구매'
        WHEN total_orders BETWEEN 2 AND 5 THEN '2-5회'
        WHEN total_orders BETWEEN 6 AND 10 THEN '6-10회'
        ELSE '11회 이상'
    END AS purchase_frequency,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_counts), 2) AS percentage
FROM order_counts
GROUP BY purchase_frequency
ORDER BY MIN(total_orders);

/* =====================================================
   대시보드 KPI
     - 경영진 리포팅 및 의사결정 지원
===================================================== */
SELECT 
    COUNT(DISTINCT o.orderNumber) AS total_orders,
    COUNT(DISTINCT c.customerNumber) AS total_customers,
    ROUND(SUM(od.quantityOrdered * od.priceEach), 2) AS total_revenue,
    ROUND(AVG(order_value), 2) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
LEFT JOIN orderdetails od ON o.orderNumber = od.orderNumber
LEFT JOIN (
    SELECT orderNumber, SUM(quantityOrdered * priceEach) AS order_value
    FROM orderdetails
    GROUP BY orderNumber
) AS ov ON o.orderNumber = ov.orderNumber;

/* =====================================================
코호트 분석
===================================================== */
WITH first_purchase AS (
    SELECT 
        customerNumber,
        DATE_FORMAT(MIN(orderDate), '%Y-%m') AS cohort_month
    FROM orders
    GROUP BY customerNumber
)
SELECT 
    fp.cohort_month,
    DATE_FORMAT(o.orderDate, '%Y-%m') AS order_month,
    COUNT(DISTINCT o.customerNumber) AS active_customers
FROM first_purchase fp
JOIN orders o USING (customerNumber)
GROUP BY fp.cohort_month, order_month
ORDER BY cohort_month, order_month;

