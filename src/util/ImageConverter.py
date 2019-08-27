from PIL import Image


# Convert The Retrieved WEBP file to JPEG
def webp_jpg_converter(src_img_path, output_img_path):
    with Image.open(src_img_path) as im:
        im.convert("RGB").save(output_img_path + ".jpeg", "jpeg")
