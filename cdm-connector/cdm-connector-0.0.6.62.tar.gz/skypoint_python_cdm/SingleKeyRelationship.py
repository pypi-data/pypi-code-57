from .Relationship import Relationship
from .SchemaEntry import SchemaEntry
from .AttributeReference import AttributeReference
from .utils import String
from collections import OrderedDict


class SingleKeyRelationship(Relationship):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("$type", String, "SingleKeyRelationship"),
            SchemaEntry("fromAttribute", AttributeReference),
            SchemaEntry("toAttribute", AttributeReference)
        ]
        super().__init__(self.schema)

    def validate(self):
        super().validate()
        className = self.__class__.__name__
        if self.fromAttribute is None:
            raise ValueError("%s.fromAttribute is not set" % (className, ))
        if self.toAttribute is None:
            raise ValueError("%s.toAttribute is not set" % (className, ))
        if self.fromAttribute == self.toAttribute:
            raise ValueError("%s must exist between different attribute references" % (className, ))

    def toJson(self):
        result = OrderedDict()
        result["$type"] = "SingleKeyRelationship"
        entity = super().toJson()
        for k, v in entity.items():
            result[k] = v
        return result
