from .Base import Base
from .SchemaEntry import SchemaEntry
from .Annotation import AnnotationCollection
from .ObjectCollection import ObjectCollection
from .utils import String
import re


class MetadataObject(Base):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("name", String),
            SchemaEntry("description", String),
            SchemaEntry("annotations", AnnotationCollection)
        ]
        super().__init__(self.schema)

    nameLengthMin = 1
    nameLengthMax = 256
    invalidNameRegex = re.compile("^\\s|\\s$")
    descriptionLengthMax = 4000

    def __repr__(self):
        name = getattr(self, "name", None)
        className = self.__class__.__name__
        if name:
            return "<%s '%s'>" % (className, name)
        else:
            return "<%s>" % (className, )
    
    def validate(self):
        if self.name is not None:
            if len(self.name) > self.nameLengthMax or len(self.name) < self.nameLengthMin:
                raise ValueError("Length of %s.name (%d) is not between %d and %d." % (className, len(self.name), self.nameLengthMin, self.nameLengthMax))
            if self.invalidNameRegex.search(self.name):
                raise ValueError("%s.name cannot contain leading or trailing blank spaces or consist only of whitespace." % (className, ))
        if self.description is not None and len(self.description) > self.descriptionLengthMax:
            raise ValueError("Length of %s.description (%d) may not exceed %d." % (className, len(self.name), self.nameLengthMin, self.nameLengthMax))


class MetadataObjectCollection(ObjectCollection):
    def __getitem__(self, index):
        if type(index) == str:
            index = next((i for i, item in enumerate(self) if item.name.lower() == index.lower()), None)
        if index is None:
            return None
        return super(MetadataObjectCollection, self).__getitem__(index)

