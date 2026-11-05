# End-to-End Data Engineering Projects

A portfolio repository for practical data engineering patterns, from raw ingestion through analytics-ready outputs.

## Projects

### NYC Taxi AI Data Platform

A real-world batch pipeline for NYC TLC Yellow Taxi trip records. It ingests monthly public Parquet data, validates the source contract, creates curated trip and daily metric outputs with DuckDB, detects statistical anomalies, and optionally generates an AI explanation from aggregate metrics.

- [Project guide and quick start](projects/nyc-taxi-ai-data-platform/README.md)
- [Architecture](projects/nyc-taxi-ai-data-platform/docs/architecture.md)
- [Data contract](projects/nyc-taxi-ai-data-platform/docs/data-contract.md)
- [Roadmap](projects/nyc-taxi-ai-data-platform/docs/roadmap.md)

Run this project independently from its directory:

```bash
cd projects/nyc-taxi-ai-data-platform
pip install -r requirements.txt
python -m src.pipeline --year 2024 --month 1
```

The AI summary is optional. Set `OPENAI_API_KEY` and pass `--ai`; only daily aggregates and anomaly findings are sent to the model.

### RetailPulse pipeline example

The original local demo shows a scheduled retail ELT flow using Python, PostgreSQL, Airflow, dbt, Docker Compose, and Metabase. It uses deterministic generated orders so the infrastructure can be exercised without external data access.

Start the services with `docker compose up --build`, then follow the [Airflow and Metabase setup](#retailpulse-local-stack).

## Repository structure

```text
projects/
  nyc-taxi-ai-data-platform/  Real TLC data, DuckDB, quality rules, AI insights
src/                          RetailPulse example ingestion and generator
airflow/dags/                 RetailPulse orchestration
dbt/retail_analytics/         RetailPulse staging models and marts
sql/                          PostgreSQL bootstrap
tests/                        RetailPulse unit tests
```

## RetailPulse local stack

1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. Open Airflow at `http://localhost:8080` and trigger `retail_daily_pipeline`.
4. Open Metabase at `http://localhost:3000` and connect to PostgreSQL.

The Airflow DAG loads generated orders, runs dbt transformations, and executes dbt tests. The NYC Taxi project has its own dependencies, CLI, documentation, and CI test step.

## Data sources and attribution

The NYC Taxi project uses the New York City Taxi & Limousine Commission [Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). This repository is independent and is not affiliated with the TLC.

## Development

RetailPulse tests run with:

```bash
python -m unittest discover -s tests -v
```

The NYC Taxi project test suite runs in its own GitHub Actions step using the dependencies from its `requirements.txt`.
