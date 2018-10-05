# ebay-feedsdk-py

[![Build Status](https://travis-ci.org/alessandrozamberletti/ebay-feedsdk-py.svg?branch=master)](https://travis-ci.org/alessandrozamberletti/ebay-feedsdk-py)
[![codecov](https://codecov.io/gh/alessandrozamberletti/ebay-feedsdk-py/branch/master/graph/badge.svg)](https://codecov.io/gh/alessandrozamberletti/ebay-feedsdk-py)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Download item feeds from eBay using Python.

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

Get all items for 'Travel' (3252) category and convert them to pandas dataframe:
```python
import ebayfeed
from pandas import read_table
from pandas.compat import StringIO

# download tsv feed
credentials = ebayfeed.Credentials(client_id, client_secret)
feed = ebayfeed.get_feed(credentials, 3252, ebayfeed.SCOPE_ALL_ACTIVE, ebayfeed.MARKETPLACE_US)

# convert to dataframe
df = read_table(StringIO(tsv_feed.splitlines()))
```

Get items listed on 2018-10-03 for 'Toys & Hobbies' (220) category:
```python
import ebayfeed

# download tsv feed
credentials = ebayfeed.Credentials(client_id, client_secret)
feed = ebayfeed.get_feed(credentials, 220, ebayfeed.SCOPE_NEWLY_LISTED, ebayfeed.MARKETPLACE_DE, date='20181003')
```

Get OAuth 2.0 access token to buy.item.feed scope (cached until expiration):
```python
import ebayfeed

credentials = ebayfeed.Credentials(client_id, client_secret)
access_token = credentials.access_token
```

Connect to eBay sandbox APIs:
```python
import ebayfeed

sandbox_api = ebayfeed.Api(env=ebayfeed.ENVIRONMENT_SANDBOX)

credentials = ebayfeed.Credentials(client_id, client_secret, api=sandbox_api)
feed = ebayfeed.get_feed(credentials, 3252, ebayfeed.SCOPE_ALL_ACTIVE, ebayfeed.MARKETPLACE_US)
```

# References
* eBay API documentation: https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed
* eBay categories map: https://www.isoldwhat.com/
