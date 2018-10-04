# -*- coding: utf-8 -*-
from os import path
from mock import Mock


def mock_response(status_code=200, expires_in=7200, raise_for_status=None):
    mock_rsp = Mock()
    mock_rsp.json = Mock(
        side_effect=[
            {"expires_in": expires_in, "access_token": "OLD_token"},
            {"expires_in": expires_in, "access_token": "NEW_token"},
        ]
    )
    mock_rsp.raise_for_status = Mock()
    if raise_for_status:
        mock_rsp.raise_for_status.side_effect = raise_for_status
    mock_rsp.status_code = status_code
    return mock_rsp


def get_test_path(_file):
    tests_path = path.dirname(path.realpath(__file__))
    return path.join(tests_path, _file)
