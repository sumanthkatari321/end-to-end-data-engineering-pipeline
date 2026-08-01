SELECT
    order_date,
    country,
    COUNT(DISTINCT order_id) AS order_count,
    COUNT(DISTINCT customer_id) AS customer_count,
    SUM(quantity) AS units_sold,
    SUM(order_revenue)::numeric(14, 2) AS gross_revenue,
    ROUND(SUM(order_revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_order_value
FROM {{ ref('stg_orders') }}
GROUP BY 1, 2
