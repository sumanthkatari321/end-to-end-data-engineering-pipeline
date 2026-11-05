import unittest

import pandas as pd

from src.anomaly import detect_anomalies


class AnomalyTests(unittest.TestCase):
    def test_flags_extreme_daily_volume(self):
        daily = pd.DataFrame(
            {"pickup_date": pd.date_range("2024-01-01", periods=5),
             "trip_count": [100, 101, 99, 102, 900]}
        )
        findings = detect_anomalies(daily)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["metric"], "trip_count")
        self.assertEqual(findings[0]["direction"], "high")

    def test_needs_sufficient_history(self):
        daily = pd.DataFrame({"pickup_date": pd.date_range("2024-01-01", periods=3), "trip_count": [1, 2, 3]})
        self.assertEqual(detect_anomalies(daily), [])


if __name__ == "__main__":
    unittest.main()
