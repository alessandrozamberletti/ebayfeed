# -*- coding: utf-8 -*-
from requests import get, post

from ebayfeed.constants import ENVIRONMENT_PRODUCTION
from ebayfeed.utils import get_api_uri


class Api:
    """
    eBay FeedAPI wrapper.
    """

    def __init__(self, env=ENVIRONMENT_PRODUCTION):
        """
        Create an API object for the given environment.

        Args:
            env (str, optional): eBay environment. Must be one of [ENVIRONMENT_PRODUCTION, ENVIRONMENT_SANDBOX].
                                 Default: EBAY_PRODUCTION.
        """
        self.uri = get_api_uri(env)

    def post(self, route, headers={}, params={}):
        """
        POST request to eBay API.

        Args:
            route (str): API POST route.
            headers (dict, optional): Dictionary of request headers, default empty.
            params (dict, optional): Dictionary of request parameters, default empty.
        """
        rsp = post('{}/{}'.format(self.uri, route), headers=headers, params=params)
        rsp.raise_for_status()
        return rsp

    def get(self, route, headers={}, params={}):
        """
        GET request to eBay API.

        Args:
            route (str): API GET route.
            headers (dict, optional): Dictionary of request headers, default empty.
            params (dict, optional): Dictionary of request parameters, default empty.
        """
        rsp = get('{}/{}'.format(self.uri, route), headers=headers, params=params)
        rsp.raise_for_status()
        return rsp
