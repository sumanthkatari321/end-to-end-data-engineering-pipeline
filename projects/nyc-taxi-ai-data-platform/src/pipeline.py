"""Download, quality-check, transform, and optionally narrate NYC TLC trips."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd
from dotenv import load_dotenv

from .ai_summary import summarize
from .anomaly import detect_anomalies
from .quality import validate_and_clean

TLC_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet"


def daily_aggregate(clean: pd.DataFrame) -> pd.DataFrame:
    trips = clean.copy()
    if "tip_amount" not in trips:
        trips["tip_amount"] = 0.0
    trips["pickup_date"] = trips["tpep_pickup_datetime"].dt.date
    trips["is_airport_trip"] = trips.get("PULocationID", pd.Series(index=trips.index)).isin(
        [1, 132, 138]
    )
    con = duckdb.connect(database=":memory:")
    try:
        con.register("trips", trips)
        return con.execute(
            """
            SELECT pickup_date,
                   count(*)::BIGINT AS trip_count,
                   round(sum(total_amount), 2) AS gross_revenue,
                   round(avg(total_amount), 2) AS avg_fare,
                   round(avg(trip_distance), 2) AS avg_distance,
                   round(avg(tip_amount), 2) AS avg_tip,
                   round(100.0 * avg(CASE WHEN is_airport_trip THEN 1 ELSE 0 END), 2)
                       AS airport_trip_pct
            FROM trips
            GROUP BY pickup_date
            ORDER BY pickup_date
            """
        ).df()
    finally:
        con.close()


def run(year: int, month: int, input_file: str | None, output_dir: Path, with_ai: bool) -> dict:
    if not 2009 <= year <= datetime.now(timezone.utc).year or not 1 <= month <= 12:
        raise ValueError("Choose a valid year (2009 or later) and month (1-12)")
    output_dir.mkdir(parents=True, exist_ok=True)
    source = input_file or TLC_URL.format(year=year, month=month)
    if input_file and not Path(input_file).is_file():
        raise FileNotFoundError(input_file)

    # Inspect the schema, then project only fields we can use. TLC occasionally
    # changes optional columns between years, so they must not break ingestion.
    con = duckdb.connect(database=":memory:")
    try:
        con.execute("INSTALL httpfs; LOAD httpfs;")
        available = set(con.execute(
            "DESCRIBE SELECT * FROM read_parquet(?)", [source]
        ).df()["column_name"])
        required = (
            "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count",
            "trip_distance", "fare_amount", "total_amount",
        )
        missing = set(required).difference(available)
        if missing:
            raise ValueError(f"Input is missing required columns: {', '.join(sorted(missing))}")
        optional = ("tip_amount", "PULocationID", "DOLocationID", "VendorID")
        columns = ", ".join(f'"{column}"' for column in (*required, *(c for c in optional if c in available)))
        frame = con.execute(
            f"SELECT {columns} FROM read_parquet(?)", [source]
        ).df()
    finally:
        con.close()

    result = validate_and_clean(frame)
    if result.clean.empty:
        raise ValueError("No valid trips remain after applying the data quality contract")
    stem = f"yellow_{year}_{month:02d}"
    trips_path = output_dir / f"trips_{stem}.parquet"
    mart_path = output_dir / f"daily_metrics_{year}_{month:02d}.csv"
    insights_path = output_dir / f"insights_{year}_{month:02d}.json"

    result.clean.to_parquet(trips_path, index=False)
    daily = daily_aggregate(result.clean)
    daily.to_csv(mart_path, index=False)
    anomalies = detect_anomalies(daily)
    daily_records = daily.assign(pickup_date=daily["pickup_date"].astype(str)).to_dict("records")
    narrative = summarize(daily_records, anomalies) if with_ai else None
    insights = {
        "period": f"{year}-{month:02d}",
        "anomaly_method": "modified z-score (median absolute deviation)",
        "anomalies": anomalies,
        "ai_summary": narrative,
    }
    insights_path.write_text(json.dumps(insights, indent=2), encoding="utf-8")
    metadata = {
        "source": source,
        "processed_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_rows": result.input_rows,
        "valid_rows": len(result.clean),
        "rejected_rows": result.rejected_rows,
        "duplicate_rows": result.duplicate_rows,
        "daily_rows": len(daily),
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--month", type=int, default=1)
    parser.add_argument("--input", help="Local TLC-compatible Parquet file")
    parser.add_argument("--output-dir", default=os.getenv("DATA_DIR", "data/processed"))
    parser.add_argument("--ai", action="store_true", help="Generate an optional AI narrative")
    args = parser.parse_args()
    metadata = run(args.year, args.month, args.input, Path(args.output_dir), args.ai)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()

