from .utils import getattrIgnoreCase
from collections import OrderedDict


class Base(object):

    __ctors = {}

    def __init__(self, schema):
        self.schema = schema
        for entry in schema:
            setattr(self, entry.name, entry.defaultValue)

    def getSchema(self):
        return self.schema

    def toJson(self):
        result = OrderedDict()
        for entry in self.schema:
            element = getattrIgnoreCase(self, entry.name, result)
            if element != result and entry.shouldSerialize(element):
                result[entry.name] = getattr(element, "toJson", lambda: element)()
        result.update(getattrIgnoreCase(self, "customProperties", {}))
        return result

    def validate(self):
        tmp = object()
        className = self.__class__.__name__
        for entry in self.schema:
            element = getattrIgnoreCase(self, entry.name, tmp)
            if element != tmp and element is not None:
                if not isinstance(element, entry.cls):
                    raise TypeError("%s.%s must be of type %s" % (className, entry.name, entry.cls))
                getattr(element, "validate", lambda: None)()

    @classmethod
    def fromJson(cls, value, schema):
        result = cls()
        for entry in schema:
            element = value.pop(entry.name, result)
            if element != result:
                setattr(result, entry.name, cls.__getCtor(entry.cls)(element))
        result.customProperties = value
        return result
    
    @classmethod
    def __getCtor(cls, type):
        ctor = cls.__ctors.get(type, None)
        if not ctor:
            ctor = getattr(type, "fromJson", type)
            cls.__ctors[type] = ctor
        return ctor

