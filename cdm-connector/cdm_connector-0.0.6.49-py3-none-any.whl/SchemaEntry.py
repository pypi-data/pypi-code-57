from .ObjectCollection import ObjectCollection
from .utils import Uri


class SchemaEntry(object):

    def __init__(self, name, cls, defaultValue = None):
        self.name = name
        self.cls = cls
        if defaultValue is None and issubclass(cls, list):
            defaultValue = cls()
        self.defaultValue = defaultValue

    def shouldSerialize(self, value):
        if issubclass(self.cls, list):
            return len(value) > 0
        return self.defaultValue != value


class SchemaCollection(ObjectCollection):
    itemType = Uri