from unittest import TestCase

from src.downloader.ImageDownloader import download_image

import requests
import shutil


class TestDownloadImage(TestCase):
    img_url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"
    test_path = "./out/Example.jpg"

    def test_download_image(self):
        # response = requests.get(self.img_url, stream=True)
        # # with open('/tmp/Example.jpg', 'wb') as out_file:
        # #     shutil.copyfileobj(response.raw, out_file)
        # with open("/tmp/Example.jpg", 'wb') as f:
        #     f.write(response.content)
        # del response
        download_image(self.img_url, self.test_path)
        # self.fail()
