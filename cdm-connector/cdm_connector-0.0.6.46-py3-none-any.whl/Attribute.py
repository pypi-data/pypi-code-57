from .MetadataObject import MetadataObject
from .MetadataObject import MetadataObjectCollection
from .SchemaEntry import SchemaEntry
from .CdmDataType import DataType


class Attribute(MetadataObject):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("dataType", DataType),
        ]
        super().__init__(self.schema)

    def __repr__(self):
        return "<[%s]>" % (getattr(self, "name", "(unnamed)"), )

class AttributeCollection(MetadataObjectCollection):
    itemType = Attribute