"""Input schema validation and business-rule quality checks."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

REQUIRED_COLUMNS = {
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "total_amount",
}


@dataclass
class QualityResult:
    clean: pd.DataFrame
    input_rows: int
    rejected_rows: int
    duplicate_rows: int


def validate_and_clean(frame: pd.DataFrame) -> QualityResult:
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError("Input contains no trips")

    trips = frame.copy()
    trips["tpep_pickup_datetime"] = pd.to_datetime(
        trips["tpep_pickup_datetime"], errors="coerce"
    )
    trips["tpep_dropoff_datetime"] = pd.to_datetime(
        trips["tpep_dropoff_datetime"], errors="coerce"
    )
    numeric = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
    for column in numeric:
        trips[column] = pd.to_numeric(trips[column], errors="coerce")

    valid = (
        trips["tpep_pickup_datetime"].notna()
        & trips["tpep_dropoff_datetime"].notna()
        & (trips["tpep_dropoff_datetime"] >= trips["tpep_pickup_datetime"])
        & trips["passenger_count"].between(0, 6)
        & (trips["trip_distance"] >= 0)
        & (trips["fare_amount"] >= 0)
        & (trips["total_amount"] >= 0)
    )
    rejected = int((~valid).sum())
    trips = trips.loc[valid].copy()
    before_dedup = len(trips)
    trips = trips.drop_duplicates().reset_index(drop=True)
    return QualityResult(
        clean=trips,
        input_rows=len(frame),
        rejected_rows=rejected,
        duplicate_rows=before_dedup - len(trips),
    )
