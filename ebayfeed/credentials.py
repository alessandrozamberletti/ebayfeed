# -*- coding: utf-8 -*-
from time import time

from ebayfeed.utils import get_base64_oauth
from ebayfeed.api import Api


class Credentials:
    """
    Grant access_token to Ebay sandbox and production FeedAPI by following the client credentials grant flow.
    See: https://developer.ebay.com/_api-docs/static/oauth-client-_credentials-grant.html
    """
    _OAUTH2_ROUTE = 'identity/v1/oauth2/token'
    _PARAMS = {'grant_type': 'client_credentials',
               'scope': 'https://api.ebay.com/oauth/api_scope/buy.item.feed'}

    def __init__(self, client_id, client_secret, api=Api()):
        """
        Instantiate a new Credentials object by providing keys from https://developer.ebay.com/my/keys.

        Args:
            client_id (str): App-ID (Client-ID) from application keyset.
            client_secret (str): Cert-ID (Client-Secret) from application keyset.
            api (obj, optional): ebayfeed.Api instance. Default: eBay production API.
        """
        self._b64 = get_base64_oauth(client_id, client_secret)
        self._api = api  #: _api access pt
        self._req_ts = None  #: timestamp of last access token _api request
        self._access_token = None  #: _api access_token
        self._ttl = None  #: access token expiration time in seconds

    @property
    def access_token(self):
        """
        str: OAuth access token to eBay FeedAPI (scope: https://_api.ebay.com/oauth/api_scope/buy.item.feed).
             The token is cached until it expires or invalidate_cache() method is called.
        """
        if self._access_token and time() < self._req_ts + self._ttl:
            return self._access_token
        headers = {'Authorization': 'Basic {}'.format(self._b64)}
        self._req_ts = time()
        rsp = self._api.post(self._OAUTH2_ROUTE, headers, self._PARAMS)
        rsp = rsp.json()
        self._ttl = int(rsp['expires_in'])
        self._access_token = rsp['access_token']
        return self._access_token

    def invalidate_cache(self):
        """
        Invalidate cache. The next request to access_token property will query Ebay FeedAPI to generate a new
        access token.
        """
        self._access_token = None
