import unittest

import pandas as pd

from src.quality import validate_and_clean


def fixture() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "tpep_pickup_datetime": ["2024-01-01 10:00:00", "2024-01-01 11:00:00", "bad"],
            "tpep_dropoff_datetime": ["2024-01-01 10:15:00", "2024-01-01 10:50:00", "2024-01-01"],
            "passenger_count": [1, 1, 1],
            "trip_distance": [2.1, 3.2, 1.0],
            "fare_amount": [10.0, 12.0, 5.0],
            "total_amount": [13.0, 15.0, 6.0],
        }
    )


class QualityTests(unittest.TestCase):
    def test_rejects_invalid_datetime(self):
        result = validate_and_clean(fixture())
        self.assertEqual(len(result.clean), 2)
        self.assertEqual(result.rejected_rows, 1)

    def test_deduplicates_exact_duplicate_rows(self):
        frame = pd.concat([fixture().iloc[[0]], fixture().iloc[[0]]], ignore_index=True)
        result = validate_and_clean(frame)
        self.assertEqual(len(result.clean), 1)
        self.assertEqual(result.duplicate_rows, 1)

    def test_missing_columns_fail_fast(self):
        with self.assertRaisesRegex(ValueError, "missing required columns"):
            validate_and_clean(pd.DataFrame({"fare_amount": [1]}))


if __name__ == "__main__":
    unittest.main()
