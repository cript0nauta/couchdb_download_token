=====
Usage
=====

Run the server
--------------

To start the server, first install the package as described in the installation page.
The API can run in any WSGI server, like Gunicorn::

    $ pip install gunicorn
    $ gunicorn couchdb_download_token:api         
    [2016-07-12 23:33:28 -0300] [7880] [INFO] Starting gunicorn 19.6.0
    [2016-07-12 23:33:28 -0300] [7880] [INFO] Listening at: http://127.0.0.1:8000 (7880)
    [2016-07-12 23:33:28 -0300] [7880] [INFO] Using worker: sync
    [2016-07-12 23:33:28 -0300] [7884] [INFO] Booting worker with pid: 7884

Web API Usage
-------------

.. http:get:: /(str:database_name)/(str:document_id)/(str:attachment_filename)

   Download the attachment `attachment_filename` of the document with id
   `document_id` in database `database_name` if download token matches.

   :query token: download token of the document
   :resheader Content-Type: The content type that specified in the document's
                            attachment metadata
   :statuscode 200: No error, permission granted
   :statuscode 403: Download token mismatch, permission dennied.
                    If there is no token in the document or if it is null a 403
                    error will be raised too.
   :statuscode 404: Attachment not found. Only raised if the token is valid.

