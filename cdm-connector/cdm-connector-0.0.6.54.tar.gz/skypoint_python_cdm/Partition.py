from .DataObject import DataObject
from .SchemaEntry import SchemaEntry
from .FileFormatSettings import FileFormatSettings
from .MetadataObject import MetadataObjectCollection
from .utils import DateTimeOffset
from .utils import Uri


class Partition(DataObject):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("refreshTime", DateTimeOffset),
            SchemaEntry("location", Uri),
            SchemaEntry("fileFormatSettings", FileFormatSettings)
        ]
        super().__init__(self.schema)


class PartitionCollection(MetadataObjectCollection):
    itemType = Partition
