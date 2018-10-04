# -*- coding: utf-8 -*-
from unittest import TestCase, main
from requests import get
from mock import patch
from requests.exceptions import HTTPError
from tests import api, a_uri, some_headers, some_params
from tests.test_commons import mock_response

from ebayfeed import SANDBOX_API_URI, PRODUCTION_API_URI


def _params_are_as_expected(mock):
    expected_uri = "{}/{}".format(api.uri, a_uri)
    mock.assert_called_once_with(expected_uri, headers=some_headers, params=some_params)


class TestApi(TestCase):
    def test_real_api_are_alive(self):
        def is_alive(uri):
            return get(uri).ok

        self.assertTrue(is_alive(SANDBOX_API_URI))
        self.assertTrue(is_alive(PRODUCTION_API_URI))

    @patch("ebayfeed.api.get")
    @patch("ebayfeed.api.post")
    def test_raise_for_status_is_called(self, mock_post, mock_get):
        self._raises_httperror_on(api.post, mock_post)
        self._raises_httperror_on(api.get, mock_get)

    def _raises_httperror_on(self, req_method, req_mock):
        req_mock.return_value = mock_response(
            raise_for_status=HTTPError("i_raise_http_error")
        )
        with self.assertRaises(HTTPError):
            req_method("api_get_route", some_headers, some_params)

    @patch("ebayfeed.api.get")
    @patch("ebayfeed.api.post")
    def test_get_and_post_route_and_params(self, mock_post, mock_get):
        mock_get.return_value = mock_response(status_code=1)
        mock_post.return_value = mock_response(status_code=2)
        self.assertEqual(1, api.get(a_uri, some_headers, some_params).status_code)
        self.assertEqual(2, api.post(a_uri, some_headers, some_params).status_code)
        _params_are_as_expected(mock_get)
        _params_are_as_expected(mock_post)


if __name__ == "__main__":
    main()
