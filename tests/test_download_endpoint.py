"""Download endpoint unit and integration tests."""

from unittest import mock
from io import BytesIO
from ddt import data, ddt
from falcon.testing import TestCase
from couchdb import ResourceNotFound
from couchdb_download_token import api
from .helpers import ServerPatch


@ddt
@mock.patch('couchdb_download_token.connection', new_callable=ServerPatch)
class TestDownloadResource(TestCase):

    def setUp(self):
        self.api = api

    def simulate_simple_query(self, token='12345', status=None,
                              **kwargs):
        res = self.simulate_get('/db/doc/file.txt',
                                query_string='token=%s' % token,
                                **kwargs)
        if status is not None:
            self.assertEqual(res.status_code, status)
        return res

    def test_gets_correct_attachment(self, server_patch):
        server_patch.set_document()
        res = self.simulate_simple_query(status=200)
        server_patch.database.get_attachment.assert_called_with('doc',
                                                                'file.txt')

    def test_403_if_token_is_invalid(self, server_patch):
        server_patch.set_document()
        res = self.simulate_simple_query('54321', 403)

    @data(None, 'other=asd')
    def test_403_with_no_token_in_query(self, query_string, server_patch):
        server_patch.set_document()
        res = self.simulate_get('/db/doc/file.txt', query_string=query_string)
        self.assertEqual(res.status_code, 403)

    @data(None, 'token=12345')
    def test_403_if_no_or_null_token(self, query_string, server_patch):
        server_patch.set_document(download_token=None)
        res = self.simulate_get('/db/doc/file.txt', query_string=query_string)
        self.assertEqual(res.status_code, 403)

        server_patch.reset_mock()
        del server_patch.base_document['download_token']
        server_patch.set_document()

    def test_403_if_invalid_token_and_unexistent_attachment(self,
                                                            server_patch):
        server_patch.database.get_attachment.return_value = None
        server_patch.set_document()
        self.simulate_simple_query('bad', 403)

    def test_404_if_valid_token_and_unexistent_attachment(self,
                                                          server_patch):
        server_patch.database.get_attachment.return_value = None
        server_patch.set_document()
        self.simulate_simple_query(status=404)

    def test_404_in_non_existent_database(self, server_patch):
        server_patch.__getitem__.side_effect = ResourceNotFound()
        res = self.simulate_simple_query(status=404)

    def test_404_in_non_existent_document(self, server_patch):
        server_patch.database.__getitem__.side_effect = ResourceNotFound(
            ('not_found', 'missing'))
        res = self.simulate_simple_query(status=404)

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

    def test_cors(self, server_patch):
        server_patch.set_document()
        res = self.simulate_simple_query(status=200)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'], '*')
