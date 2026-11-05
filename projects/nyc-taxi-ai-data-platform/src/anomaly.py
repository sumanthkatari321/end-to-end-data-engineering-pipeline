"""Deterministic anomaly detection for daily aggregates."""

from __future__ import annotations

import pandas as pd

METRICS = ("trip_count", "gross_revenue", "avg_fare", "avg_distance")


def detect_anomalies(daily: pd.DataFrame, threshold: float = 3.5) -> list[dict]:
    """Flag robust outliers using the modified z-score (median absolute deviation)."""
    findings: list[dict] = []
    for metric in METRICS:
        if metric not in daily or len(daily) < 4:
            continue
        values = pd.to_numeric(daily[metric], errors="coerce")
        median = values.median()
        mad = (values - median).abs().median()
        if not mad or pd.isna(mad):
            continue
        scores = 0.6745 * (values - median) / mad
        for index in scores.index[scores.abs() > threshold]:
            findings.append(
                {
                    "date": str(pd.Timestamp(daily.loc[index, "pickup_date"]).date()),
                    "metric": metric,
                    "value": float(values.loc[index]),
                    "median": float(median),
                    "modified_z_score": round(float(scores.loc[index]), 2),
                    "direction": "high" if scores.loc[index] > 0 else "low",
                }
            )
    return findings
