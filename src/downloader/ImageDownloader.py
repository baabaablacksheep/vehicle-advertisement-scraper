from src.util.ImageConverter import webp_jpg_converter
from src.util.UrlReformatter import format_url
from src.writers import DirectoryCreator, VehicleInfoWriter

import io
import requests
import re
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def download_vehicles(vehicle_list, abs_path):
    ad_count = 1
    for vehicle in vehicle_list:
        ad_title = vehicle.ad_title
        if re.match(ad_title, "unknown", re.I):
            continue
        ad_url = format_url(vehicle.ad_url)
        body_type = vehicle.body_type
        dir_path = abs_path + "/" + body_type + "/" + ad_url
        # Creating a Directory To Hold The Data
        DirectoryCreator.generate_folder_struct(dir_path)
        # Create Info File
        VehicleInfoWriter.generate_vehicle_info(dir_path, vehicle)

        print("Ad No: " + str(ad_count))
        print("Start Downloading " + ad_title)
        download_images(vehicle.image_url_list, dir_path, ad_title)
        print("Successfully Downloaded " + ad_title)
        ad_count += 1


def download_images(img_url_list, path, ad_title):
    img_counter = 1
    for img_url in img_url_list:
        try:
            extension = img_url.split(".")[-1]
            ad_title_formatted = ad_title.strip().replace(" ", "_")
            img_path = path + "/" + ad_title_formatted + "_img_" + str(img_counter) + "." + extension
            download_image(img_url, img_path)
            img_counter += 1
        except OSError:
            print("Saving Image Failed in the directory %s" % path)
            logging.error("Saving Image Failed in the directory %s" % path, exc_info=True)
        else:
            print("Saving Image Successful! %s " % path)


def download_image(img_url, path):
    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        if img_url.endswith(".webp"):
            # TODO Make Conversion Consistent By Returning A Byte Stream
            webp_jpg_converter(io.BytesIO(response.content), path)
        else:
            with open(path, 'wb') as f:
                f.write(response.content)
    else:
        logging.error("Image Couldn't Found in the Given URL : %s" % img_url)
    del response
