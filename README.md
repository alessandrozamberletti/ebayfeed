# ebay-feedsdk-py
Download eBay feeds through Feed APIs using Python.

```python
import ebayfeed

api = ebayfeed.Api(env=ebayfeed.ENVIRONMENT_SANDBOX)
credentials = ebayfeed.Credentials(client_id, client_secret, api)
feed = ebayfeed.download_tsv(api, credentials, category, ebayfeed.FEED_SCOPE_ALL_ACTIVE, ebayfeed.MARKETPLACE_US)
```
