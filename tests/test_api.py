# -*- coding: utf-8 -*-
import unittest
import requests
from mock import patch
from test_mocks import mock_requests
from requests.exceptions import HTTPError

import ebayfeed


def is_alive(uri):
    return requests.get(uri).ok


a_uri = 'a_route'


class TestBase(unittest.TestCase):
    _API = ebayfeed.Api(env=ebayfeed.ENVIRONMENT_SANDBOX)
    _HEADERS = {'headers': 'xyz'}
    _PARAMS = {'params': 'xyz'}

    def test_real_api_are_alive(self):
        self.assertTrue(is_alive(ebayfeed.SANDBOX_API_URI))
        self.assertTrue(is_alive(ebayfeed.PRODUCTION_API_URI))

    @patch('ebayfeed.api.requests.get')
    @patch('ebayfeed.api.requests.post')
    def test_raise_for_status_is_called(self, mock_post, mock_get):
        self._raises_httperror_on(self._API.post, mock_post)
        self._raises_httperror_on(self._API.get, mock_get)

    def _raises_httperror_on(self, req_method, req_mock):
        req_mock.return_value = mock_requests(raise_for_status=HTTPError('i_will_raise_http_error'))
        with self.assertRaises(HTTPError):
            req_method('api_get_route', self._HEADERS, self._PARAMS)

    @patch('ebayfeed.api.requests.post')
    def test_post_route_and_params(self, mock_post):
        mock_post.return_value = mock_requests(content='post')
        self.assertEqual('post', self._API.post(a_uri, self._HEADERS, self._PARAMS).content)
        self._req_params_are_ok(mock_post)

    @patch('ebayfeed.api.requests.get')
    def test_get_route_and_params(self, mock_get):
        mock_get.return_value = mock_requests(content='get')
        self.assertEqual('get', self._API.get(a_uri, self._HEADERS, self._PARAMS).content)
        self._req_params_are_ok(mock_get)

    def _req_params_are_ok(self, mock):
        expected_uri = '{}/{}'.format(self._API.uri, a_uri)
        mock.assert_called_once_with(expected_uri, headers=self._HEADERS, params=self._PARAMS)


if __name__ == '__main__':
    unittest.main()
