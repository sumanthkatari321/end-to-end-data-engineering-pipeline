SELECT
    product_id,
    MAX(product_name) AS product_name,
    MAX(category) AS category,
    SUM(quantity) AS units_sold,
    SUM(order_revenue)::numeric(14, 2) AS gross_revenue
FROM {{ ref('stg_orders') }}
GROUP BY 1
