# ebay-feedsdk-py
Download eBay feeds from FeedAPI using Python.

```python
import ebayfeed as ebay

credentials = ebay.Credentials(client_id, client_secret, ebay.Api())
feed = ebay.get_feed(api, credentials, category, ebay.FEED_SCOPE_ALL_ACTIVE, ebay.MARKETPLACE_US)
```

# References
* eBay API documentation: https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed
* eBay categories map: https://www.isoldwhat.com/
