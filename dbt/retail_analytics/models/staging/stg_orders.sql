WITH ranked_orders AS (
    SELECT
        order_id,
        order_ts::timestamp AS order_ts,
        order_ts::date AS order_date,
        customer_id,
        TRIM(customer_name) AS customer_name,
        product_id,
        TRIM(product_name) AS product_name,
        category,
        quantity::integer AS quantity,
        unit_price::numeric(12, 2) AS unit_price,
        quantity * unit_price AS order_revenue,
        country,
        ingested_at,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ingested_at DESC) AS row_number
    FROM raw.orders
)
SELECT * EXCEPT (row_number)
FROM ranked_orders
WHERE row_number = 1
