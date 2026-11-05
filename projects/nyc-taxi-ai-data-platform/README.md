# NYC Taxi AI Data Platform

An end-to-end data engineering portfolio project using real NYC Yellow Taxi trip records. It downloads a public monthly Parquet file, validates and transforms it with DuckDB, writes analytics-ready Parquet/CSV outputs, detects operational anomalies, and optionally asks an LLM to explain the aggregate findings.

## What it demonstrates

- Real-world batch ingestion from the NYC Taxi & Limousine Commission public data lake
- Column pruning and partition-friendly Parquet processing with DuckDB
- Data contracts and quality checks for timestamps, fares, distances, and passenger counts
- A curated daily mart with trip volume, revenue, distance, tips, and airport-trip metrics
- Robust anomaly detection using median absolute deviation, without requiring a paid model
- Optional AI-generated narrative grounded only in aggregate metrics
- Reproducible CLI, Docker image, and GitHub Actions validation

## Architecture

```text
NYC TLC monthly Yellow Taxi Parquet (public S3)
                    |
                    v
         Python ingestion + DuckDB
          |                     |
          v                     v
   curated trips          data quality checks
          |
          v
      daily metrics -> anomaly detection -> optional AI narrative
```

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline --year 2024 --month 1
```

Outputs appear in `data/processed/`:

- `yellow_trips_2024_01.parquet` — cleaned trip-level data
- `daily_metrics_2024_01.csv` — analytics mart
- `insights_2024_01.json` — deterministic anomaly findings and optional AI summary
- `run_metadata.json` — source, row counts, and run timestamp

To use a local sample file instead of downloading from TLC:

```bash
python -m src.pipeline --input path/to/yellow_tripdata_2024-01.parquet
```

### Optional AI summary

Set `OPENAI_API_KEY` and optionally `OPENAI_MODEL` (default: `gpt-4.1-mini`) in your shell or `.env`, then pass `--ai`. Only aggregated daily metrics and detected anomalies are sent to the model; trip-level records and identifiers stay local. The pipeline still succeeds without AI credentials.

```bash
# macOS/Linux
export OPENAI_API_KEY="your-key"
python -m src.pipeline --year 2024 --month 1 --ai
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DATA_DIR` | `data` | Local raw and processed output location |
| `OPENAI_API_KEY` | unset | Enables the optional AI summary |
| `OPENAI_MODEL` | `gpt-4.1-mini` | Model used for aggregate insight narration |

## Data quality contract

The pipeline rejects an empty input, missing required columns, invalid pickup timestamps, negative fares or distances, and implausible passenger counts. It excludes corrupt business records from the curated output and reports rejected-row counts in metadata. Duplicate trips are removed by the available trip fields before aggregation.

## CLI options

```text
python -m src.pipeline --year 2024 --month 1 [--input FILE] [--output-dir DIR] [--ai]
```

The TLC public source uses the stable `yellow_tripdata_YYYY-MM.parquet` naming convention. Review TLC's current data dictionary and terms before adapting this for commercial use.

## Run in Docker

```bash
docker build -t nyc-taxi-ai-data-platform .
docker run --rm -v "${PWD}/data:/app/data" nyc-taxi-ai-data-platform --year 2024 --month 1
```

## Project structure

```text
src/pipeline.py       Download, validate, transform, detect, and summarize
src/quality.py        Data contract and rejection accounting
src/anomaly.py        Robust daily metric outlier detection
src/ai_summary.py     Optional LLM narrative over aggregate results
tests/                Unit tests using small in-memory fixtures
```

## Next extensions

Add a monthly scheduler (Airflow or Dagster), store raw files in object storage, load marts into Postgres or Snowflake, and publish a dashboard. The source URL, processing functions, and output contracts are deliberately separated so these additions can be made without changing the data-quality rules.

## Data source

NYC Taxi & Limousine Commission, [Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). This project is independent and is not affiliated with the TLC.
