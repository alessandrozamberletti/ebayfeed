# -*- coding: utf-8 -*-
from json import load
from tests.test_commons import get_test_path
from tests.test_constants import *

from ebayfeed.constants import ENVIRONMENT_SANDBOX
from ebayfeed.api import Api
from ebayfeed.credentials import Credentials


script_path = get_test_path('test_credentials.json')
with open(script_path, 'r') as f:
    config = load(f)

client_id = config[ENVIRONMENT_SANDBOX]['app-id']
client_secret = config[ENVIRONMENT_SANDBOX]['cert-id']

api = Api(env=ENVIRONMENT_SANDBOX)
credentials = Credentials(client_id, client_secret, api)
