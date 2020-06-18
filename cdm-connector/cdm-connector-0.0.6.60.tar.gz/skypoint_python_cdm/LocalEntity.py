from .Entity import Entity
from .SchemaEntry import SchemaEntry
from .SchemaEntry import SchemaCollection
from .Attribute import AttributeCollection
from .Partition import PartitionCollection
from .utils import String


class LocalEntity(Entity):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("$type", String, "LocalEntity"),
            SchemaEntry("schemas", SchemaCollection),
            SchemaEntry("attributes", AttributeCollection),
            SchemaEntry("partitions", PartitionCollection)
        ]
        super().__init__(self.schema)

    def toJson(self):
        entity = super().toJson()
        entity["$type"] = "LocalEntity"
        return entity
