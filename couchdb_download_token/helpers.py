"""Some helper functions."""

import couchdb
from . import config

connection = couchdb.Server(config.COUCHDB_URL)


def get_download_token(document: couchdb.Document):
    """Get the download token of the specified document.

    :returns: The download token or None if it isn't defined.

    """
    return recursive_get(document, config.DOWNLOAD_TOKEN_KEY_NAME)


def recursive_get(dict_, key):
    """Get nested dictionary keys.

    >>> recursive_get({"a": {"b": {"c": "d"}}}, "a.b.c")
    "d"

    Returns None if there are type conflicts.
    """
    keys = key.split('.')
    last = keys.pop(-1)

    dict_ = dict_.copy()
    for key in keys:
        value = dict_.get(key)
        if not isinstance(value, dict):
            return
        dict_ = value
    return dict_.get(last)
