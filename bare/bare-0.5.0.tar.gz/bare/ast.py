from enum import Enum, auto
from collections import OrderedDict


class TypeKind(Enum):
    UINT = auto()
    U8 = auto()
    U16 = auto()
    U32 = auto()
    U64 = auto()
    INT = auto()
    I8 = auto()
    I16 = auto()
    I32 = auto()
    I64 = auto()
    F32 = auto()
    F64 = auto()
    Bool = auto()
    String = auto()
    Data = auto()
    DataFixed = auto()
    Void = auto()
    Optional = auto()
    Array = auto()
    ArrayFixed = auto()
    Map = auto()
    TaggedUnion = auto()
    Struct = auto()
    UserType = auto()


class BareType:
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type

    def __repr__(self):
        return '<BareType {}: {} >'.format(self.name, self.type)

    def code(self):
        return 'BareType("{}", {})'.format(self.name, self.type.code())


class BareEnum:
    def __init__(self):
        self.name = None
        self.type = None
        self.values = []

    def __repr__(self):
        result = '<BareEnum {} {}\n'.format(self.name, self.type)
        for value in self.values:
            result += '    ' + repr(value) + '\n'
        return result + '>'

    def code(self):
        return 'BareEnum()'


class BarePrimitive:
    def __init__(self, type, length=None):
        self.type = type
        self.length = length

    def __repr__(self):
        if self.length is None:
            return '<BarePrimitive {}>'.format(self.type)
        else:
            return '<BarePrimitive {}<{}> >'.format(self.type, self.length)

    def code(self):
        if self.length is not None:
            return 'BarePrimitive({}, {})'.format(self.type, self.length)
        else:
            return 'BarePrimitive({})'.format(self.type)


class OptionalType:
    def __init__(self, subtype):
        self.subtype = subtype

    def code(self):
        return 'OptionalType({})'.format(self.subtype.code())


class NamedType:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<NamedType {}>'.format(self.name)

    def code(self):
        return 'NamedType("{}")'.format(self.name)


class StructType:
    def __init__(self, fields=None):
        if fields is None:
            fields = OrderedDict()
        self.fields = fields

    def __repr__(self):
        result = '<StructType\n'
        for key in self.fields:
            type_repr = repr(self.fields[key])
            type_repr = '\n    '.join(type_repr.split('\n'))
            result += '    ' + type_repr + '\n'
        return result + '>'

    def code(self):
        result = 'StructType(OrderedDict(\n'
        for name in self.fields:
            result += '\t{}={},\n'.format(name, self.fields[name].code())
        return result + "))"


class ArrayType:
    def __init__(self, subtype, length=None):
        self.subtype = subtype
        self.length = length

    def __repr__(self):
        if self.length is None:
            return '<ArrayType {}>'.format(self.subtype)
        else:
            return '<ArrayType {}[{}]>'.format(self.subtype, self.length)

    def code(self):
        if self.length is None:
            return 'ArrayType({})'.format(self.subtype.code())
        else:
            return 'ArrayType({}, {})'.format(self.subtype.code(), self.length)


class MapType:
    def __init__(self, keytype, valuetype):
        self.keytype = keytype
        self.valuetype = valuetype

    def __repr__(self):
        return '<MapType [{}] {}>'.format(self.keytype, self.valuetype)

    def code(self):
        return 'MapType({}, {})'.format(self.keytype.code(), self.valuetype.code())


class UnionType:
    def __init__(self, types):
        self.types = types

    def __repr__(self):
        types = map(repr, self.types)
        return '<UnionType ({})>'.format(', '.join(types))

    def code(self):
        types = []
        for t in self.types:
            types.append(t.code())
        return 'UnionType([\n\t\t{}\n\t])'.format(',\n\t\t'.join(types))


class EnumValue:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<EnumValue {}: {}>'.format(self.name, self.value)

    def code(self):
        return 'EnumValue()'


class UnionValue:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return '<UnionValue {}= {}>'.format(self.type, self.value)

    def code(self):
        return 'UnionValue({}, {})'.format(self.type.code(), self.value)
