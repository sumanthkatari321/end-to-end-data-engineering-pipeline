SELECT rating, availability, COUNT(*) AS book_count, ROUND(AVG(price_gbp), 2) AS average_price_gbp,
    MIN(scraped_at) AS first_seen_at, MAX(scraped_at) AS last_seen_at
FROM {{ ref('stg_scraped_books') }}
GROUP BY 1, 2
