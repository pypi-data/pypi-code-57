import inspect

from .config_type import ConfigType


class ConfigClass:

    __slots__ = ['_keys']

    def __init__(self, auto_load: bool = True):

        self._keys = {
            key[0]: ConfigType.from_attribute(key[0], key[1])
            for key in inspect.getmembers(self)
            if not key[0].startswith('_') and not callable(key[1])
        }
        if auto_load:
            self.load()
        else:
            for key in self._keys:
                setattr(self, key, self._keys[key].default_value)

    def description_dict(self) -> dict:
        return {key: str(self._keys[key])
                for key in self._keys}

    def load(self):
        for key in self._keys:
            value = self._keys[key].load()
            setattr(self, key, value)

    def to_dict(self):
        return {key: self._keys[key].value
                for key in self._keys}
