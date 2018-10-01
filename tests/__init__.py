# -*- coding: utf-8 -*-
import yaml
import os
from mock import Mock
from tests.test_constants import *

from ebayfeed.constants import ENVIRONMENT_SANDBOX
from ebayfeed.api import Api
from ebayfeed.credentials import Credentials


def mock_response(status_code=200, expires_in=7200, raise_for_status=None):
    mock_rsp = Mock()
    mock_rsp.json = Mock(side_effect=[{'expires_in': expires_in, 'access_token': 'OLD_token'},
                                      {'expires_in': expires_in, 'access_token': 'NEW_token'}])
    mock_rsp.raise_for_status = Mock()
    if raise_for_status:
        mock_rsp.raise_for_status.side_effect = raise_for_status
    mock_rsp.status_code = status_code
    return mock_rsp


def get_test_path(_file):
    tests_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(tests_path, _file)


script_path = get_test_path('test_credentials.yaml')
with open(script_path, 'r') as f:
    config = yaml.load(f)

client_id = config[ENVIRONMENT_SANDBOX]['app-id']
client_secret = config[ENVIRONMENT_SANDBOX]['cert-id']

api = Api(env=ENVIRONMENT_SANDBOX)
credentials = Credentials(client_id, client_secret, api)
