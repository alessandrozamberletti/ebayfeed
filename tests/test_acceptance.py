# -*- coding: utf-8 -*-
from unittest import TestCase, main
from tests import credentials, a_category, a_marketplace
from datetime import datetime

from ebayfeed.downloader import get_feed
from ebayfeed.categories import get_macro_categories
from ebayfeed.constants import SCOPE_ALL_ACTIVE, SCOPE_NEWLY_LISTED


class TestAcceptance(TestCase):
    def test_get_feed_all_active(self):
        get_feed(credentials, a_category, SCOPE_ALL_ACTIVE, a_marketplace)

    def test_get_feed_newly_listed(self):
        yesterday = datetime.today().strftime("%Y%m%d")
        get_feed(credentials, a_category, SCOPE_NEWLY_LISTED, a_marketplace, date=yesterday)

    def test_get_macro(self):
        get_macro_categories(credentials, a_marketplace)


if __name__ == "__main__":
    main()
