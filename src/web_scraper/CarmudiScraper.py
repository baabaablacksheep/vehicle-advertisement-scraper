import requests

from bs4 import BeautifulSoup, SoupStrainer

import re

from src.web_scraper.Vehicle import Vehicle


class CarmudiScraper:
    # website_url = "https://www.carmudi.lk/cars/?page=2"
    website_url = "https://www.carmudi.lk/"

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
        ad_url_list = []
        for page_no in range(self.start_page, self.end_page + 1):
            try:
                r = requests.get(self.formatted_url + str(page_no))
                if r.status_code == 200:
                    items = SoupStrainer('div', {'class': re.compile('.*card-container.*')})
                    soup = BeautifulSoup(r.content, features="lxml", parse_only=items)
                    for a in soup.findAll('a', {'class': re.compile('.*c-item-title.*')}):
                        ad_url_list.append("https://www.carmudi.lk" + a.get('href'))
            except():
                pass
        return ad_url_list

    def extract_vehicle_data(self, ad_link):

        try:
            img_url_list = []

            r = requests.get(ad_link)
            if r.status_code == 200:
                # Scrape Advertisement Heading
                container_main = SoupStrainer('div', {'class': 'c-listing-title-container'})
                title_soup = BeautifulSoup(r.content, features="lxml", parse_only=container_main)
                item_top = title_soup.find('div')

                # Just Checking isEmpty via find() function
                ad_title = "unknown"
                if item_top is not None:
                    ad_title = title_soup.select('div')[0].text.strip()

                # Scrape All The Image URLS
                gallery_items = SoupStrainer('div', {'class': re.compile('.*c-gallery-main__current.*')})
                gallery_soup = BeautifulSoup(r.content, features="lxml", parse_only=gallery_items)
                for img in gallery_soup.findAll('img'):
                    src_url = img.get("src")
                    if src_url is None:
                        src_url = img.get('data-lazy')
                    img_url_list.append("https:" + src_url)
                return Vehicle(ad_link, ad_title, "unknown", "unknown", "unknown", "unknown", img_url_list)
        except():
            pass
