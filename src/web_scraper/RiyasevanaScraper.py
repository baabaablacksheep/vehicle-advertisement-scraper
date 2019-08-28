from bs4 import BeautifulSoup, SoupStrainer
from src.web_scraper.Vehicle import Vehicle

import re
import requests
import logging


# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class RiyasevanaScraper:
    # website_url = "https://riyasewana.com/search/cars?page=2"
    website_url = "https://riyasewana.com/search/"

    def __init__(self, category, start_page, end_page):
        self.category = category
        self.start_page = start_page
        self.end_page = end_page
        self.formatted_url = self.website_url + self.category + "?page="

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
                if r.status_code == 200:
                    items = SoupStrainer('div', {'id': re.compile('.*content.*')})
                    soup = BeautifulSoup(r.content, features="lxml", parse_only=items)
                    for li in soup.findAll('li', {'class': "item round"}):
                        a = li.select('h3')[0].select('a')[0]
                        ad_url_set.add(a.get('href'))
            except:
                logging.error("Specified Website Cannot Be Reached %s" % (self.formatted_url + str(page_no)))
                pass
        return list(ad_url_set)

    @staticmethod
    def extract_vehicle_data(ad_link):

        try:
            img_url_list = []

            r = requests.get(ad_link)

            if r.status_code == 200:
                # Parse The Vehicle Content
                main_content = SoupStrainer('div', {'id': re.compile('.*content.*')})
                main_content_soup = BeautifulSoup(r.content, features="lxml", parse_only=main_content)

                ad_title = "unknown"
                if main_content is not None:
                    # Scrape The Ad Title
                    ad_title = main_content_soup.select('h1')[0].text.strip()

                    # Scrape Vehicle Info
                    info_table = main_content_soup.find('table', {'class': re.compile('.*moret.*')})

                    brand = "unknown"
                    model = "unknown"
                    model_year = "unknown"
                    body_type = "unknown"

                    if info_table is not None:
                        for key_p in info_table.find_all('p'):
                            if re.match("Make", key_p.text, re.I):
                                brand = key_p.parent.find_next_sibling('td').contents[0]
                            elif re.match("Model", key_p.text, re.I):
                                model = key_p.parent.find_next_sibling('td').contents[0]
                            elif re.match("Year", key_p.text, re.I):
                                model_year = key_p.parent.find_next_sibling('td').contents[0]
                            else:
                                continue

                    # Get Body Type From The Ad Title
                    if ad_title != "unknown":
                        body_type = ad_title.split(" ")[-1]

                    # Scrape All The Image URLS
                    gallery_items = main_content_soup.find('div', {'id': 'thumbs'})
                    if gallery_items is not None:
                        for img in gallery_items.findAll('div', {'class': 'thumb'}):
                            img_url = img.select('a')[0].get('href')
                            if "crop" in img_url:
                                continue
                            img_url_list.append(img_url)
                    return Vehicle(ad_link, ad_title, brand, model, model_year, body_type, img_url_list)
        except:
            logging.error("Error Occurred While Scraping Data from %s" % ad_link)
            return None
