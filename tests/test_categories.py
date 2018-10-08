# -*- coding: utf-8 -*-
from unittest import TestCase, main
from mock import patch, Mock, PropertyMock
from tests import api, credentials
from tests.test_commons import get_test_path
from tests.test_constants import some_headers, some_params, a_marketplace, a_token
from json import load

from ebayfeed.categories import (
    get_top_categories,
    _tree2dict,
    _get_cat_tree_id,
    _get_cat_tree,
    _CAT_TREE_ID_ROUTE,
    _CAT_TREE_ROUTE,
)


class TestCredentials(TestCase):
    def setUp(self):
        script_path = get_test_path("test_categories.json")
        with open(script_path, "r") as f:
            self.cats_tree = load(f)

    def test_tree2dict(self):
        children = self.cats_tree["rootCategoryNode"]["childCategoryTreeNodes"]
        self.assertEqual({"first": 1, "second": 2, "third": 3}, _tree2dict(children))

    @patch("ebayfeed.Api.get")
    def test_get_cat_tree_id(self, mock_api_get):
        mock_api_get.return_value = Mock()
        mock_api_get.return_value.json.return_value = {
            "categoryTreeId": 1,
            "categoryTreeVersion": 2,
        }
        cat_tree_id = _get_cat_tree_id(api, some_headers, some_params)
        mock_api_get.assert_called_once_with(
            _CAT_TREE_ID_ROUTE, headers=some_headers, params=some_params
        )
        self.assertEqual(1, cat_tree_id)

    @patch("ebayfeed.Api.get")
    def test_get_cat_tree(self, mock_api_get):
        mock_api_get.return_value = Mock()
        mock_api_get.return_value.json.return_value = self.cats_tree
        cat_tree = _get_cat_tree(api, 1, some_headers)
        mock_api_get.assert_called_once_with(
            "{}/{}".format(_CAT_TREE_ROUTE, 1), headers=some_headers
        )
        self.assertEqual(
            self.cats_tree["rootCategoryNode"]["childCategoryTreeNodes"], cat_tree
        )

    @patch("ebayfeed.Credentials.access_token", new_callable=PropertyMock)
    @patch("ebayfeed.categories._get_cat_tree_id")
    @patch("ebayfeed.categories._get_cat_tree")
    def test_get_top_categories(
        self, mock_get_cat_tree, mock_get_cat_tree_id, mock_access_token
    ):
        mock_get_cat_tree.return_value = self.cats_tree["rootCategoryNode"][
            "childCategoryTreeNodes"
        ]
        mock_get_cat_tree_id.return_value = 1
        mock_access_token.return_value = a_token
        expected_headers = {"Authorization": "Bearer {}".format(a_token)}
        expected_params = {"marketplace_id": a_marketplace}
        top_categories = get_top_categories(credentials, a_marketplace)
        self.assertEqual({"first": 1, "second": 2, "third": 3}, top_categories)
        mock_access_token.assert_called_once()
        mock_get_cat_tree_id.assert_called_once_with(
            api, expected_headers, expected_params
        )
        mock_get_cat_tree.assert_called_once_with(api, 1, expected_headers)


if __name__ == "__main__":
    main()
