# -*- coding: utf-8 -*-
_CAT_TREE_ID_ROUTE = "commerce/taxonomy/v1_beta/get_default_category_tree_id"
_CAT_TREE_ROUTE = "commerce/taxonomy/v1_beta/category_tree"


def get_macro_categories(credentials, marketplace):
    """
    Retrieve top-level category names and IDs for the given eBay marketplace.
    See: https://developer.ebay.com/api-docs/commerce/taxonomy/static/overview.html.

    Args:
        credentials (obj): A ebayfeed.Credentials object used to obtain an API access_token.
        marketplace (str): The ID of the eBay marketplace for which to retrieve the desired top-level categories.

    Returns:
        dict: Keys are category names, values are category IDs.
    """
    headers = {"Authorization": "Bearer {}".format(credentials.access_token)}
    params = {"marketplace_id": marketplace}
    api = credentials.api
    tree_id = _get_cat_tree_id(api, headers, params)
    tree = _get_cat_tree(api, tree_id, headers)

    return _tree2dict(tree)


def _get_cat_tree_id(api, headers, params):
    # see: https://developer.ebay.com/api-docs/buy/static/buy-categories.html
    rsp = api.get(_CAT_TREE_ID_ROUTE, headers=headers, params=params)
    return rsp.json()["categoryTreeId"]


def _get_cat_tree(api, tree_id, headers):
    # see: https://developer.ebay.com/api-docs/buy/static/buy-categories.html
    tree = api.get("{}/{}".format(_CAT_TREE_ROUTE, tree_id), headers=headers)
    return tree.json()["rootCategoryNode"]["childCategoryTreeNodes"]


def _tree2dict(tree):
    # build a {'category_name': 'category_id'} dict of top-level categories
    return {
        el["category"]["categoryName"]: int(el["category"]["categoryId"]) for el in tree
    }
