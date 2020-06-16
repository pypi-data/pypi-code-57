import numbers

class MissingAttributeError(Exception):
    def __init__(self, key):
        self._key = key

    def __str__(self):
        return "Missing '%s'" % self._key

class BadValueError(Exception):
    def __init__(self, error):
        self._error = error

    def __str__(self):
        return self._error

class BadAttributeError(Exception):
    def __init__(self, key, value):
        self._key = key
        self._value = value

    def __str__(self):
        return "Attribute '%s' with value %s is of wrong type(%s)" % (self._key, self._value, type(self._value))

def get_field(field, json, type, default = None):
    if field in json:
        value = json[field]
        if type is not None and not isinstance(value, type):
            raise BadAttributeError(field, value)
        else:
            return value
    elif default is not None:
        return default
    else:
        raise MissingAttributeError(field)

def get_int(field, json, default = None):
    return get_field(field, json, int, default)

def get_list(field, json, default = None):
    return get_field(field, json, list, default)

def get_float(field, json, default = None):
    return get_field(field, json, numbers.Number, default)

def get_string(field, json, default = None):
    return get_field(field, json, str, default)

def get_bool(field, json, default = None):
    return get_field(field, json, bool, default)
