import unittest
from . import helpers as test_helpers

from couchdb_download_token import helpers


class TestGetDownloadToken(unittest.TestCase):

    def test_retrieves_existing_token(self):
        # Mock database and document retrieving
        result = helpers.get_download_token({"download_token": "abc123"})
        self.assertEqual(result, 'abc123')

    def test_returns_none_with_non_existing_token(self):
        # Mock database and document retrieving
        result = helpers.get_download_token({})
        self.assertIsNone(result)

    @test_helpers.mock_config('couchdb_download_token.helpers.config',
                              DOWNLOAD_TOKEN_KEY_NAME='token')
    def test_can_change_key_name_in_config(self):
        result = helpers.get_download_token({"token": "abc123"})
        self.assertEqual(result, 'abc123')

    @test_helpers.mock_config('couchdb_download_token.helpers.config',
                              DOWNLOAD_TOKEN_KEY_NAME='data.download_token')
    def test_config_with_nested_keys(self):
        result = helpers.get_download_token({"data":{"download_token": "123"}})
        self.assertEqual(result, '123')


class TestRecursiveGet(unittest.TestCase):

    def call_and_assert_equal(self, dict_, key, expected):
        result = helpers.recursive_get(dict_, key)
        self.assertEqual(result, expected)

    def test_retrieves_non_nested_key(self):
        self.call_and_assert_equal({"foo": "bar"}, "foo", "bar")

    def test_retrieves_nested_key(self):
        self.call_and_assert_equal({"a": {"b": {"c": "d"}}}, "a.b.c", "d")

    def test_retrieves_none_in_unexisting_key(self):
        self.call_and_assert_equal({"a": {"b": {"x": "d"}}}, "a.b.c", None)

    def test_retrieves_none_in_failing_nested(self):
        self.call_and_assert_equal({"a": {"b": 5}}, "a.b.c", None)

