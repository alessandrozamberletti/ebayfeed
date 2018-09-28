# -*- coding: utf-8 -*-
import unittest
from mock import Mock, patch, PropertyMock
from tests import client_id, client_secret

from ebayfeed import *


a_token = 'a_token'
a_category = 267
a_scope = FEED_SCOPE_ALL_ACTIVE
a_marketplace = MARKETPLACE_US
a_date = '20180102'


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.api = Api(env=ENVIRONMENT_SANDBOX)
        self.credentials = Credentials(client_id, client_secret, self.api)

    def test_raise_for_newly_listed_without_date(self):
        with self.assertRaises(ValueError):
            download_tsv(self.api, self.credentials, a_category, FEED_SCOPE_NEWLY_LISTED, a_marketplace)

    @patch('ebayfeed.Credentials.access_token', new_callable=PropertyMock)
    def test_req_headers_and_params_are_ok(self, mock_access_token):
        mock_access_token.return_value = a_token
        headers, params = self._build_req_params(a_date)
        # check headers
        self.assertEqual(2, len(headers))
        self.assertEqual('Bearer {}'.format(a_token), headers['Authorization'])
        self.assertEqual(a_marketplace, headers['X-EBAY-C-MARKETPLACE-ID'])
        # check params
        self.assertEqual(3, len(params))
        self.assertEqual(a_category, params['category_id'])
        self.assertEqual(a_scope, params['feed_scope'])
        self.assertEqual(a_date, params['date'])

    @patch('ebayfeed.Credentials.access_token', new_callable=PropertyMock)
    def test_date_ommitted_if_not_given(self, mock_access_token):
        mock_access_token.return_value = a_token
        _, params = self._build_req_params()
        # check date field is not present
        self.assertEqual(2, len(params))
        self.assertFalse('date' in params)

    @patch('ebayfeed.Api.get')
    def test_read_until_eof(self, mock_api_get):
        feed_length = 10
        fake_rsp = Mock(content='.', headers={'Content-Range': 'x/{}'.format(feed_length)}, status_code=206)
        mock_api_get.return_value = fake_rsp
        # brange = 0 = advance by 1 each loop
        downloader._download_chunks(self.api, {}, {}, 0)
        self.assertEqual(10, mock_api_get.call_count)
        mock_api_get.reset_mock()
        # 10/(1+1) -> 5 loops
        downloader._download_chunks(self.api, {}, {}, 1)
        self.assertEqual(5, mock_api_get.call_count)
        mock_api_get.reset_mock()
        # 10/(10+1) -> 1 loop
        downloader._download_chunks(self.api, {}, {}, 10)
        self.assertEqual(1, mock_api_get.call_count)
        mock_api_get.reset_mock()
        # 10/(10000+1) -> 1 loop
        downloader._download_chunks(self.api, {}, {}, 10000)
        self.assertEqual(1, mock_api_get.call_count)

    @patch('ebayfeed.Api.get')
    def test_respects_status_code(self, mock_api_get):
        fake_rsp = Mock(content='.', headers={'Content-Range': 'x/10'})
        type(fake_rsp).status_code = PropertyMock(side_effect=[206, 206, 401])
        mock_api_get.return_value = fake_rsp
        # 3 loops, stopped by status_code 401
        downloader._download_chunks(self.api, {}, {}, 0)
        self.assertEqual(3, mock_api_get.call_count)
        mock_api_get.reset_mock()
        # 1 loop is enough to read till eof
        downloader._download_chunks(self.api, {}, {}, 10)
        self.assertEqual(1, mock_api_get.call_count)

    def test_raise_on_wrong_format_works(self):
        with self.assertRaises(ValueError):
            downloader._date_format_is_correct('wrong_date_format')
        self.assertTrue(downloader._date_format_is_correct('20180923'))

    @patch('ebayfeed.Credentials.access_token', new_callable=PropertyMock)
    def test_correct_route_and_params(self, mock_access_token):
        mock_access_token.return_value = a_token
        headers, params = self._build_req_params()
        mock_access_token.assert_called_once()
        self.assertEqual({'Authorization': 'Bearer {}'.format(a_token),
                          'X-EBAY-C-MARKETPLACE-ID': MARKETPLACE_US}, headers)
        self.assertEqual({'category_id': 267,
                          'feed_scope': FEED_SCOPE_ALL_ACTIVE}, params)

    @patch('ebayfeed.Credentials.access_token', new_callable=PropertyMock)
    def test_feed_req_renews_access_token(self, mock_access_token):
        mock_access_token.return_value = a_token
        self._build_req_params()
        mock_access_token.assert_called_once()

    @patch('ebayfeed.Credentials.access_token', new_callable=PropertyMock)
    def test_build_req_params_raises_on_wrong_date_format(self, mock_access_token):
        mock_access_token.return_value = a_token
        with self.assertRaises(ValueError):
            self._build_req_params('wrong_date_format')

    def _build_req_params(self, date=None):
        return downloader._build_req_params(self.credentials, a_category, a_scope, a_marketplace, date)


if __name__ == '__main__':
    unittest.main()
