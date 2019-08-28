import json
import glob
import os
import re
import shutil

src_directory = '/home/sahan/Projects/Anotation_Project/site_scraped_processed_images/2019-08-26'
dist_directory = '/home/sahan/Projects/Anotation_Project/site_scraped_processed_images/2019-08-26-Restructured'

# Brand List
brand_list = ["toyota", "nissan", "tata", "honda", "hyundai", "fiat", "kia", "suzuki", "mazda", "mitsubishi", "peugeot",
              "mercedes", "ford", "lexus", "audi", "land rover", "jaguar", "volkswagen", "bmw", "bajaj", "volvo",
              "renault",
              "piaggio", "leyland", "perodua", "hero", "isuzu", "tvs", "mini cooper", "mahindra", "micro", "mini",
              "chevrolet", "daihatsu", "datsun", "subaru", "chery", "daewoo", "morris minor", "tesla", "morris garages",
              "zotye", "proton", "maruti", "chevrolet", "porsche", "dfsk", "ssangyong", "mg", "chrysler", "citroen",
              "geely"]


# Helper Functions
def file_formatter(src, target, brands):
    counter = 1
    for root, dirs, files in os.walk(src):
        ad_title = "unknown"
        body_type = "unknown"
        brand = "unknown"
        if os.path.isfile(root + '/vehicle_info.json'):
            with open(root + '/vehicle_info.json') as json_file:
                data = json.load(json_file)
                brand = data['brand']
                ad_title = data['ad_title']
                body_type = data['body_type']
            for file in files:
                if file.endswith('.jpg'):
                    brand = brand_categorizer(brand, ad_title, brands)
                    copy_file(root + "/" + file, target, body_type, brand)


def brand_categorizer(brand, ad_title, brands):
    if brand == "unknown":
        brand = next((x for x in brands if re.search(x, ad_title, re.I)), "unknown")
    return brand


def generate_folder_struct(path):
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def copy_file(file_path, dist_path, body_type, brand):
    target_path = dist_path + '/' + body_type + "/" + brand
    if not os.path.isdir(target_path):
        print("Copying File...")
        print(target_path)
        generate_folder_struct(target_path)
    shutil.copy(file_path, target_path)


# Start Execution
file_formatter(src_directory, dist_directory, brand_list)
