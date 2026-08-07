from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from airflow.decorators import dag, task
from pendulum import datetime

PROJECT_ROOT = Path("/opt/airflow")
sys.path.insert(0, str(PROJECT_ROOT))


@dag(schedule="0 6 * * *", start_date=datetime(2025, 1, 1, tz="UTC"), catchup=False, tags=["web-scraping", "elt"])
def web_scraping_warehouse_pipeline():
    @task(retries=2)
    def scrape_and_load_catalogue():
        from src.ingest import load_books
        from src.scraper import scrape_books

        return {"rows_loaded": load_books(scrape_books())}

    @task
    def transform_with_dbt():
        env = {**os.environ, "DBT_PROFILES_DIR": str(PROJECT_ROOT / "dbt")}
        subprocess.run(["dbt", "run", "--project-dir", str(PROJECT_ROOT / "dbt/retail_analytics")], check=True, env=env)

    @task
    def validate_with_dbt():
        env = {**os.environ, "DBT_PROFILES_DIR": str(PROJECT_ROOT / "dbt")}
        subprocess.run(["dbt", "test", "--project-dir", str(PROJECT_ROOT / "dbt/retail_analytics")], check=True, env=env)

    scrape_and_load_catalogue() >> transform_with_dbt() >> validate_with_dbt()


web_scraping_warehouse_pipeline()
