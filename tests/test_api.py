# -*- coding: utf-8 -*-
import unittest
import requests
from mock import patch
from requests.exceptions import HTTPError
from tests import api, mock_response, a_uri, some_headers, some_params

from ebayfeed import SANDBOX_API_URI, PRODUCTION_API_URI


def is_alive(uri):
    return requests.get(uri).ok


def params_are_as_expected(mock):
    expected_uri = '{}/{}'.format(api.uri, a_uri)
    mock.assert_called_once_with(expected_uri, headers=some_headers, params=some_params)


class TestApi(unittest.TestCase):
    def test_real_api_are_alive(self):
        self.assertTrue(is_alive(SANDBOX_API_URI))
        self.assertTrue(is_alive(PRODUCTION_API_URI))

    @patch('ebayfeed.api.requests.get')
    @patch('ebayfeed.api.requests.post')
    def test_raise_for_status_is_called(self, mock_post, mock_get):
        self._raises_httperror_on(api.post, mock_post)
        self._raises_httperror_on(api.get, mock_get)

    def _raises_httperror_on(self, req_method, req_mock):
        req_mock.return_value = mock_response(raise_for_status=HTTPError('i_will_raise_http_error'))
        with self.assertRaises(HTTPError):
            req_method('api_get_route', some_headers, some_params)

    @patch('ebayfeed.api.requests.post')
    def test_post_route_and_params(self, mock_post):
        mock_post.return_value = mock_response()
        self.assertEqual(200, api.post(a_uri, some_headers, some_params).status_code)
        params_are_as_expected(mock_post)

    @patch('ebayfeed.api.requests.get')
    def test_get_route_and_params(self, mock_get):
        mock_get.return_value = mock_response()
        self.assertEqual(200, api.get(a_uri, some_headers, some_params).status_code)
        params_are_as_expected(mock_get)


if __name__ == '__main__':
    unittest.main()
