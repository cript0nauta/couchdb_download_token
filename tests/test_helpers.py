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
