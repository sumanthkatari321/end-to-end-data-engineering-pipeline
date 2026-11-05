# Roadmap

This roadmap separates the current local batch workflow from proposed production extensions.

## Current

- Download one TLC Yellow Taxi month or read a local Parquet file.
- Validate, deduplicate, curate, aggregate, and write period-scoped outputs.
- Detect robust statistical outliers.
- Optionally generate an AI explanation from aggregate metrics.
- Run unit tests in GitHub Actions.

## Next

1. Add orchestration with retries, backfills, and run-level observability.
2. Add a persistent warehouse target and dbt models for bronze, silver, and gold layers.
3. Add source freshness checks and quarantine output for rejected rows.
4. Add a small dashboard over daily metrics and anomaly history.
5. Add incremental processing and explicit late-arriving data handling.

Each extension should include a documented decision, a clear data contract, and an automated check before it is called production-ready.
