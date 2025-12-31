-- =========================================================
-- Task 3.3: OLAP Analytics Queries
-- Database: fleximart_dw
-- =========================================================

USE fleximart;

-- =========================================================
-- Query 1: Monthly Sales Drill-Down Analysis
-- Business Scenario:
-- The CEO wants to analyze sales performance over time.
-- Drill-down from Year → Quarter → Month.
-- =========================================================

SELECT
    d.year,
    d.quarter,
    d.month_name,
    SUM(f.total_amount) AS total_sales,
    SUM(f.quantity_sold) AS total_quantity
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;

-- =========================================================
-- Query 2: Product Performance Analysis
-- Business Scenario:
-- Identify top 10 products by revenue.
-- Show category, units sold, revenue, and revenue percentage.
-- =========================================================

SELECT
    p.product_name,
    p.category,
    SUM(f.quantity_sold) AS units_sold,
    SUM(f.total_amount) AS revenue,
    ROUND(
        (SUM(f.total_amount) /
        (SELECT SUM(total_amount) FROM fact_sales)) * 100,
        2
    ) AS revenue_percentage
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_key,
    p.product_name,
    p.category
ORDER BY
    revenue DESC
LIMIT 10;

-- =========================================================
-- Query 3: Customer Segmentation Analysis
-- Business Scenario:
-- Segment customers based on total spending:
-- High Value    : > 50,000
-- Medium Value  : 20,000 – 50,000
-- Low Value     : < 20,000
-- =========================================================

WITH customer_spending AS (
    SELECT
        c.customer_key,
        SUM(f.total_amount) AS total_spent
    FROM fact_sales f
    JOIN dim_customer c
        ON f.customer_key = c.customer_key
    GROUP BY
        c.customer_key
)

SELECT
    CASE
        WHEN total_spent > 50000 THEN 'High Value'
        WHEN total_spent BETWEEN 20000 AND 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*) AS customer_count,
    SUM(total_spent) AS total_revenue,
    ROUND(AVG(total_spent), 2) AS avg_revenue_per_customer
FROM customer_spending
GROUP BY
    customer_segment
ORDER BY
    total_revenue DESC;
