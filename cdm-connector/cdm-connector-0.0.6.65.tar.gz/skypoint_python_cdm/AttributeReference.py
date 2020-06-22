from .Base import Base
from .SchemaEntry import SchemaEntry
from .utils import String

class AttributeReference(Base):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("entityName", String),
            SchemaEntry("attributeName", String)
        ]
        super().__init__(self.schema)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.entityName == other.entityName and self.attributeName == other.attributeName
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def validate(self):
        super().validate()
        className = self.__class__.__name__
        if not self.entityName:
            raise ValueError("%s.entityName is not set" % (className, ))
        if not self.attributeName:
            raise ValueError("%s.attributeName is not set" % (className, ))

    def getSchema(self):
        return super().getSchema()

    @classmethod
    def fromJson(cls, value):
        schema = AttributeReference().getSchema()
        return super().fromJson(value, schema)