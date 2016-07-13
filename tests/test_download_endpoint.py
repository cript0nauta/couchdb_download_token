"""Download endpoint unit and integration tests."""

from unittest import mock
from io import BytesIO
from ddt import data, ddt
from falcon.testing import TestCase
from couchdb_download_token import api
from .helpers import ServerPatch


@ddt
@mock.patch('couchdb_download_token.connection', new_callable=ServerPatch)
class TestDownloadResource(TestCase):

    def setUp(self):
        self.api = api

    def simulate_simple_query(self, token='12345', **kwargs):
        return self.simulate_get('/db/doc/file.txt',
                                 query_string='token=%s' % token,
                                 **kwargs)

    def test_gets_correct_attachment(self, server_patch):
        server_patch.set_document()
        res = self.simulate_simple_query()
        self.assertEqual(res.status_code, 200)
        server_patch.database.get_attachment.assert_called_with('doc',
                                                                'file.txt')

    def test_403_if_token_is_invalid(self, server_patch):
        server_patch.set_document()
        res = self.simulate_simple_query('54321')
        self.assertEqual(res.status_code, 403)

    @data(None, 'other=asd')
    def test_403_with_no_token_in_query(self, query_string, server_patch):
        server_patch.set_document()
        res = self.simulate_get('/db/doc/file.txt', query_string=query_string)
        self.assertEqual(res.status_code, 403)

    def test_correct_document_body(self, server_patch):
        server_patch.set_document()
        file_contents = bytes(bytearray(range(256)))  # Test encoding issues
        with BytesIO(file_contents) as fp:
            server_patch.database.get_attachment.return_value = fp
            res = self.simulate_simple_query()
        self.assertEqual(res.content, file_contents)

    def test_correct_content_type(self, server_patch):
        server_patch.set_document(_attachments={
            "file.txt": {"content_type": "custom/type"}})
        res = self.simulate_simple_query()
        self.assertEqual(res.headers['Content-Type'], 'custom/type')
