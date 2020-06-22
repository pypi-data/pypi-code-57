import inspect


class DefaultValue:
    """Default value class for static or callable data
    """

    __slots__ = ['_default_value']

    def __init__(self, default_value):
        if callable(default_value):
            signature = inspect.signature(default_value)
            if len(signature.parameters) > 0:
                raise DefaultValueException(
                    'default value method must have no arguments')

        self._default_value = default_value

    @property
    def value(self):
        if callable(self._default_value):
            return self._default_value()
        return self._default_value


class DefaultValueException(Exception):
    pass
