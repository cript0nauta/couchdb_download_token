import sys
import unittest
from unittest import mock
from . import helpers as test_helpers

from couchdb_download_token import helpers

class TestGetDownloadToken(unittest.TestCase):

    def setUp(self):
        self.test_doc = {
            "_id": "test",
            "_rev": "123",
            "download_token": "abc123"
        }

    def patch_server_and_call(self, server_patch):
        """Mock document retreiving of server_patch and return the
        output of calling get_download_token."""
        get_document_patch = server_patch.__getitem__.return_value.__getitem__
        get_document_patch.return_value = self.test_doc
        return helpers.get_download_token('db', self.test_doc['_id'])

    @mock.patch('couchdb_download_token.helpers.connection')
    def test_retrieves_document(self, server_patch):
        # Mock database and document retrieving
        get_document_patch = server_patch.__getitem__.return_value.__getitem__
        self.patch_server_and_call(server_patch)
        get_document_patch.assert_any_call(self.test_doc['_id'])

    @mock.patch('couchdb_download_token.helpers.connection')
    def test_retrieves_existing_token(self, server_patch):
        # Mock database and document retrieving
        result = self.patch_server_and_call(server_patch)
        self.assertEqual(result, 'abc123')

    @mock.patch('couchdb_download_token.helpers.connection')
    def test_returns_none_with_non_existing_token(self, server_patch):
        # Mock database and document retrieving
        del self.test_doc['download_token']
        result = self.patch_server_and_call(server_patch)
        self.assertIsNone(result)

    @mock.patch('couchdb_download_token.helpers.connection')
    @test_helpers.mock_config('couchdb_download_token.helpers.config',
                              DOWNLOAD_TOKEN_KEY_NAME='token')
    def test_can_change_key_name_in_config(self, server_patch):
        get_document_patch = server_patch.__getitem__.return_value.__getitem__
        document_get_item_patch = get_document_patch.return_value.get
        helpers.get_download_token('db', self.test_doc['_id'])
        document_get_item_patch.assert_any_call('token')
