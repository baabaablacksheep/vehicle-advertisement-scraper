from bs4 import BeautifulSoup, SoupStrainer
from src.web_scraper.Vehicle import Vehicle

import re
import requests
import logging


# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class IkmanScraper:
    # website_url = "https://ikman.lk/en/ads/sri-lanka/cars?page=1"
    website_url = "https://ikman.lk/en/ads/sri-lanka/"

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
        return vehicle_list

    def visit_site(self):
        ad_url_set = set()
        for page_no in range(self.start_page, self.end_page + 1):
            try:
                r = requests.get(self.formatted_url + str(page_no))
                if r.status_code == 200:
                    items = SoupStrainer('div', {'class': re.compile('.*item-content.*')})
                    soup = BeautifulSoup(r.content, features="lxml", parse_only=items)
                    for a in soup.findAll('a', {'class': re.compile('.*item-title.*')}):
                        ad_url_set.add("https://ikman.lk" + a.get('href'))
            except:
                logging.error("Specified Website Cannot Be Reached %s" % (self.formatted_url + str(page_no)))
                pass
        return list(ad_url_set)

    # Old visit_site method
    # def visit_site(self):
    #     ad_url_set = set()
    #     for page_no in range(self.start_page, self.end_page + 1):
    #         try:
    #             r = requests.get(self.formatted_url + str(page_no))
    #             if r.status_code == 200:
    #                 items = SoupStrainer('li', {'class': re.compile('.*normal--2QYVk.*')})
    #                 soup = BeautifulSoup(r.content, features="lxml", parse_only=items)
    #                 for a in soup.findAll('a', {'class': re.compile('.*card-link--3ssYv.*', re.I)}):
    #                     if 'promotion' in a:
    #                         continue
    #                     else:
    #                         ad_url_set.add("https://ikman.lk" + a.get('href'))
    #         except:
    #             logging.error("Specified Website Cannot Be Reached %s" % (self.formatted_url + str(page_no)))
    #             pass
    #     return list(ad_url_set)

    @staticmethod
    def extract_vehicle_data(ad_link):

        try:
            img_url_list = []

            r = requests.get(ad_link)

            if r.status_code == 200:
                # Scrape Advertisement Heading
                container_main = SoupStrainer('div', {'class': re.compile('.*container main.*')})
                title_soup = BeautifulSoup(r.content, features="lxml", parse_only=container_main)
                item_top = title_soup.find('div', {'class': re.compile('.*item-top.*')})

                ad_title = "unknown"
                if item_top is not None:
                    ad_title = item_top.select('h1')[0].text.strip()

                # Scrape Vehicle Info
                item_properties = SoupStrainer('div', {'class': re.compile('.*item-properties.*')})
                property_soup = BeautifulSoup(r.content, features="lxml", parse_only=item_properties)

                # Extract Brand
                brand_elem = property_soup.find('dt', text=re.compile("Brand:"))
                brand = "unknown"
                if brand_elem is not None:
                    # print("Brand Tester: " + str(brand_elem.find_next_sibling("dd").contents[0]))
                    brand = brand_elem.find_next_sibling("dd").contents[0]

                # Extract Model
                model_elem = property_soup.find('dt', text=re.compile("Model:"))
                model = "unknown"
                if model_elem is not None:
                    model = model_elem.find_next_sibling("dd").contents[0]

                # Extract Model_year
                model_year_elem = property_soup.find('dt', text=re.compile("Model year:"))
                model_year = "unknown"
                if model_year_elem is not None:
                    model_year = model_year_elem.find_next_sibling("dd").contents[0]

                # Extract Body_Type
                body_type_elem = property_soup.find('dt', text=re.compile("Body type:"))
                body_type = "unknown"
                if body_type_elem is not None:
                    body_type = body_type_elem.find_next_sibling("dd").contents[0]

                # Scrape All The Image URLS
                gallery_items = SoupStrainer('div', {'class': re.compile('.*gallery-item.*')})
                gallery_soup = BeautifulSoup(r.content, features="lxml", parse_only=gallery_items)
                for img in gallery_soup.findAll('img'):
                    src_url = img.get('data-srcset')
                    if "crop" in src_url:
                        continue
                    img_url = src_url.split(" ")[-2]
                    img_url_list.append("https:" + img_url)

                return Vehicle(ad_link, ad_title, brand, model, model_year, body_type, img_url_list)
        except AttributeError:
            logging.error("Error Occurred While Scraping Data from %s Dur To And Attribute Missing Error" % ad_link)
            return None
        except:
            logging.error("Error Occurred While Scraping Data from %s" % ad_link)
            return None
