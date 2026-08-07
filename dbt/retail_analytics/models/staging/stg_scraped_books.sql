WITH ranked_books AS (
    SELECT product_url, TRIM(title) AS title, price_gbp::numeric(10, 2) AS price_gbp,
        rating, availability, source_url, scraped_at,
        ROW_NUMBER() OVER (PARTITION BY product_url ORDER BY scraped_at DESC) AS row_number
    FROM raw.scraped_books
)
SELECT * EXCEPT (row_number) FROM ranked_books WHERE row_number = 1
