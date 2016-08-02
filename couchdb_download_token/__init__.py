# -*- coding: utf-8 -*-

import falcon
from .helpers import connection, get_download_token

__author__ = 'Matías Lang'
__email__ = 'yo@matiaslang.me'
__version__ = '0.1.1'


class HTTPForbidden(falcon.HTTPForbidden):
    """403 HTTP Error with the fixed title and description

    I will avoid changing them for security reasons.
    """

    title = "Forbidden"
    description = "Incorrect download token or unexisting document or database"

    def __init__(self, **kwargs):
        super(HTTPForbidden, self).__init__(self.title, self.description,
                                            **kwargs)


class DownloadResource:
    def on_get(self, req, resp, database_name, document_id, filename):
        database = connection[database_name]
        document = database[document_id]
        correct_token = get_download_token(document)

        if correct_token is None or req.params.get('token') != correct_token:
            raise HTTPForbidden()

        attachment = database.get_attachment(document_id, filename)
        if attachment is None:
            raise falcon.HTTPNotFound()
        # If exists document[_attachments][filename] return its content type.
        # If it doesn't (very rare condition, there has to be a change between
        # the execution of the above and below lines) force download
        resp.content_type = (document.get('_attachments', {})
                             .get(filename, {'content_type':
                                             'application/force-download'})
                             ['content_type'])
        resp.stream = attachment

api = falcon.API()
api.add_route('/{database_name}/{document_id}/{filename}', DownloadResource())
