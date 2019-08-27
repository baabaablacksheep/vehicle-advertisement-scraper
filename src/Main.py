from datetime import date

from src.downloader.ImageDownloader import download_images, download_vehicles
from src.web_scraper.SiteVisitor import SiteVisitor

import configparser
import io

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Variables That'll be Used In The Program
dir_path = config['main']['dir_path']  # "/home/sahan/Projects/Anotation_Project/sl_vehicle_site_scrape"

# Choose from ikman | carmudi | patpat | riyasevana | riyapola | autolanka
web_site_list = []
web_site = config['main']['web_site']
if web_site == "all":
    web_site_list = ['carmudi', 'patpat', 'riyasevana', 'riyapola', 'autolanka']
else:
    web_site_list = [web_site]

# Choose from cars | motorcycles
category = config['main']['category']  # "cars"

# Start and End Page Need to Be Given Since Scraping The Whole Website Could Lead To Some Errors
start_page, end_page = int(config['main']['start_page']), int(config['main']['end_page'])

for web_site in web_site_list:
    vehicles = SiteVisitor(web_site, category, start_page, end_page).get_scraped_data()
    print("Successfully Retrieved Image Urls")
    path = dir_path + "/" + str(date.today()) + "/" + web_site + "/" + category
    download_vehicles(vehicles, path)
