class PolymorphicMeta(type):
    classes = {}
    
    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        cls.classes[cls] = {cls.__name__ : cls}
        cls.__appendBases(bases, cls)
        return cls
    
    @staticmethod
    def __appendBases(bases, cls):
        for base in bases:
            basemap = cls.classes.get(base, None)
            if basemap is not None:
                basemap[cls.__name__] = cls
                cls.__appendBases(base.__bases__, cls)

class Polymorphic(metaclass=PolymorphicMeta):
    @classmethod
    def fromJson(cls, value, _=""):
        actualClass = PolymorphicMeta.classes[cls][value["$type"]]
        schema = actualClass().getSchema()
        return super(Polymorphic, actualClass).fromJson(value, schema)

