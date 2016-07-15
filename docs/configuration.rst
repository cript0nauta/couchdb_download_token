=============
Configuration
=============

You can set this environment variables in order to configure the
web service:

    - COUCHDB_URL: URL of the CouchDB Server in format `http://user:password@server_url:port`.
                   Should have administrator credentials to access all the attachments and
                   decide which users serve them to.
    - DOWNLOAD_TOKEN_KEY_NAME: Name of the field containing the downlad token of the
                               document. By default it is download_token.
                               If it has dots, the lookup will be nested. For example, if its
                               value is "data.token" the service will get the document token
                               from document['data']['token']. This is useful for using PouchDB
                               which saves the document's data inside a "data" key.
