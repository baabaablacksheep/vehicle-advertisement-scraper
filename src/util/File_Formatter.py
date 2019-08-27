import json
import glob
import os
import re
import shutil


src_directory = '/home/sahan/Projects/Anotation_Project/site_scraped_processed_images/2019-08-26'
dist_directory = '/home/sahan/Projects/Anotation_Project/site_scraped_processed_images/2019-08-26-Restructured'

# Brand List
brand_list = ["toyota","nissan","tata","honda","hyundai","fiat","kia","suzuki","mazda","mitsubishi","peugeot",
"mercedes","ford","lexus","audi","land rover","jaguar","volkswagen","bmw","bajaj","volvo","renault",
"piaggio","leyland","perodua","hero","isuzu","tvs","mini cooper","mahindra","micro", "mini",
"chevrolet","daihatsu","datsun","subaru","chery","daewoo","morris minor","tesla","morris garages",
"zotye","proton", "maruti", "chevrolet", "porsche", "dfsk", "ssangyong", "mg", "chrysler", "citroen", "geely"]

# Helper Functions
def file_formatter(src, target, brand_list):
	counter = 1
	for root, dirs, files in os.walk(src):
		brand = "unknown"
		ad_title = "unknown"
		if os.path.isfile(root + '/vehicle_info.json'):
			with open(root + '/vehicle_info.json') as json_file:
				data = json.load(json_file)
				brand = data['brand']
				ad_title = data['ad_title']
			for file in files:
				if file.endswith('.jpg'):
					brand = brand_categorizer(brand, ad_title, brand_list)
					copy_file(root + "/"+ file,target,brand)

def brand_categorizer(brand, ad_title, brand_list):
	if brand == "unknown":
		brand = next((x for x in brand_list if re.search(x,ad_title, re.I)), "unknown")
	return brand

def generate_folder_struct(path):
	try:
		os.makedirs(path)
	except OSError:
		print("Creation of the directory %s failed" % path)
	else:
		print("Successfully created the directory %s " % path)

def copy_file(file_path, dist_path, brand):
	target_path = dist_path+'/'+brand
	if not os.path.isdir(target_path):
		print("Copying File...")
		print(target_path)
		generate_folder_struct(target_path)
	shutil.copy(file_path, target_path)


file_formatter(src_directory, dist_directory, brand_list)
# Rough Work
# def dir_flattener(src_directory, dist_directory):
# 	counter = 1
# 	for x in os.walk(src_directory):
# 	    path = x[0]
# 	    brand = "unknown"
# 	    ad_title = "unknown"
# 	    if os.path.isfile(path + '/vehicle_info.json'):
# 	        with open(path + '/vehicle_info.json') as json_file:
# 	            data = json.load(json_file)
# 	            brand = data['brand']
# 	            ad_title = data['ad_title']

# 		    for file in glob.glob(path + '/' + '*.jpg'):
# 		    	brand = next((x for x in brand_list if re.search(x,file, re.I)), None)
# 		    	if brand:
# 		    		move_file(src_directory+ "/"+ file,dist_directory,brand)
# 		    	else:
# 		    		move_file(src_directory+ "/"+ file,dist_directory,"unknown")

# 		        new_name = str(counter) + "_" + brand + "_" + ad_title + ".jpg"
# 		        shutil.move(file, dist_directory+'/'+new_name)
# 		        counter+=1



# def move_file(file_path, dist_path, brand):
#     target_path = dist_path+'/'+brand
#     if not os.path.isdir(target_path):
#         generate_folder_struct(target_path)
#     shutil.copy(file_path, target_path)

# def brand_categorizer(src_directory, dist_directory):
# 	for root, dirs, files in os.walk(src_directory):
# 		for file in files:
# 		    if file.endswith('.jpg'):
# 		    	brand = next((x for x in brand_list if re.search(x,file, re.I)), None)
# 		    	if brand:
# 		    		move_file(src_directory+ "/"+ file,dist_directory,brand)
# 		    	else:
# 		    		move_file(src_directory+ "/"+ file,dist_directory,"unknown")