# -*- coding: utf-8 -*-
import yaml
import os
from ebayfeed.constants import ENVIRONMENT_SANDBOX
from ebayfeed.api import Api


script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_credentials.yaml')
with open(script_path, 'r') as f:
    config = yaml.load(f)

client_id = config[ENVIRONMENT_SANDBOX]['app-id']
client_secret = config[ENVIRONMENT_SANDBOX]['cert-id']

api = Api(env=ENVIRONMENT_SANDBOX)
