# ebayfeed

[![Build Status](https://travis-ci.org/alessandrozamberletti/ebayfeed.svg?branch=master)](https://travis-ci.org/alessandrozamberletti/ebayfeed)
[![Build status](https://ci.appveyor.com/api/projects/status/ksrptpthfj88pxl7/branch/master?svg=true)](https://ci.appveyor.com/project/alessandrozamberletti/ebay-feedsdk-py/branch/master)
[![codecov](https://codecov.io/gh/alessandrozamberletti/ebayfeed/branch/master/graph/badge.svg)](https://codecov.io/gh/alessandrozamberletti/ebayfeed)
[![PyPI version](https://badge.fury.io/py/ebayfeed.svg)](https://badge.fury.io/py/ebayfeed)
[![Downloads](https://pepy.tech/badge/ebayfeed)](https://pepy.tech/project/ebayfeed)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Download item feeds from eBay RESTful API.

**NOTE:** As of Nov.2018 Feed API ([v1_beta.10.0](https://developer.ebay.com/api-docs/buy/feed/release-notes.html#v1_beta.10.0)) are available only for the following marketplaces:
* EBAY-DE - eBay Germany (ebay.de)
* EBAY-GB - eBay Great Britain (ebay.co.uk)
* EBAY-US - eBay USA (ebay.com)

Package will be updated as soon as [other](https://developer.ebay.com/api-docs/static/rest-request-components.html#Marketpl) marketplaces are added.
More info [here](https://developer.ebay.com/api-docs/buy/feed/overview.html#API).

[Feed API release notes](https://developer.ebay.com/api-docs/buy/feed/release-notes.html)

# Installation
To install, use `pip` or `easy_install`:

```bash
$ pip install --upgrade ebayfeed
```
or
```bash
$ easy_install --upgrade ebayfeed
```

# How to create a keyset

Sign in to your [eBay Developers Program account](https://developer.ebay.com) to create an App ID and a keyset.

**You can test your application in eBay's sandbox environment without limitations.**

To download item feeds from eBay's production environment, your keyset needs to be granted access to https://api.ebay.com/oauth/api_scope/buy.product.feed OAuth scope. 

You can obtain such authorization by completing all the steps described here: [apply for production access](https://developer.ebay.com/api-docs/buy/static/buy-requirements.html#Applying).

# Examples

Get all items for ```{'Travel': 3252}``` category and convert them to pandas dataframe:
```python
import ebayfeed
from pandas import read_table
from pandas.compat import StringIO

# download tsv feed
credentials = ebayfeed.Credentials(client_id, client_secret)
feed = ebayfeed.get_feed(credentials, 3252, ebayfeed.SCOPE_ALL_ACTIVE, ebayfeed.EBAY_US)

# convert to dataframe
df = read_table(StringIO(tsv_feed.splitlines()))
```

Use eBay's sandbox environment instead of production:
```python
sandbox_api = ebayfeed.Api(env=ebayfeed.ENVIRONMENT_SANDBOX)
credentials = ebayfeed.Credentials(client_id, client_secret, api=sandbox_api)
```

Get items listed on 2018-10-03 for ```{'Toys & Hobbies': 220}``` category:
```python
feed = ebayfeed.get_feed(credentials, 220, ebayfeed.SCOPE_NEWLY_LISTED, ebayfeed.EBAY_US, date='20181003')
```

Get top-level category names and IDs for a given marketplace from Taxonomy API:
```python
categories = ebayfeed.get_macro_categories(credentials, ebayfeed.EBAY_DE)
```

Get access token to taxonomy and buy.item.feed OAuth scopes (cached until expiration):
```python
credentials = ebayfeed.Credentials(client_id, client_secret)
access_token = credentials.access_token
```

# References

* FeedAPI documentation: https://developer.ebay.com/api-docs/buy/feed/static/overview.html
* Best practices: https://developer.ebay.com/events/connect17/sj/2-6_breakout_api-best-practices_tanya-vlahovic.pdf
