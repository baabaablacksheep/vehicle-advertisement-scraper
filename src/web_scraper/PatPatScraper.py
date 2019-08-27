from bs4 import BeautifulSoup, SoupStrainer
from src.web_scraper.Vehicle import Vehicle

import re
import requests
import logging


class PatPatScraper:
    # website_url = "https://patpat.lk/cars/?page=2"
    website_url = "https://patpat.lk/"

    def __init__(self, category, start_page, end_page):
        self.category = category
        self.start_page = start_page
        self.end_page = end_page
        self.formatted_url = self.website_url + self.category + "/?page="

    def extract_data(self):
        ad_link_list = self.visit_site()
        vehicle_list = []
        for ad in ad_link_list:
            vehicle_list.append(self.extract_vehicle_data(ad))
        return vehicle_list

    def visit_site(self):
        ad_url_set = set()
        for page_no in range(self.start_page, self.end_page + 1):
            try:
                r = requests.get(self.formatted_url + str(page_no))
                items = SoupStrainer('div', {'class': re.compile('.*vehicle-result.*')})
                soup = BeautifulSoup(r.content, features="lxml", parse_only=items)
                for sp in soup.findAll('span', {'class': re.compile('.*vehicle-model.*')}):
                    ad_url_set.add("https://patpat.lk/" + sp.parent.get('href'))
            except():
                logging.error("Specified Website Cannot Be Reached %s" % (self.formatted_url + str(page_no)))
                pass
        ad_url_set.discard("null")
        ad_url_list = list(ad_url_set)
        return ad_url_list

    @staticmethod
    def extract_vehicle_data(ad_link):

        try:
            img_url_list = []

            r = requests.get(ad_link)

            if r.status_code == 200:
                # Get Main Div
                main_content = SoupStrainer('div', {'class': re.compile('.*main-content.*')})
                main_soup = BeautifulSoup(r.content, features="lxml", parse_only=main_content)

                # Scrape Advertisement Heading
                ad_title = "unknown"
                ad_title_elem = main_soup.find('h2', {'class': 'heading'})
                if ad_title_elem is not None:
                    ad_title = ad_title_elem.text

                # Scrape Vehicle Info
                vehicle_info_soup = main_soup.find('div', {'class': re.compile('.*vehicle-info.*')})

                brand = "unknown"
                model = "unknown"
                model_year = "unknown"
                body_type = "unknown"

                if vehicle_info_soup is not None:
                    vehicle_info_soup = vehicle_info_soup.find('table')

                    # Extract Brand
                    brand_elem = vehicle_info_soup.find('label', text=re.compile(".*Manufacturer.*", re.I))
                    if brand_elem is not None:
                        brand = brand_elem.parent \
                            .find_next_sibling("td") \
                            .select('span')[0] \
                            .contents[0]\
                            .replace(":", "") \
                            .strip()

                    # Extract Model
                    model_elem = vehicle_info_soup.find('label', text=re.compile(".*Model(\s)*$", re.I))
                    if model_elem is not None:
                        if brand_elem is not None:
                            model = model_elem.parent \
                                .find_next_sibling("td") \
                                .select('span')[0] \
                                .contents[0]\
                                .replace(":", "") \
                                .strip()

                    # Extract Model_year
                    model_year_elem = vehicle_info_soup.find('label', text=re.compile(".*Model Year.*", re.I))
                    if model_year_elem is not None:
                        model_year = model_year_elem.parent \
                                .find_next_sibling("td") \
                                .select('span')[0] \
                                .contents[0]\
                                .replace(":", "") \
                                .strip()

                    # Extract Body_Type
                    body_type_elem = vehicle_info_soup.find('label', text=re.compile(".*Body Type.*", re.I))
                    if body_type_elem is not None:
                        body_type = body_type_elem.parent \
                                .find_next_sibling("td") \
                                .select('span')[0] \
                                .contents[0]\
                                .replace(":", "")\
                                .strip()

                    # Scrape All The Image URLS
                    gallery_items = main_soup.find('div', {'class': 'carousel-inner'})
                    for item in gallery_items.find_all('div', {'class': re.compile('.*item.*')}):
                        img_src = item.select('img')[0].get('src')
                        img_url_list.append("https://patpat.lk/" + img_src)

                return Vehicle(ad_link, ad_title, brand, model, model_year, body_type, img_url_list)
        except():
            logging.error("Error Occurred While Scraping Data from %s" % ad_link)
            pass
