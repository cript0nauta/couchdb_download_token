import os
COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984')
DOWNLOAD_TOKEN_KEY_NAME = os.environ.get('DOWNLOAD_TOKEN_KEY_NAME',
                                         'download_token')
