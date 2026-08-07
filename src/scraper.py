"""Scrape a public practice catalogue and normalize records for the raw layer."""
from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

DEFAULT_SOURCE_URL = "https://books.toscrape.com/catalogue/page-1.html"


def scrape_books(source_url: str = DEFAULT_SOURCE_URL, timeout: int = 20) -> list[dict[str, str]]:
    """Fetch one Books to Scrape catalogue page.

    The target is an intentionally scrapeable practice site. A real deployment
    should use a source only when its terms of service and robots policy allow it.
    """
    response = requests.get(source_url, timeout=timeout, headers={"User-Agent": "WebShelfDataProject/1.0"})
    response.raise_for_status()
    scraped_at = datetime.now(timezone.utc).isoformat()
    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        price = card.select_one("p.price_color")
        rating = card.select_one("p.star-rating")
        if not link or not price or not rating:
            continue
        relative_url = link.get("href", "")
        books.append({
            "product_url": urljoin(source_url, relative_url),
            "title": link.get("title", "").strip(),
            "price_gbp": price.get_text(strip=True).replace("£", ""),
            "rating": next((value for value in rating.get("class", []) if value != "star-rating"), "Unknown"),
            "availability": "In stock" if "In stock" in card.get_text(" ", strip=True) else "Unknown",
            "source_url": source_url,
            "scraped_at": scraped_at,
        })
    return books
