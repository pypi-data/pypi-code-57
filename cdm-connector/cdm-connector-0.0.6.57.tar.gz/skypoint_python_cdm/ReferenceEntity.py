from .Entity import Entity
from .SchemaEntry import SchemaEntry
from .utils import String
from .utils import DateTimeOffset


class ReferenceEntity(Entity):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("$type", String, "ReferenceEntity"),
            SchemaEntry("refreshTime", DateTimeOffset),
            SchemaEntry("source", String),
            SchemaEntry("modelId", String)
        ]
        super().__init__(self.schema)

    def toJson(self):
        entity = super().toJson()
        entity["$type"] = "ReferenceEntity"
        return entity
