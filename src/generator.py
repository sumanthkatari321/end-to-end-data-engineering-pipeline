"""Deterministic retail event generation for local development."""
from __future__ import annotations

import csv
import random
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

PRODUCTS = [
    ("P-100", "Mechanical Keyboard", "Electronics", 89.99),
    ("P-200", "Noise Cancelling Headphones", "Electronics", 129.99),
    ("P-300", "Coffee Grinder", "Home", 64.50),
    ("P-400", "Running Shoes", "Sports", 74.00),
]
CUSTOMERS = [("C-001", "Ava Patel"), ("C-002", "Noah Chen"), ("C-003", "Mia Smith"), ("C-004", "Liam Jones")]
COUNTRIES = ["India", "United States", "United Kingdom", "Singapore"]
FIELDS = ["order_id", "order_ts", "customer_id", "customer_name", "product_id", "product_name", "category", "quantity", "unit_price", "country"]


def generate_orders(run_date: date, count: int = 40) -> list[dict[str, str]]:
    """Generate stable events so retrying a run yields the same natural keys."""
    rng = random.Random(run_date.isoformat())
    rows = []
    for sequence in range(1, count + 1):
        customer_id, customer_name = rng.choice(CUSTOMERS)
        product_id, product_name, category, price = rng.choice(PRODUCTS)
        timestamp = datetime.combine(run_date, time.min, tzinfo=timezone.utc) + timedelta(minutes=rng.randrange(1440))
        rows.append({
            "order_id": f"{run_date:%Y%m%d}-{sequence:04d}",
            "order_ts": timestamp.isoformat(),
            "customer_id": customer_id,
            "customer_name": customer_name,
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "quantity": str(rng.randint(1, 4)),
            "unit_price": f"{price:.2f}",
            "country": rng.choice(COUNTRIES),
        })
    return rows


def write_orders(run_date: date, output_dir: Path, count: int = 40) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"orders_{run_date.isoformat()}.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(generate_orders(run_date, count))
    return path
