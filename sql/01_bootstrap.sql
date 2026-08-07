CREATE DATABASE airflow;
\connect retail
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS raw.orders (
  order_id TEXT PRIMARY KEY,
  order_ts TIMESTAMPTZ NOT NULL,
  customer_id TEXT NOT NULL,
  customer_name TEXT NOT NULL,
  product_id TEXT NOT NULL,
  product_name TEXT NOT NULL,
  category TEXT NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
  country TEXT NOT NULL,
  source_file TEXT NOT NULL,
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.scraped_books (
  product_url TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  price_gbp NUMERIC(10, 2) NOT NULL CHECK (price_gbp >= 0),
  rating TEXT NOT NULL,
  availability TEXT NOT NULL,
  source_url TEXT NOT NULL,
  scraped_at TIMESTAMPTZ NOT NULL
);
