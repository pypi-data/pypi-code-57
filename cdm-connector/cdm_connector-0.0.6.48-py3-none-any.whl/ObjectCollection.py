from .Base import Base

class ObjectCollection(list, Base):
    def append(self, item):
        if not isinstance(item, self.itemType):
            raise TypeError("item is not of type %s" % self.itemType)
        super().append(item)

    def toJson(self):
        result = []
        for item in self:
            result.append(getattr(item, "toJson", lambda: item)())
        return result

    @classmethod
    def fromJson(cls, value):
        result = cls()
        ctor = getattr(cls.itemType, "fromJson", cls.itemType)
        for item in value:
            result.append(ctor(item, cls.itemType().getSchema()))
        return result