from unittest import TestCase
from src.web_scraper.RiyapolaScraper import RiyapolaScraper


class TestRiyapolaScraper(TestCase):
    sample_url_1 = "http://riyapola.com/vehicles/cars/toyota-aqua-g-grade-i32148-{ITEM_CITY}"
    sample_url_2 = "http://riyapola.com/vehicles/cars/toyota-axio-wxb-2019-permit-i32831-horana"

    def test_extract_vehicle_data(self):
        extr_data_1 = RiyapolaScraper.extract_vehicle_data(self.sample_url_1)
        extr_data_2 = RiyapolaScraper.extract_vehicle_data(self.sample_url_2)
        # self.fail()
