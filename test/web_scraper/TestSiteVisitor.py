from unittest import TestCase

from src.web_scraper.SiteVisitor import SiteVisitor


class TestSiteVisitor(TestCase):
    def test_get_scraped_data(self):
        # Start of Executing The Program
        vehicles = SiteVisitor("ikman", "cars", 0, 1).get_scraped_data()

        vehicle1 = vehicles[0]
        assert vehicle1
        print("\nVehicle 1 Info: ")
        vehicle1.showInfo()

        vehicle2 = vehicles[1]
        assert vehicle2
        print("\nVehicle 2 Info: ")
        vehicle2.showInfo()

        vehicle3 = vehicles[2]
        assert vehicle3
        print("\nVehicle 3 Info: ")
        vehicle2.showInfo()

        # self.fail()
