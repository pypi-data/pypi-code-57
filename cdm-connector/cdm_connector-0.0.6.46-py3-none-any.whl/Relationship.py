from .Base import Base
from .ObjectCollection import ObjectCollection
from .Polymorphic import Polymorphic


class Relationship(Polymorphic, Base):
    def __init__(self, schema=[]):
        super().__init__(schema)



class RelationshipCollection(ObjectCollection):
    itemType = Relationship
