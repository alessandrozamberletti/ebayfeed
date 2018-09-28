# -*- coding: utf-8 -*-
from mock import Mock


def mock_requests(status=200, content='content', raise_for_status=None):
    mock_resp = Mock()
    mock_resp.json = Mock(side_effect=[{'expires_in': 7200, 'access_token': 'access_token'},
                                       {'expires_in': 7200, 'access_token': 'NEW_access_token'}])
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content
    return mock_resp
