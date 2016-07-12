"""Helpers for testing."""

import functools
from unittest import mock

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

