# ebay-feedsdk-py
Download eBay feeds from FeedAPI using Python.

```python
import ebayfeed as ebay

api = ebay.Api(env=ebay.ENVIRONMENT_SANDBOX)
credentials = ebay.Credentials(client_id, client_secret, api)
feed = ebay.download_tsv(api, credentials, category, ebay.FEED_SCOPE_ALL_ACTIVE, ebay.MARKETPLACE_US)
```

# References
* eBay API documentation: https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed
