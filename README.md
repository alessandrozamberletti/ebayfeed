# ebay-feedsdk-py
[![Build Status](https://travis-ci.org/alessandrozamberletti/ebay-feedsdk-py.svg?branch=master)](https://travis-ci.org/alessandrozamberletti/ebay-feedsdk-py)
[![codecov](https://codecov.io/gh/alessandrozamberletti/ebay-feedsdk-py/branch/master/graph/badge.svg)](https://codecov.io/gh/alessandrozamberletti/ebay-feedsdk-py)

Download item feeds from eBay FeedAPI using Python.

```python
import ebayfeed

credentials = ebayfeed.Credentials(client_id, client_secret)
feed = ebayfeed.get_feed(credentials, category, ebayfeed.SCOPE_ALL_ACTIVE, ebayfeed.MARKETPLACE_US)
```

# References
* eBay API documentation: https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed
* eBay categories map: https://www.isoldwhat.com/
