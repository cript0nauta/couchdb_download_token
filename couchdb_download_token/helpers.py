"""Some helper functions."""

import couchdb
from . import config

connection = couchdb.Server(config.COUCHDB_URL)

def get_download_token(db_name, document_id):
    """Get the download token of the specified document.

    :returns: The download token or None if it isn't defined.

    """
    database = connection[db_name]
    document = database[document_id]
    return document.get(config.DOWNLOAD_TOKEN_KEY_NAME)
