import inspect


class ValidationKey:
    __slots__ = ['_validation']

    def __init__(self, validation=None):
        self._validation = None
        if callable(validation):
            signature = inspect.signature(validation)
            if len(signature.parameters) != 1:
                raise ValidationKeyException(
                    "Validation method must have one positional argument")
            self._validation = validation

        elif (isinstance(validation, list) or
              isinstance(validation, dict) or
              isinstance(validation, set)):
            self._validation = set(validation)

        elif isinstance(validation, range):
            self._validation = validation

        elif validation is not None:
            raise ValidationKeyException(
                "Validation must be a method, a enumerable or None")

    def is_valid(self, value) -> bool:
        if not self._validation:
            return True
        if callable(self._validation):
            return self._validation(value)
        return value in self._validation


class ValidationKeyException(Exception):
    pass
