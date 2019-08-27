from unittest import TestCase

from src.util.UrlReformatter import format_url


class TestUrlReformatter(TestCase):
    def test_reformat_url(self):
        formatted_url = format_url("https://ikman.lk/en/ad/nissan-march-k11-2000-for-sale-kalutara-82")
        assert formatted_url == "en_ad_nissan-march-k11-2000-for-sale-kalutara-82", \
            "%s Should Be Equal to en_ad_nissan-march-k11-2000-for-sale-kalutara-82" % formatted_url
        # self.fail()
