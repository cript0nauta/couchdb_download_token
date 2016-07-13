===============================
CouchDB Download Token Service
===============================


.. image:: https://img.shields.io/pypi/v/couchdb_download_token.svg
        :target: https://pypi.python.org/pypi/couchdb_download_token

.. image:: https://img.shields.io/travis/sh4r3m4n/couchdb_download_token.svg
        :target: https://travis-ci.org/sh4r3m4n/couchdb_download_token

.. image:: https://readthedocs.org/projects/couchdb-download-token/badge/?version=latest
        :target: https://couchdb-download-token.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/codecov/c/github/sh4r3m4n/couchdb_download_token.svg
     :target: https://codecov.io/gh/sh4r3m4n/couchdb_download_token
     :alt: Code coverage


Simple web service that allows downloading CouchDB document attachments with a per-document download token.

This project was created with the objetive of provide GET URLs for CouchDB document
attachments without having specify the couch username and password in the URL itself
or in the request headers.

The method I found to do this worrying about permissions is assigning each document a
secret `download_token` field to each document that will have to match when doing
requests to this service.

The service needs to have admin user credentials so it can query all document's
attachments and decide which clients give then. To do this you have to set a
`COUCHDB_URL` environment variable of format 
`http://admin_user:password@server_domain:5984`. By default it uses localhost
with no user credentials.


* Free software: GNU General Public License v3
* Documentation: https://couchdb-download-token.readthedocs.io.


Example usage
-------------

::

    $ pip install couchdb_download_token
    $ pip install gunicorn
    $ gunicorn couchdb_download_token:api         
    [2016-07-12 23:33:28 -0300] [7880] [INFO] Starting gunicorn 19.6.0
    [2016-07-12 23:33:28 -0300] [7880] [INFO] Listening at: http://127.0.0.1:8000 (7880)
    [2016-07-12 23:33:28 -0300] [7880] [INFO] Using worker: sync
    [2016-07-12 23:33:28 -0300] [7884] [INFO] Booting worker with pid: 7884
    $ curl http://localhost:5984/my_database/my_document
    {
        "_id": "my_document",
        "_rev": "4-763e041701ae3e55fd4af08dff93efc4",
        "info": "test document",
        "download_token": "123456",
        "_attachments": {
            "file.txt": {
                "content_type": "text/plain",
                "revpos": 2,
                "digest": "md5-U0f+Rrm7WPnsUGK3oD8t8g==",
                "length": 100,
                "stub": true
            }
        }
    }
    $ curl http://localhost:8000/my_database/my_document/file.txt?token=incorrect
    ...
    < HTTP/1.1 403 Forbidden
    < Server: gunicorn/19.6.0
    ...
    $ curl http://localhost:8000/my_database/my_document/file.txt?token=123456
    ...
    < HTTP/1.1 200 OK
    < Server: gunicorn/19.6.0
    < Date: Wed, 13 Jul 2016 03:02:07 GMT
    < Connection: close
    < Transfer-Encoding: chunked
    < content-type: text/plain
    File contents

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

