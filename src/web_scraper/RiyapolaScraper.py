from bs4 import BeautifulSoup, SoupStrainer
from src.web_scraper.Vehicle import Vehicle

import logging
import re
import requests


class RiyapolaScraper:
    # website_url = "http://riyapola.com/vehicles/cars/2"
    website_url = "http://riyapola.com/vehicles/"

    def __init__(self, category, start_page, end_page):
        self.category = category
        self.start_page = start_page
        self.end_page = end_page
        self.formatted_url = self.website_url + self.category + "/"

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
                    items = SoupStrainer('div', {'class': re.compile('.*item.*')})
                    soup = BeautifulSoup(r.content, features="lxml", parse_only=items)
                    for a in soup.findAll('a', {'class': "image-wrapper"}):
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
                # Scrape Advertisement Heading
                container_header = SoupStrainer('div', {'class': re.compile('.*container clearfix.*')})
                header_soup = BeautifulSoup(r.content, features="lxml", parse_only=container_header)
                google_ad = header_soup.find('div', {'class': re.compile('.*divSpacer.*')})

                ad_title = "unknown"
                if google_ad is not None:
                    ad_title = google_ad.parent \
                        .find_next_sibling("div") \
                        .find('h1') \
                        .contents[0] \
                        .strip()

                # Scrape Vehicle Info
                brand = "unknown"
                model = "unknown"
                model_year = "unknown"
                body_type = "unknown"

                item_properties = SoupStrainer('section', {'class': re.compile('.*box.*')})
                property_soup = BeautifulSoup(r.content, features="lxml", parse_only=item_properties)

                custom_fields_elem = property_soup.find('div', {'id': 'custom_fields'})
                if custom_fields_elem is not None:
                    table_elem = custom_fields_elem.find_next_sibling("table")
                    if table_elem is not None:
                        # Extract Brand
                        brand_elem = property_soup.find('label', text=re.compile("Make", re.I))
                        if brand_elem is not None:
                            brand = brand_elem.parent.find_next_sibling("td").contents[0]

                        # Extract Model
                        model_elem = property_soup.find('label', text=re.compile("Model", re.I))
                        if model_elem is not None:
                            model = model_elem.parent.find_next_sibling("td").contents[0]

                        # Extract Model_year
                        model_year_elem = property_soup.find('label', text=re.compile("Year", re.I))
                        if model_year_elem is not None:
                            model_year = model_year_elem.parent.find_next_sibling("td").contents[0]

                        # Extract Body_Type
                        body_type_elem = property_soup.find('label', text=re.compile("Car type", re.I))
                        if body_type_elem is not None:
                            body_type = body_type_elem.parent.find_next_sibling("td").contents[0]

                # Scrape All The Image URLS
                gallery_items = SoupStrainer('div', {'class': re.compile('.*gallery-carousel-thumbs.*')})
                gallery_soup = BeautifulSoup(r.content, features="lxml", parse_only=gallery_items)
                for img in gallery_soup.findAll('img'):
                    src_url = img.get('src')
                #     if "crop" in src_url:
                #         continue
                #     img_url = src_url.split(" ")[-2]
                    img_url_list.append(src_url)

                return Vehicle(ad_link, ad_title, brand, model, model_year, body_type, img_url_list)
        except:
            logging.error("Error Occurred While Scraping Data from %s" % ad_link)
            return None
