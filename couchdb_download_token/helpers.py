"""Some helper functions."""

import couchdb
from . import config

connection = couchdb.Server(config.COUCHDB_URL)


def get_download_token(document: couchdb.Document):
    """Get the download token of the specified document.

    :returns: The download token or None if it isn't defined.

    """
    return document.get(config.DOWNLOAD_TOKEN_KEY_NAME)
