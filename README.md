# ebay-feedsdk-py

[![Build Status](https://travis-ci.org/alessandrozamberletti/ebay-feedsdk-py.svg?branch=master)](https://travis-ci.org/alessandrozamberletti/ebay-feedsdk-py)
[![codecov](https://codecov.io/gh/alessandrozamberletti/ebay-feedsdk-py/branch/master/graph/badge.svg)](https://codecov.io/gh/alessandrozamberletti/ebay-feedsdk-py)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Download item feeds from eBay using Python.

```python
import ebayfeed

credentials = ebayfeed.Credentials(client_id, client_secret)
tsv_feed = ebayfeed.get_feed(credentials, category, ebayfeed.SCOPE_ALL_ACTIVE, ebayfeed.MARKETPLACE_US)
```

# Examples

Transform tsv feed into pandas dataframe:
```python
import ebayfeed
from pandas import read_table
from pandas.compat import StringIO

# download tsv feed
credentials = ebayfeed.Credentials(client_id, client_secret)
tsv_feed = ebayfeed.get_feed(credentials, category, ebayfeed.SCOPE_ALL_ACTIVE, ebayfeed.MARKETPLACE_US)

# convert to pandas dataframe
df_feed = read_table(StringIO(tsv_feed.splitlines()))
```

# References
* eBay API documentation: https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed
* eBay categories map: https://www.isoldwhat.com/
