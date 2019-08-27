from bs4 import BeautifulSoup, SoupStrainer
from src.web_scraper.Vehicle import Vehicle

import re
import requests
import logging


# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class AutoLankaScraper:
    # website_url = "http://www.autolanka.com/cars/?page=2"
    website_url = "http://www.autolanka.com/"

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
        vehicle_list = list(filter(None, vehicle_list))
        return vehicle_list

    def visit_site(self):
        ad_url_set = set()
        for page_no in range(self.start_page, self.end_page + 1):
            try:
                r = requests.get(self.formatted_url + str(page_no))
                items = SoupStrainer('div', {'class': re.compile('.*ia-cards__items.*')})
                soup = BeautifulSoup(r.content, features="lxml", parse_only=items)
                for a in soup.findAll('a', {'class': re.compile("ia-card__title")}):
                    ad_url_set.add(a.get('href'))
            except():
                logging.error("Specified Website Cannot Be Reached %s" % (self.formatted_url + str(page_no)))
                pass
        return list(ad_url_set)

    @staticmethod
    def extract_vehicle_data(ad_link):

        try:
            img_url_list = []

            r = requests.get(ad_link)

            if r.status_code == 200:
                # Scrape Advertisement Heading
                container_main = SoupStrainer('div', {'class': re.compile('.*v-item__header.*')})
                title_soup = BeautifulSoup(r.content, features="lxml", parse_only=container_main)

                item_top = title_soup.find('h2')

                ad_title = "unknown"
                if item_top is not None:
                    ad_title = item_top.select('span')[0].text.strip()

                # Extract Brand
                brand = "unknown"
                model = "unknown"
                if ad_title != "unknown" is not None:
                    try:
                        brand_model = ad_title.split(',')[0]
                        brand_model_split = brand_model.split(' ', 1)
                        brand = brand_model_split[0].strip()
                        model = brand_model_split[1].strip()
                    except():
                        brand = "unknown"
                        model = "unknown"
                        logging.WARN("Spliting Add Title Failed For %s" % ad_title)
                        pass

                # Scrape Vehicle Info
                item_table = SoupStrainer('table', {'class': re.compile('.*v-item-table.*')})
                item_table_soup = BeautifulSoup(r.content, features="lxml", parse_only=item_table)

                # Extract Model_year
                model_year_elem = item_table_soup.find('td', text=re.compile("Release Year", re.I))
                model_year = "unknown"
                if model_year_elem is not None:
                    model_year = model_year_elem.find_next_sibling("td").find('a').text.strip()

                # Extract Body_Type
                body_type_elem = item_table_soup.find('td', text=re.compile("Body Type"))
                body_type = "unknown"
                if body_type_elem is not None:
                    body_type = body_type_elem.find_next_sibling("td").find('a').text.strip()

                # Scrape All The Image URLS
                gallery_items = SoupStrainer('div', {'class': re.compile('.*v-item__gallery.*')})
                gallery_soup = BeautifulSoup(r.content, features="lxml", parse_only=gallery_items)
                for a in gallery_soup.findAll('a', {'class': 'v-item__gallery__item'}):
                    src_url = a.get('href')
                    img_url_list.append("https:" + src_url)

                return Vehicle(ad_link, ad_title, brand, model, model_year, body_type, img_url_list)
        except():
            logging.error("Error Occurred While Scraping Data from %s" % ad_link)
            pass
