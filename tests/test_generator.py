from datetime import date
from pathlib import Path
import unittest

from src.generator import FIELDS, generate_orders, write_orders


class GeneratorTests(unittest.TestCase):
    def test_generation_is_deterministic_and_has_unique_order_ids(self):
        first = generate_orders(date(2025, 1, 1), count=5)
        second = generate_orders(date(2025, 1, 1), count=5)
        self.assertEqual(first, second)
        self.assertEqual(5, len({row["order_id"] for row in first}))

    def test_write_orders_creates_csv_with_headers(self):
        output_dir = Path(".test-output")
        file_path = write_orders(date(2025, 1, 1), output_dir, count=1)
        self.assertTrue(file_path.exists())
        self.assertEqual(",".join(FIELDS), file_path.read_text(encoding="utf-8").splitlines()[0])


if __name__ == "__main__":
    unittest.main()
