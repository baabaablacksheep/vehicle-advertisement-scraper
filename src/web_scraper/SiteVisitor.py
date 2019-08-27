from src.web_scraper.AutoLankaScraper import AutoLankaScraper
from src.web_scraper.CarmudiScraper import CarmudiScraper
from src.web_scraper.IkmanScraper import IkmanScraper
from src.web_scraper.PatPatScraper import PatPatScraper
from src.web_scraper.RiyapolaScraper import RiyapolaScraper
from src.web_scraper.RiyasevanaScraper import RiyasevanaScraper


class SiteVisitor:
    def __init__(self, site_name, category, start_page, end_page):
        self.site_name = site_name
        self.category = category
        self.start_page = start_page
        self.end_page = end_page

    def get_scraped_data(self):
        def select_scraper(site_name):
            switcher = {
                "ikman": IkmanScraper(self.category, self.start_page, self.end_page),
                "carmudi": CarmudiScraper(self.category, self.start_page, self.end_page),
                "patpat": PatPatScraper(self.category, self.start_page, self.end_page),
                "riyasevana": RiyasevanaScraper(self.category, self.start_page, self.end_page),
                "autolanka": AutoLankaScraper(self.category, self.start_page, self.end_page),
                "riyapola": RiyapolaScraper(self.category, self.start_page, self.end_page)
            }
            # Get the function from switcher dictionary
            return switcher.get(site_name, lambda: "Invalid Choice")

        ad_object_list = select_scraper(self.site_name).extract_data()
        return ad_object_list
