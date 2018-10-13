# -*- coding: utf-8 -*-
from time import time

from ebayfeed.utils import get_base64_oauth
from ebayfeed.api import Api


class Credentials:
    """
    Create access tokens to eBay RESTful API using Client credentials grant flow.
    See: https://developer.ebay.com/_api-docs/static/oauth-client-_credentials-grant.html
    Also: https://developer.ebay.com/events/connect17/sj/2-6_breakout_api-best-practices_tanya-vlahovic.pdf
    """

    _OAUTH2_ROUTE = "identity/v1/oauth2/token"

    # taxonomy and buyItemFeed scopes. See: https://developer.ebay.com/api-docs/static/oauth-details.html
    _PARAMS = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/buy.item.feed",
    }

    def __init__(self, client_id, client_secret, api=Api()):
        """
        Instantiate a new Credentials object by providing keys from https://developer.ebay.com/my/keys.

        Args:
            client_id (str): App-ID (Client-ID) from application keyset.
            client_secret (str): Cert-ID (Client-Secret) from application keyset.
            api (obj, optional): ebayfeed.Api instance. Default: eBay production API.

        Attributes:
            api (obj): ebayfeed.Api instance for which the access token needs to be created (sandbox or production).
        """
        self.api = api
        self._b64 = get_base64_oauth(client_id, client_secret)  # encoded credentials
        self._req_ts = None  # timestamp of last access token api request
        self._access_token = None  # api access_token
        self._ttl = None  # access token expiration time in seconds

    @property
    def access_token(self):
        """
        str: access token to eBay Taxonomy and buyItemFeed OAuth scopes.
             The token is cached until it expires or invalidate_cache() method is called.
        """
        if self._access_token and time() < self._req_ts + self._ttl:
            return self._access_token
        headers = {"Authorization": "Basic {}".format(self._b64)}
        self._req_ts = time()
        rsp = self.api.post(self._OAUTH2_ROUTE, headers, self._PARAMS)
        rsp = rsp.json()
        self._ttl = int(rsp["expires_in"])
        self._access_token = rsp["access_token"]
        return self._access_token

    def invalidate_cache(self):
        """
        Invalidate cache. The next request to access_token property will query eBay to generate a new access token.
        """
        self._access_token = None
