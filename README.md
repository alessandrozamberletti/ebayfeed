# ebay-feedsdk-py
Download eBay feeds from FeedAPI using Python.

```python
from ebayfeed import Api, Credentials, get_feed, FEED_SCOPE_ALL_ACTIVE, MARKETPLACE_US

credentials = Credentials(client_id, client_secret, Api())
feed = get_feed(api, credentials, category, FEED_SCOPE_ALL_ACTIVE, MARKETPLACE_US)
```

# References
* eBay API documentation: https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed
* eBay categories map: https://www.isoldwhat.com/
