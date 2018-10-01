# -*- coding: utf-8 -*-
# eBay environments
ENVIRONMENT_PRODUCTION = 'production'
ENVIRONMENT_SANDBOX = 'sandbox'

# eBay API entry pts
PRODUCTION_API_URI = 'https://api.ebay.com'
SANDBOX_API_URI = 'https://api.sandbox.ebay.com'

# match environments to entry pt
ENVIRONMENT_TO_API_DICT = {ENVIRONMENT_PRODUCTION: PRODUCTION_API_URI,
                           ENVIRONMENT_SANDBOX: SANDBOX_API_URI}

# currently available marketplaces
MARKETPLACE_US = 'EBAY-US'
MARKETPLACE_GB = 'EBAY-GB'
MARKETPLACE_DE = 'EBAY-DE'

# feed scopes:
# - all_active = all items (new, buy now, trusted)
# - newly_listed = newly listed items for a specific date
SCOPE_ALL_ACTIVE = 'ALL_ACTIVE'
SCOPE_NEWLY_LISTED = 'NEWLY_LISTED'

# feed formats
FORMAT_TSV = 'TSV'
FORMAT_DATAFRAME = 'DATAFRAME'

# chunk size
MB10 = 1e+7
