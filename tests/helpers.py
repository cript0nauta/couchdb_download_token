"""Helpers for testing."""

import functools
from unittest import mock
from io import BytesIO
from couchdb import Document


class mock_config(object):
    def __init__(self, module_name='couchdb_download_token.config', **kwargs):
        """Change the config variables given in kwargs."""
        self.module_name = module_name
        self.updates = kwargs

    def __call__(self, func):
        @mock.patch(self.module_name)
        @functools.wraps(func)
        def wrapped(self_, config_patch, *args, **kwargs):
            for (key, value) in self.updates.items():
                setattr(config_patch, key, value)
            return func(self_, *args, **kwargs)
        return wrapped


def get_document_patch(server_patch):
    """Get a document patch given a server patch."""
    return server_patch.__getitem__.return_value.__getitem__.return_value


class ServerPatch(mock.MagicMock):
    """Magic mock with helper methods."""

    def __init__(self, *args, **kwargs):
        super(ServerPatch, self).__init__(*args, **kwargs)
        self.base_document = Document({
            "_rev": "123",
            "download_token": "12345"
        })
        self.database.get_attachment.return_value = BytesIO(b'mock')

    def _get_child_mock(self, **kwargs):
        # Define this to avoid RecursionError when setting recursive attributes
        # in __init__
        return mock.MagicMock(**kwargs)

    def set_document(self, **kwargs):
        """Mock the returned document.
        Use self.base_document by default, updated with kwargs."""
        self.base_document.update(kwargs)
        self.__getitem__.return_value.__getitem__.return_value = \
            self.base_document

    @property
    def document(self):
        """Get the document patch."""
        return self.__getitem__.return_value.__getitem__.return_value

    @property
    def database(self):
        """Get the database patch."""
        return self.__getitem__.return_value
