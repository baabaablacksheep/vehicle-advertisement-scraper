from unittest import TestCase

from src.web_scraper.CarmudiScraper import CarmudiScraper


class TestCarmudiScraper(TestCase):
    def test_visit_site(self):
        assert CarmudiScraper("cars", 1, 2).visit_site(), "List Should Not Be Empty"
        # self.fail()
