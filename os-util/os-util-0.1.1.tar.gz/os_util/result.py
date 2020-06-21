

class Result:

    def __init__(self, ok=None, error=None, data=None, value=None, status=None):
        self._ok = ok
        self._error = error
        self._data = self._set_data(data, value)
        self._status = status

    def __bool__(self):
        return self.bool_state

    def __repr__(self):
        string = f"<Result status:{self.status} | value:'{self.value}'>"
        return string

    @property
    def ok_property(self):
        return self._ok

    @property
    def error_property(self):
        return self._error

    @property
    def data(self):
        return self._data

    @property
    def value(self):
        return self.data

    @property
    def status(self):
        return self._status

    @property
    def bool_state(self):
        if self.ok_property is True or self.error_property is False:
            return True
        elif self.error_property is True or self.ok_property is False:
            return False
        else:
            return None

    def _set_data(self, data, value):

        if data and value:
            raise NotImplementedError

        if data:
            return data
        elif value:
            return value
        else:
            raise NotImplementedError

    @classmethod
    def ok(cls):
        return Result(ok=True)

    @classmethod
    def error(cls):
        return Result(error=True)




