from .MetadataObject import MetadataObject
from .SchemaEntry import SchemaEntry


class DataObject(MetadataObject):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("isHidden", bool, False)
        ]
        super().__init__(self.schema)

    def validate(self):
        super().validate()
        className = self.__class__.__name__
        if self.name is None:
            raise ValueError("%s.name is not set" % (className, ))