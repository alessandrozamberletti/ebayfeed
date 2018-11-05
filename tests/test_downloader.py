# -*- coding: utf-8 -*-
from unittest import TestCase, main
from mock import Mock, patch, PropertyMock
from tests import (
    api,
    credentials,
    a_category,
    a_marketplace,
    a_token,
    a_date,
    a_scope,
    a_range,
    get_test_path,
)
from re import split

from ebayfeed.constants import SCOPE_NEWLY_LISTED, SCOPE_ALL_ACTIVE, EBAY_US, _1MB
from ebayfeed.downloader import (
    get_feed,
    _download_tsv,
    _download_chunks,
    _date_is_correct,
    _build_req_params,
)


def _build_test_req_params(date=None):
    return _build_req_params(credentials, a_category, a_scope, a_marketplace, date)


class TestDownloader(TestCase):
    def setUp(self):
        # drop cache
        credentials.invalidate_cache()
        # load test feed
        with open(get_test_path("test_feed.tsv")) as f:
            self.tsv_feed = f.read()

    def test_raise_for_newly_listed_without_date(self):
        with self.assertRaises(ValueError):
            get_feed(credentials, a_category, SCOPE_NEWLY_LISTED, a_marketplace)

    @patch("ebayfeed.Credentials.access_token", new_callable=PropertyMock)
    def test_req_headers_and_params_are_ok(self, mock_access_token):
        mock_access_token.return_value = a_token
        headers, params = _build_test_req_params(a_date)
        # check headers
        self.assertEqual(2, len(headers))
        self.assertEqual("Bearer {}".format(a_token), headers["Authorization"])
        self.assertEqual(a_marketplace, headers["X-EBAY-C-MARKETPLACE-ID"])
        # check params
        self.assertEqual(3, len(params))
        self.assertEqual(a_category, params["category_id"])
        self.assertEqual(a_scope, params["feed_scope"])
        self.assertEqual(a_date, params["date"])

    @patch("ebayfeed.Credentials.access_token", new_callable=PropertyMock)
    def test_date_ommitted_if_not_given(self, mock_access_token):
        mock_access_token.return_value = a_token
        _, params = _build_test_req_params()
        # check date field is not present
        self.assertEqual(2, len(params))
        self.assertFalse("date" in params)

    @patch("ebayfeed.Api.get")
    def test_read_until_eof(self, mock_api_get):
        feed_length = 10
        fake_rsp = Mock(
            content=b".",
            headers={"Content-Range": "x/{}".format(feed_length)},
            status_code=206,
        )
        mock_api_get.return_value = fake_rsp
        # brange = 0 = advance by 1 each loop -> 10 loops to eof
        _download_chunks(api, {}, {}, 0)
        self.assertEqual(10, mock_api_get.call_count)
        mock_api_get.reset_mock()
        # 10/(1+1) -> 5 loops to eof
        _download_chunks(api, {}, {}, 1)
        self.assertEqual(5, mock_api_get.call_count)
        mock_api_get.reset_mock()
        # 10/(10+1) -> 1 loop to eof
        _download_chunks(api, {}, {}, 10)
        self.assertEqual(1, mock_api_get.call_count)
        mock_api_get.reset_mock()
        # 10/(10000+1) -> 1 loop to eof
        _download_chunks(api, {}, {}, 10000)
        self.assertEqual(1, mock_api_get.call_count)

    @patch("ebayfeed.Api.get")
    def test_respects_status_code(self, mock_api_get):
        fake_rsp = Mock(content=b".", headers={"Content-Range": "x/10"})
        type(fake_rsp).status_code = PropertyMock(side_effect=[206, 206, 401])
        mock_api_get.return_value = fake_rsp
        # 3 loops, stopped by status_code 401
        _download_chunks(api, {}, {}, 0)
        self.assertEqual(3, mock_api_get.call_count)
        mock_api_get.reset_mock()
        # 1 loop is enough to read till eof
        _download_chunks(api, {}, {}, 10)
        self.assertEqual(1, mock_api_get.call_count)

    def test_raise_on_wrong_format_works(self):
        with self.assertRaises(ValueError):
            _date_is_correct("wrong_date_format")
        self.assertTrue(_date_is_correct("20180923"))

    @patch("ebayfeed.Credentials.access_token", new_callable=PropertyMock)
    def test_correct_route_and_params(self, mock_access_token):
        mock_access_token.return_value = a_token
        headers, params = _build_test_req_params()
        mock_access_token.assert_called_once()
        self.assertEqual(
            {
                "Authorization": "Bearer {}".format(a_token),
                "X-EBAY-C-MARKETPLACE-ID": EBAY_US,
            },
            headers,
        )
        self.assertEqual({"category_id": 3252, "feed_scope": SCOPE_ALL_ACTIVE}, params)

    @patch("ebayfeed.Credentials.access_token", new_callable=PropertyMock)
    def test_feed_req_renews_access_token(self, mock_access_token):
        mock_access_token.return_value = a_token
        # should trigger grant_token api call
        _build_test_req_params()
        mock_access_token.assert_called_once()

    @patch("ebayfeed.Credentials.access_token", new_callable=PropertyMock)
    def test_build_req_params_raises_on_wrong_date_format(self, mock_access_token):
        mock_access_token.return_value = a_token
        with self.assertRaises(ValueError):
            _build_test_req_params("wrong_date_format")

    @patch("ebayfeed.downloader._download_tsv", new_callable=PropertyMock)
    def test_get_feed_format(self, mock_download_tsv):
        def correct_call_params(mock):
            mock.assert_called_once_with(
                api, credentials, a_category, a_scope, a_marketplace, None, _1MB
            )

        mock_download_tsv.return_value = self.tsv_feed
        tsv_feed = get_feed(credentials, a_category, a_scope, a_marketplace)
        tsv_feed = tsv_feed.splitlines()
        correct_call_params(mock_download_tsv)
        self.assertTrue(all(isinstance(row, str) for row in tsv_feed))
        self.assertEqual(5, len(tsv_feed))  # includes header
        first_row = split(r"\t+", tsv_feed[1])
        self.assertEqual("NEW", first_row[10])

    @patch("ebayfeed.downloader._build_req_params", new_callable=PropertyMock)
    @patch("ebayfeed.downloader._download_chunks", new_callable=PropertyMock)
    @patch("ebayfeed.downloader.gunzip", new_callable=PropertyMock)
    def test_download_tsv_calls_gunzip(
        self, mock_gunzip, mock_download_chunks, mock_build_req_params
    ):
        mock_build_req_params.return_value = ({}, {})
        mock_download_chunks.return_value = "gunzipped_feed"
        _download_tsv(
            api, credentials, a_category, a_scope, a_marketplace, a_date, a_range
        )
        mock_gunzip.assert_called_once_with("gunzipped_feed")


if __name__ == "__main__":
    main()
