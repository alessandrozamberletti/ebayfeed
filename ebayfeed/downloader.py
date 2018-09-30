# -*- coding: utf-8 -*-
from datetime import datetime

from ebayfeed.constants import FEED_SCOPE_NEWLY_LISTED
from ebayfeed.utils import gunzip


_ROUTE = 'buy/feed/v1_beta/item'


def download_tsv(api, credentials, category, scope, marketplace, date=None, brange=1e+7):
    """
    Download eBay TSV feed for the given category, scope and marketplace using the provided credentials.
    See: https://developer.ebay.com/_api-docs/buy/feed/resources/item/methods/getItemFeed.

    Args:
        api (obj): An Api object used as entry point to Ebay Feed APIs
        credentials (obj): A Credentials object used to obtain an API access_token
        category (int): An eBay top-level category ID of the items to be returned in the feed file.
        scope (str): Feed type to return. Must be one of [FEED_SCOPE_ALL_ACTIVE, FEED_SCOPE_NEWLY_LISTED].
        marketplace (str): The ID for the eBay marketplace where the items are hosted.
        date (str, optional): Date of the feed file to retrieve. Must be within 3-14 days in the past.
                              Format: yyyyMMdd. Ignored when scope is FEED_SCOPE_ALL_ACTIVE.
        brange (int, optional): Number of bytes downloaded at each call to FeedAPI. Must be between 1 and 1e+7.
                                Default: 1e+7 (10mb).

    Returns:
        str: Requested TSV feed in str format.

    Raises:
        ValueError: If scope is FEED_SCOPE_NEWLY_LISTED and date is None.
    """
    if scope == FEED_SCOPE_NEWLY_LISTED and date is None:
        raise ValueError('date must be specified when scope is {}'.format(FEED_SCOPE_NEWLY_LISTED))
    headers, params = _build_req_params(credentials, category, scope, marketplace, date)
    feed_gz = _download_chunks(api, headers, params, int(brange))
    return gunzip(feed_gz)


def _build_req_params(credentials, category, scope, marketplace, date):
    # headers and params for /getItemFeed call
    headers = {
        'X-EBAY-C-MARKETPLACE-ID': marketplace,
        'Authorization': 'Bearer {}'.format(credentials.access_token),
    }
    params = {
        'feed_scope': scope,
        'category_id': category,
    }
    if date:
        _date_format_is_correct(date)
        params['date'] = date
    return headers, params


def _date_format_is_correct(date):
    # check date satisfies yyyyMMdd format, else raise valueError
    datetime.strptime(date, '%Y%m%d')
    return True


def _download_chunks(api, headers, params, brange):
    # download feed chunks and cat them together
    feed_gz = ''
    bstart = 0
    while True:
        headers['Range'] = 'bytes={}-{}'.format(bstart, bstart + brange)
        bstart += brange + 1
        rsp = api.get(_ROUTE, headers, params)
        feed_gz += rsp.content
        feed_length = _get_feed_length(rsp.headers['Content-Range'])
        if bstart >= feed_length or rsp.status_code != 206:
            break
    return feed_gz


def _get_feed_length(content_range):
    # extract feed length (in byte) from response header Content-Range
    return int(content_range.split('/')[-1])
