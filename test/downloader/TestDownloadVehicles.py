from unittest import TestCase
from src.downloader.ImageDownloader import download_vehicles
from src.web_scraper.Vehicle import Vehicle


class TestDownloadVehicles(TestCase):
    def test_download_vehicles(self):
        v1 = Vehicle('https://ikman.lk/en/ad/austin-mini-cooper-rover-1971-for-sale',
                     'Austin MIni Cooper rover 1971',
                     'Austin',
                     'Mini Cooper',
                     '1971',
                     'Hatchback',
                     ['https://i.ikman-st.com/9d05a03b-5223-46aa-aeb3-f954b24220f6/612/459/fitted.webp',
                      'https://i.ikman-st.com/461e332e-f553-4ca3-acd1-075da97a5a38/1224/918/fitted.webp'])
        v2 = Vehicle('unknown',
                     'unknown',
                     'unknown',
                     'unknown',
                     'unknown',
                     'unknown',
                     [])
        download_vehicles([v2, v1], "/tmp")
        # self.fail()
