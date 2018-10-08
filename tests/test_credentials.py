# -*- coding: utf-8 -*-
from unittest import TestCase, main
from time import sleep
from mock import patch
from tests import client_id, client_secret, api, credentials
from tests.test_commons import mock_response

from ebayfeed.utils import get_base64_oauth


class TestCredentials(TestCase):
    def setUp(self):
        # drop cache
        credentials.invalidate_cache()

    @patch("ebayfeed.api.post")
    def test_request_is_correct(self, mock_request):
        mock_request.return_value = mock_response()
        # trigger api call
        credentials.access_token
        # actual vs expected
        expected_uri = "{}/{}".format(api.uri, "identity/v1/oauth2/token")
        expected_headers = {
            "Authorization": "Basic {}".format(
                get_base64_oauth(client_id, client_secret)
            )
        }
        expected_params = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/buy.item.feed",
        }
        mock_request.assert_called_once_with(
            expected_uri, headers=expected_headers, params=expected_params
        )

    @patch("ebayfeed.api.post")
    def test_cache_ttl_works(self, mock_request):
        ttl = 5
        mock_request.return_value = mock_response(expires_in=ttl)
        # query api and load access_token into cache
        self.assertEqual("OLD_token", credentials.access_token)
        old_req_ts = credentials._req_ts
        # wait for access_token expiration
        sleep(ttl)
        # query api and load access_token into cache
        self.assertEqual("NEW_token", credentials.access_token)
        self.assertGreater(credentials._req_ts, old_req_ts)

    @patch("ebayfeed.api.post")
    def test_invalidate_cache_works(self, mock_request):
        mock_request.return_value = mock_response()
        # query api and load access_token into cache
        self.assertEqual("OLD_token", credentials.access_token)
        mock_request.assert_called_once()
        # reset mock
        mock_request.reset_mock()
        # access_token should be retrieved from cache
        for _ in range(10):
            self.assertEqual("OLD_token", credentials.access_token)
            mock_request.assert_not_called()
        # invalidate cache
        credentials.invalidate_cache()
        # query api and load access_token into cache
        self.assertEqual("NEW_token", credentials.access_token)
        mock_request.assert_called_once()


if __name__ == "__main__":
    main()
