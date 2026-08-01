"""Load generated orders into the raw PostgreSQL layer."""
from __future__ import annotations

import csv
import os
from pathlib import Path

import psycopg

INSERT_SQL = """
INSERT INTO raw.orders (order_id, order_ts, customer_id, customer_name, product_id, product_name, category, quantity, unit_price, country, source_file)
VALUES (%(order_id)s, %(order_ts)s, %(customer_id)s, %(customer_name)s, %(product_id)s, %(product_name)s, %(category)s, %(quantity)s, %(unit_price)s, %(country)s, %(source_file)s)
ON CONFLICT (order_id) DO UPDATE SET
  order_ts = EXCLUDED.order_ts, customer_id = EXCLUDED.customer_id, customer_name = EXCLUDED.customer_name,
  product_id = EXCLUDED.product_id, product_name = EXCLUDED.product_name, category = EXCLUDED.category,
  quantity = EXCLUDED.quantity, unit_price = EXCLUDED.unit_price, country = EXCLUDED.country,
  source_file = EXCLUDED.source_file, ingested_at = NOW();
"""


def database_url() -> str:
    return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
        user=os.getenv("POSTGRES_USER", "analytics"), password=os.getenv("POSTGRES_PASSWORD", "analytics"),
        host=os.getenv("POSTGRES_HOST", "localhost"), port=os.getenv("POSTGRES_PORT", "5432"), database=os.getenv("POSTGRES_DB", "retail"),
    )


def load_csv(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as file:
        rows = [dict(row, source_file=path.name) for row in csv.DictReader(file)]
    with psycopg.connect(database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(INSERT_SQL, rows)
    return len(rows)
