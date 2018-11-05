# -*- coding: utf-8 -*-
# eBay environments
ENVIRONMENT_PRODUCTION = "production"
ENVIRONMENT_SANDBOX = "sandbox"

# feed-enabled marketplaces
EBAY_US = "EBAY-US"
EBAY_GB = "EBAY-GB"
EBAY_DE = "EBAY-DE"

# feed scopes:
# - all_active = all items (new, buy now, trusted)
# - newly_listed = newly listed items for a specific date
SCOPE_ALL_ACTIVE = "ALL_ACTIVE"
SCOPE_NEWLY_LISTED = "NEWLY_LISTED"

# eBay API entry pts
_PRODUCTION_API_URI = "https://api.ebay.com"
_SANDBOX_API_URI = "https://api.sandbox.ebay.com"

# match environments to entry pt
_ENVIRONMENT_TO_API_DICT = {
    ENVIRONMENT_PRODUCTION: _PRODUCTION_API_URI,
    ENVIRONMENT_SANDBOX: _SANDBOX_API_URI,
}

# chunk size
_1MB = 1e6
