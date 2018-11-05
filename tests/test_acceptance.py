# -*- coding: utf-8 -*-
from unittest import TestCase, main
from tests import credentials
from datetime import datetime

from ebayfeed.downloader import get_feed
from ebayfeed.categories import get_macro_categories
from ebayfeed.constants import SCOPE_ALL_ACTIVE, SCOPE_NEWLY_LISTED, EBAY_US


class TestAcceptance(TestCase):
    def test_get_feed_all_active(self):
        get_feed(credentials, 3252, SCOPE_ALL_ACTIVE, EBAY_US)

    def test_get_feed_newly_listed(self):
        yesterday = datetime.today().strftime("%Y%m%d")
        get_feed(credentials, 3252, SCOPE_NEWLY_LISTED, EBAY_US, date=yesterday)

    def test_get_macro(self):
        get_macro_categories(credentials, EBAY_US)


if __name__ == "__main__":
    main()
