# ebay-feedsdk-py
Download eBay feeds through Feed APIs using Python.

```python
import ebayfeed as ebay

api = ebay.Api(env=ebay.ENVIRONMENT_SANDBOX)
credentials = ebay.Credentials(client_id, client_secret, api)
feed = ebay.download_tsv(api, credentials, category, ebay.FEED_SCOPE_ALL_ACTIVE, ebay.MARKETPLACE_US)
```
