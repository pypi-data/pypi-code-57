from .Base import Base
from .SchemaEntry import SchemaEntry
from .ObjectCollection import ObjectCollection
from .utils import String
from .utils import Uri


class Reference(Base):
    def __init__(self, schema=[]):
        self.schema = schema + (
            SchemaEntry("id", String),
            SchemaEntry("location", Uri)
        )
        super().__init__(self.schema)

class ReferenceCollection(ObjectCollection):
    itemType = Reference