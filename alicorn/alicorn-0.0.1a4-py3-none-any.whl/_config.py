#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
import os
from concurrent import futures
from collections import MutableMapping
from .port import InsecurePort


def get_defaults():
    """Returns a default configuration dict with recommended options"""

    return {
        'grpc': {
            'thread_pool': futures.ThreadPoolExecutor(max_workers=1),
            'ports': [
                InsecurePort(host='localhost', port=9000)
            ]
        },
        'debug': True,
        'logging': {
            'level': 'WARNING',
            'format': "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    }


class Config(MutableMapping):
    """A dict-like object used to store alicorn configuration. Configuration is initialised locally when .run()
    is called however there is also a global config as well.

    Configuration is done by means of a nested-dict structure however for convenience keys can be recalled by using
    dot notation. Eg: ['grpc.thread_pool'] instead of ['grpc']['thread_pool'].

    Configuration can be initialised either by environment variables or by a dictionary.
    """

    def __init__(self, defaults=None, global_config=None):
        super(Config, self).__init__()
        self.data = defaults or {}
        if global_config:
            self.data.update(global_config.data)

    def load_from_dict(self, config_dict, prefix=None, _data=None):
        """Load the configuration from a nested dictionary.

        :param config_dict The dictionary to load the configuration from
        :param prefix An optional prefix that this dictionary will be loaded into
        """
        if not _data:
            _data = self.data
            if prefix:
                if prefix not in _data:
                    self.data[prefix] = {}
                _data = self.data[prefix]

        _data.update(config_dict)

    def load_from_environ(self, prefix='ALICORN_', mapping=None):
        """Load configuration from environment variables automatically changing case to lower case
        :param prefix The prefix every environment variable must start with.
        :param mapping A dict or a callable that returns an environment variable name
            (with stripped prefix) to an Alicorn configuration path (eg: grpc.compression).
            If none, then the path is determined by the environment variable's name by replacing double
            underscores with dots.
        """

        for key in filter(lambda k: k.startswith(prefix), os.environ.keys()):
            value = os.getenv(key)
            path = key[len(prefix):].lower()
            if mapping:
                if isinstance(mapping, dict):
                    if path in mapping:
                        self._nested_set(mapping[path], value)
                else:
                    _key = mapping(path)
                    if _key:
                        self._nested_set(_key, value)
            else:
                self._nested_set(path.replace('__', '.'), value)

    def _nested_set(self, key, value):
        """Like set but makes sure the hierarchy exists"""
        data = self.data
        for part in key.split('.')[:-1]:
            if part not in data:
                data[part] = {}
            data = data[part]
        self[key] = value

    def get(self, key, default=None, type=None):
        """Like a normal dict.get() but adds an additional type parameter
        :param key The key to retrieve. Can be dotted notation.
        :param default The default value if the key does not exist
        :param type A callable that converts the value
        """
        if key not in self:
            return default
        elif type is not None:
            return type(self[key])
        else:
            return self[key]

    def set(self, key, value, nested=True):
        """Like a normal dict.set() but adds an additional nested parameter.
        :param key The key to set. Can be dotted notation.
        :param value The value to set
        :param nested If True create nested dicts if they do not already exist
        """
        if nested:
            self._nested_set(key, value)
        else:
            self.__setitem__(key, value)

    def __getitem__(self, key):
        data = self.data
        for part in key.split('.'):
            data = data[part]
        return data

    def __setitem__(self, key, value):
        data = self.data
        parts = key.split('.')
        for part in parts[:-1]:
            data = data[part]
        data[parts[-1]] = value

    def __delitem__(self, key):
        data = self.data
        parts = key.split('.')
        for part in parts[:-1]:
            data = data[part]
        del data[parts[-1]]

    def __contains__(self, key: str):
        data = self.data
        for part in key.split('.'):
            if part not in data:
                return False
            data = data[part]
        return True

    def __len__(self):
        return self.data.__len__()

    def __iter__(self):
        return self.data.__iter__()

    def __repr__(self):
        return self.data.__repr__()


_global_config = Config()
