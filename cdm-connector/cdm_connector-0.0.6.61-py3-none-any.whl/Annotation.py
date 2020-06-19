from .Base import Base
from .ObjectCollection import ObjectCollection
from .SchemaEntry import SchemaEntry
from .utils import String


class Annotation(Base):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("name", String),
            SchemaEntry("value", String)
        ]
        super().__init__(self.schema)

class AnnotationCollection(ObjectCollection):
    itemType = Annotation
