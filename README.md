# RetailPulse: End-to-End Data Engineering Pipeline

RetailPulse turns daily retail orders into analytics-ready customer and product metrics. It is designed as a compact, locally runnable portfolio project that demonstrates the full data lifecycle: ingestion, storage, transformation, orchestration, validation, and serving.

## Architecture

```text
Synthetic order events -> Python ingestion -> PostgreSQL (raw)
                                          -> dbt (staging + marts)
Airflow orchestrates ingestion, transformations, and quality checks
Metabase reads curated marts for dashboards
```

## Stack

- **Python** for deterministic source generation and ingestion
- **PostgreSQL** for raw and warehouse storage
- **dbt Core** for SQL transformations and tests
- **Apache Airflow** for scheduled orchestration
- **Metabase** for BI serving
- **Docker Compose** for one-command local deployment
- **GitHub Actions** for lint and unit-test automation

## Quick start

1. Copy `.env.example` to `.env`.
2. Start the platform: `docker compose up --build`.
3. Open Airflow at `http://localhost:8080` (`airflow` / `airflow`) and trigger `retail_daily_pipeline`.
4. Open Metabase at `http://localhost:3000`, connect to PostgreSQL, and explore the `analytics` schema.

The DAG runs three idempotent stages: load daily data, run dbt models, then run dbt tests. Generated input data and pipeline logs are mounted locally under `data/` and `logs/`.

## Data model

| Layer | Relation | Purpose |
|---|---|---|
| Raw | `raw.orders` | Append-safe source events with ingestion metadata |
| Staging | `stg_orders` | Typed, cleaned, deduplicated order records |
| Mart | `fct_daily_sales` | Daily revenue, orders, units, and average order value |
| Mart | `dim_customers` | Customer lifetime value and purchase behavior |
| Mart | `dim_products` | Product-level revenue and sales performance |

## Repository layout

```text
src/                 Python ingestion package
airflow/dags/        Workflow definition
dbt/retail_analytics dbt project and data tests
sql/                 Bootstrap DDL
tests/               Fast unit tests
```

## Quality and reliability choices

- Deterministic data generation makes runs reproducible.
- `ON CONFLICT` upserts make repeated loads safe.
- dbt schema tests enforce primary-key, null, and relationship expectations.
- The DAG retries failed tasks and stops downstream publication on validation failure.
- Environment variables keep credentials out of source control.

## Local validation

```bash
python -m unittest discover -s tests -v
docker compose config
```

## Next steps for cloud deployment

Replace the generator with an API/Kafka source, move raw data to S3, run dbt against Snowflake or BigQuery, and deploy Airflow on MWAA/Composer. The layer boundaries and contracts in this project stay the same.
