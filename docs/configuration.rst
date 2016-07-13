=============
Configuration
=============

You can set this environment variables in order to configure the
web service:

    - COUCHDB_URL: URL of the CouchDB Server in format `http://user:password@server_url:port`.
                   Should have administrator credentials to access all the attachments and
                   decide which users serve them to.
    - DOWNLOAD_TOKEN_KEY_NAME: Name of the field containing the downlad token of the
                               document. By default it is download_token
