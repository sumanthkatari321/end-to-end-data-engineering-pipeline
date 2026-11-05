# Data contract

## Source

NYC TLC Yellow Taxi trip records, one monthly Parquet object per period. The source can also be supplied as a local Parquet file for repeatable development.

## Required fields

| Field | Contract |
|---|---|
| `tpep_pickup_datetime` | Parseable timestamp; required |
| `tpep_dropoff_datetime` | Parseable and not earlier than pickup |
| `passenger_count` | Numeric and within 0–6 |
| `trip_distance` | Numeric and nonnegative |
| `fare_amount` | Numeric and nonnegative |
| `total_amount` | Numeric and nonnegative |

`tip_amount` and pickup location are used when available to calculate tip and airport metrics. They are not part of the minimum required schema.

## Rejection and deduplication

Records that fail a required field or business rule are excluded from curated output and counted as rejected. Exact duplicate rows are reduced to one and counted separately. A run with no source rows or no valid rows fails rather than publishing an empty mart.

## Curated daily metrics

One row per pickup date: trip count, gross revenue, average fare, average distance, average tip, and the share of airport trips. All metric definitions are explicit in the SQL aggregation in `src/pipeline.py`.

## Anomaly interpretation

Daily outliers use a modified z-score derived from median absolute deviation. This flags unusual values for investigation; it does not label a day as an error or infer a cause. Short histories and constant metrics do not generate anomaly flags.
