# WebShelf — Web Scraping to Data Warehouse

WebShelf scrapes a public practice book catalogue and turns it into analytics-ready warehouse tables. It is a compact, locally runnable portfolio project that demonstrates scraping, raw storage, transformation, orchestration, validation, and serving.

## Architecture

```text
Books to Scrape -> Python scraper -> PostgreSQL (raw)
                                   -> dbt (staging + marts)
Airflow orchestrates scraping, transformations, and quality checks
Metabase reads curated marts for dashboards
```

## Stack

- Python, Requests, and Beautiful Soup for scraping and ingestion
- PostgreSQL for raw and warehouse storage
- dbt Core for SQL transformations and tests
- Apache Airflow for scheduled orchestration
- Metabase for BI serving
- Docker Compose for one-command local deployment
- GitHub Actions for lint and unit-test automation

## Quick start

1. Copy `.env.example` to `.env`.
2. Start the platform: `docker compose up --build`.
3. Open Airflow at `http://localhost:8080` (`airflow` / `airflow`) and trigger `web_scraping_warehouse_pipeline`.
4. Open Metabase at `http://localhost:3000`, connect to PostgreSQL, and explore the `analytics` schema.

The DAG scrapes a catalogue page, loads PostgreSQL, then runs and tests dbt models. It targets [Books to Scrape](https://books.toscrape.com/), an intentionally scrapeable practice site. Always confirm a real source's terms and robots policy before using it in production.

## Data model

| Layer | Relation | Purpose |
|---|---|---|
| Raw | `raw.scraped_books` | Catalogue snapshot with source and scrape timestamp |
| Staging | `stg_scraped_books` | Typed, cleaned, deduplicated catalogue records |
| Mart | `fct_book_catalog` | Book counts and average price by rating and availability |

## Repository layout

```text
src/                 Web scraper and PostgreSQL ingestion package
airflow/dags/         Workflow definition
dbt/retail_analytics  dbt project and data tests
sql/                  Bootstrap DDL
tests/                Fast unit tests
```

## Quality and reliability choices

- A configured timeout and identifiable user agent make source requests predictable.
- `ON CONFLICT` upserts make repeated catalogue loads safe.
- dbt schema tests enforce natural-key and null constraints.
- The DAG retries failed tasks and stops downstream publication on validation failure.
- Environment variables keep credentials out of source control.

## Local validation

```bash
python -m unittest discover -s tests -v
docker compose config
```

## Next steps for cloud deployment

Move raw snapshots to object storage, add pagination and historical price tracking, run dbt against Snowflake or BigQuery, and deploy Airflow on MWAA/Composer. The layer boundaries and contracts stay the same.
