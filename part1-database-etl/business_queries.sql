USE fleximart;
-- Note:
-- This project uses a denormalized sales fact table instead of
-- separate orders and order_items tables.
-- The sales table represents transactional order-level data.


-- ============================================================
-- Query 1: Customer Purchase History
-- Business Question:
-- Generate a detailed report showing each customer's name,
-- email, total number of orders placed, and total amount spent.
-- Include only customers who have placed at least 2 orders
-- and spent more than ₹5,000.
-- Order by total amount spent in descending order.
-- ============================================================

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    COUNT(DISTINCT s.transaction_id) AS total_orders,
    SUM(s.quantity * s.unit_price) AS total_spent
FROM customers c
JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.status = 'Completed'
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email
HAVING
    COUNT(DISTINCT s.transaction_id) >= 2
    AND SUM(s.quantity * s.unit_price) > 5000
ORDER BY total_spent DESC;


-- ============================================================
-- Query 2: Product Sales Analysis
-- Business Question:
-- For each product category, show the category name,
-- number of different products sold, total quantity sold,
-- and total revenue generated.
-- Include only categories that generated more than ₹10,000
-- in revenue.
-- Order by total revenue descending.
-- ============================================================

SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS num_products,
    SUM(s.quantity) AS total_quantity_sold,
    SUM(s.quantity * s.unit_price) AS total_revenue
FROM products p
JOIN sales s
    ON p.product_id = s.product_id
WHERE s.status = 'Completed'
GROUP BY p.category
HAVING SUM(s.quantity * s.unit_price) > 10000
ORDER BY total_revenue DESC;


-- ============================================================
-- Query 3: Monthly Sales Trend (2024)
-- Business Question:
-- Show monthly sales trends for the year 2024.
-- For each month display:
-- month name, total number of orders,
-- total revenue, and cumulative revenue
-- from January to that month.
-- ============================================================

SELECT
    MONTHNAME(transaction_date) AS month_name,
    COUNT(DISTINCT transaction_id) AS total_orders,
    SUM(quantity * unit_price) AS monthly_revenue,
    SUM(SUM(quantity * unit_price)) OVER (
        ORDER BY MONTH(transaction_date)
    ) AS cumulative_revenue
FROM sales
WHERE
    status = 'Completed'
    AND YEAR(transaction_date) = 2024
GROUP BY
    MONTH(transaction_date),
    MONTHNAME(transaction_date)
ORDER BY MONTH(transaction_date);
