# ebayfeed

[![Build Status](https://travis-ci.org/alessandrozamberletti/ebayfeed.svg?branch=master)](https://travis-ci.org/alessandrozamberletti/ebayfeed)
[![codecov](https://codecov.io/gh/alessandrozamberletti/ebayfeed/branch/master/graph/badge.svg)](https://codecov.io/gh/alessandrozamberletti/ebayfeed)
[![PyPI version](https://badge.fury.io/py/ebayfeed.svg)](https://badge.fury.io/py/ebayfeed)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Download item feeds from eBay RESTful API.

**NOTE:** As of Oct.2018 Feed API are available only for the following marketplaces:
* EBAY-DE - eBay Germany (ebay.de)
* EBAY-GB - eBay Great Britain (ebay.co.uk)
* EBAY-US - eBay USA (ebay.com)

Package will be updated as soon as [other](https://developer.ebay.com/api-docs/static/rest-request-components.html#Marketpl) marketplaces are added.
More info [here](https://developer.ebay.com/api-docs/buy/feed/overview.html#API).

# Installation
To install, use `pip` or `easy_install`:

```bash
$ pip install --upgrade ebayfeed
```
or
```bash
$ easy_install --upgrade ebayfeed
```

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
access_token = credentials.access_token
```

Use eBay sandbox environment:
```python
sandbox_api = ebayfeed.Api(env=ebayfeed.ENVIRONMENT_SANDBOX)
credentials = ebayfeed.Credentials(client_id, client_secret, api=sandbox_api)
```

# References
* eBay API documentation: https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed
* eBay categories map: https://www.isoldwhat.com/
