from __future__ import annotations

import os
import subprocess
import sys
from datetime import date
from pathlib import Path

from airflow.decorators import dag, task
from pendulum import datetime

PROJECT_ROOT = Path("/opt/airflow")
sys.path.insert(0, str(PROJECT_ROOT))


@dag(schedule="0 6 * * *", start_date=datetime(2025, 1, 1, tz="UTC"), catchup=False, tags=["retail", "elt"])
def retail_daily_pipeline():
    @task(retries=2)
    def load_daily_orders(logical_date=None):
        from src.generator import write_orders
        from src.ingest import load_csv

        run_date = logical_date.date() if logical_date else date.today()
        file_path = write_orders(run_date, PROJECT_ROOT / "data")
        return {"file": str(file_path), "rows_loaded": load_csv(file_path)}

    @task
    def transform_with_dbt():
        env = {**os.environ, "DBT_PROFILES_DIR": str(PROJECT_ROOT / "dbt")}
        subprocess.run(["dbt", "run", "--project-dir", str(PROJECT_ROOT / "dbt/retail_analytics")], check=True, env=env)

    @task
    def validate_with_dbt():
        env = {**os.environ, "DBT_PROFILES_DIR": str(PROJECT_ROOT / "dbt")}
        subprocess.run(["dbt", "test", "--project-dir", str(PROJECT_ROOT / "dbt/retail_analytics")], check=True, env=env)

    load_daily_orders() >> transform_with_dbt() >> validate_with_dbt()


retail_daily_pipeline()
