import unittest
from unittest.mock import Mock, patch

from src.scraper import scrape_books

HTML = '''<article class="product_pod"><h3><a href="book.html" title="A Book">A Book</a></h3><p class="price_color">£12.50</p><p class="star-rating Three"></p><p>In stock</p></article>'''


class ScraperTests(unittest.TestCase):
    @patch("src.scraper.requests.get")
    def test_scrape_books_normalizes_a_catalogue_card(self, get):
        get.return_value = Mock(text=HTML)
        rows = scrape_books("https://books.toscrape.com/catalogue/page-1.html")
        self.assertEqual(rows[0]["title"], "A Book")
        self.assertEqual(rows[0]["price_gbp"], "12.50")
        self.assertEqual(rows[0]["rating"], "Three")
        self.assertEqual(rows[0]["product_url"], "https://books.toscrape.com/catalogue/book.html")
