# -*- coding: utf-8 -*-
import unittest
import time
from tests import client_id, client_secret
from mock import Mock, patch

from ebayfeed.constants import ENVIRONMENT_SANDBOX
from ebayfeed.api import Api
from ebayfeed.credentials import Credentials
from ebayfeed.utils import get_base64_oauth


def mock_response(expires_in=7200):
    mock_rsp = Mock()
    mock_rsp.json = Mock(side_effect=[{'expires_in': expires_in, 'access_token': 'OLD_token'},
                                      {'expires_in': expires_in, 'access_token': 'NEW_token'}])
    mock_rsp.raise_for_status = Mock()
    return mock_rsp


class TestCredentials(unittest.TestCase):
    def setUp(self):
        self.api = Api(env=ENVIRONMENT_SANDBOX)
        self.credentials = Credentials(client_id, client_secret, self.api)

    @patch('ebayfeed.api.requests.post')
    def test_request_is_correct(self, mock_request):
        mock_request.return_value = mock_response()
        # trigger api call
        self.credentials.access_token
        # actual vs expected
        expected_uri = '{}/{}'.format(self.api.uri, 'identity/v1/oauth2/token')
        expected_headers = {'Authorization': 'Basic {}'.format(get_base64_oauth(client_id, client_secret))}
        expected_params = {'grant_type': 'client_credentials',
                           'scope': 'https://api.ebay.com/oauth/api_scope/buy.item.feed'}
        mock_request.assert_called_once_with(expected_uri, headers=expected_headers, params=expected_params)

    @patch('ebayfeed.api.requests.post')
    def test_cache_ttl_works(self, mock_request):
        ttl = 5
        mock_request.return_value = mock_response(expires_in=ttl)
        # query api and load access_token into cache
        self.assertEqual('OLD_token', self.credentials.access_token)
        old_req_ts = self.credentials._req_ts
        # wait for access_token expiration
        time.sleep(ttl)
        # query api and load access_token into cache
        self.assertEqual('NEW_token', self.credentials.access_token)
        self.assertGreater(self.credentials._req_ts, old_req_ts)

    @patch('ebayfeed.api.requests.post')
    def test_invalidate_cache_works(self, mock_request):
        mock_request.return_value = mock_response()
        # query api and load access_token into cache
        self.assertEqual('OLD_token', self.credentials.access_token)
        mock_request.assert_called_once()
        # reset mock
        mock_request.reset_mock()
        # get access_token from cache
        for i in range(10):
            self.assertEqual('OLD_token', self.credentials.access_token)
            mock_request.assert_not_called()
        # invalidate cache
        self.credentials.invalidate_cache()
        # query api and load access_token into cache
        self.assertEqual('NEW_token', self.credentials.access_token)
        mock_request.assert_called_once()


if __name__ == '__main__':
    unittest.main()
