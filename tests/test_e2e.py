# -*- coding: utf-8 -*-
from unittest import TestCase, main
from tests import credentials, a_category, a_scope, a_marketplace

from ebayfeed import get_feed


class TestE2e(TestCase):
    def test_e2e(self):
        # download feed for a category
        feed = get_feed(credentials, a_category, a_scope, a_marketplace)
        self.assertTrue(len(feed) > 1)


if __name__ == "__main__":
    main()
