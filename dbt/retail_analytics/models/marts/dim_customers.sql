SELECT
    customer_id,
    MAX(customer_name) AS customer_name,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS latest_order_date,
    COUNT(DISTINCT order_id) AS lifetime_orders,
    SUM(order_revenue)::numeric(14, 2) AS lifetime_revenue
FROM {{ ref('stg_orders') }}
GROUP BY 1
