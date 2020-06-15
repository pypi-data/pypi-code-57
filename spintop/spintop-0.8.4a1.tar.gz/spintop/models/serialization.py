import dateutil.parser
import pytz

from copy import copy
from typing import Union, NamedTuple
from collections import OrderedDict, defaultdict
from collections.abc import Sequence, Mapping, MappingView
from functools import lru_cache
from datetime import datetime

from marshmallow import Schema, fields, pre_load, post_dump, EXCLUDE, ValidationError

from spintop.utils.marshmallow_dataclass import class_schema
from spintop.utils.marshmallow_oneofschema import OneOfSchema

from spintop.utils import local_tz, isnan, dict_ops


SCHEMA_TYPES = {'json', 'bson'}

_TYPE_TO_CLS_MAP = {}

_TYPE_TO_SCHEMA_BY_TYPE = {schema_type: {} for schema_type in SCHEMA_TYPES}

TYPE_KEY = '_type'

_TYPE_CLS_CHILDREN = defaultdict(set)


def register_type(cls, _type=None, schema_cls=None):
    if _type is None:
        _type = cls.__name__
    cls.__type = _type
    
    if _type in _TYPE_TO_CLS_MAP and _TYPE_TO_CLS_MAP[_type] != cls:
        raise ValueError("Type %s is already registered to class %s" % (_type, _TYPE_TO_CLS_MAP[_type]))

    _TYPE_TO_CLS_MAP[_type] = cls
    for schema_type in _TYPE_TO_SCHEMA_BY_TYPE:
        schema_cls = DataClassSchema(cls, schema_type=schema_type, schema_cls=schema_cls)

        # Building the schema now improves serialization performance by up to 800%
        _TYPE_TO_SCHEMA_BY_TYPE[schema_type][_type] = schema_cls()

    for other_cls in _TYPE_CLS_CHILDREN:
        if other_cls in cls.__mro__:
            _TYPE_CLS_CHILDREN[other_cls].add(cls)
    _TYPE_CLS_CHILDREN[cls] = _TYPE_CLS_CHILDREN[cls]

def cls_subclasses(cls):
    """Returns a set containing the subclasses of cls 
    (if cls was at some point passed to register_type as argument)"""
    return _TYPE_CLS_CHILDREN[cls]

def cls_of_obj(obj):
    if isinstance(obj, Mapping):
        return cls_of_serialized(obj)
    else:
        return obj.__class__
    # try:
    #     _type = type_of(obj)
    #     cls = cls_of_type(_type)
    #     if cls is None:
    #         raise AttributeError(f'{cls} is not mapped to a type')
    #     return cls
    # except AttributeError:
    #     return cls_of_serialized(obj)

def cls_of_serialized(obj_serialized):
    return cls_of_type(serialized_type_of(obj_serialized))

def cls_of_type(_type):
    return _TYPE_TO_CLS_MAP.get(_type, None)

def type_of(cls):
    return cls.__type

def serialized_type_of(obj_serialized):
    return obj_serialized[TYPE_KEY]

def type_dict_of(cls):
    return {TYPE_KEY: type_of(cls)}

def is_type_of(cls, base_cls):
    return type_of(cls) == type_of(base_cls)

def is_serialized_type_of(obj_serialized, base_cls):
    return serialized_type_of(obj_serialized) == type_of(base_cls)

def get_serializer():
    return get_bson_serializer()

def get_bson_serializer():
    return Serializer(get_base_schema_cls('bson'))

def get_json_serializer():
    return Serializer(get_base_schema_cls('json'))

@lru_cache(maxsize=None)
def DataClassSchema(cls, schema_type=None, schema_cls=None):
    base_schema_cls = get_base_schema_cls(schema_type)
    if schema_cls:
        schema_cls = compose_schema_cls(base_schema_cls, schema_cls)
    else:
        schema_cls = base_schema_cls
    schema = class_schema(cls, base_schema=schema_cls)
    return schema

def get_base_schema_cls(schema_type):
    schema_map = {
        'json': JsonCompatSchema,
        'bson': BsonCompatSchema,
        None: JsonCompatSchema # default
    }
    try:
        return schema_map[schema_type]
    except KeyError:
        raise ValueError(f'Schema type {schema_type!r} not in supported list: {schema_map.keys()!r}')

def compose_schema_cls(base, child):
    return type(f'Composed{child.__name__}', (base, child), {})

class Serializer(object):
    def __init__(self, base_schema_cls):
        self.base_schema_cls = base_schema_cls

    def schema(self, *args, **kwargs):
        return self.base_schema_cls(*args, **kwargs)

    def serialize(self, obj):
        master_schema = self.schema()
        try:
            type_of(obj) # Tests if it has a __type attribute.
        except (AttributeError, TypeError):
            return self.serialize_primitive(obj)
        else:
            return master_schema.dump(obj)

    def deserialize(self, obj, cls=None):
        master_schema = self.schema()
        # _type = serialized_type_of(obj)
        if cls:
            # If no type, use cls as default.
            obj.update(type_dict_of(cls))
        return master_schema.load(obj)

    def serialize_primitive(self, obj):
        if isinstance(obj, Sequence) and not isinstance(obj, str):
            return [self.serialize(subobj) for subobj in obj]
        elif isinstance(obj, Mapping):
            return {key: self.serialize(value) for key, value in obj.items()}
        else:
            try:
                Field = self.base_schema_cls.TYPE_MAPPING[type(obj)]
            except KeyError:
                # No mapped field. Return as-is !
                return obj
            field = Field()
            return field._serialize(obj, None, None)

    def deserialize_primitive(self, obj, cls=None):
        if isinstance(obj, Sequence):
            return [self.deserialize(subobj, cls=cls) for subobj in obj]
        elif isinstance(obj, Mapping):
            return {key: self.deserialize(value, cls=cls) for key, value in obj.items()}
        else:
            raise ValueError('Unable to deserialize primitives other than list or dict.')


class NoopField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value

class OrderedDictField(fields.Mapping):
    def _serialize(self, value, attr, obj, **kwargs):
        value_as_dict = dict(value)
        serialized_as_dict = super()._serialize(value_as_dict, attr, obj, **kwargs)
        return [(key, serialized_as_dict[key]) for key in value]

    def _deserialize(self, list_value, attr, data, **kwargs):
        value_as_dict = {key: value for key, value in list_value}
        deserialized_as_dict = super()._deserialize(value_as_dict, attr, data, **kwargs)
        result = OrderedDict()
        for key, _ in list_value:
            result[key] = deserialized_as_dict[key]
        return result

class FloatFieldNoNaN(fields.Float):
    def _serialize(self, value, attr, data, **kwargs):
        if value is None or isnan(value):
            value = None
        num = super()._serialize(value, attr, data, **kwargs)
        return num

class AwareDateTimeDeserializeNoop(fields.AwareDateTime):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, default_timezone=pytz.utc, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value.replace(tzinfo=self.default_timezone)
        else:
            return super()._deserialize(value, attr, data, **kwargs)

def base_type_mapping(additions={}):
    default_type_mapping = copy(Schema.TYPE_MAPPING)
    default_type_mapping.update({
        float: FloatFieldNoNaN,
        OrderedDict: OrderedDictField,
        datetime: AwareDateTimeDeserializeNoop
    })

    try:
        from pandas import Timestamp
    except ImportError:
        pass
    else:
        default_type_mapping.update({
            Timestamp: AwareDateTimeDeserializeNoop
        })

    default_type_mapping.update(additions)
    return default_type_mapping


class AbstractSchema(OneOfSchema):
    class Meta:
        unknown = EXCLUDE

    type_field = TYPE_KEY

    def get_obj_type(self, obj):
        # If a mapping, returns the class from the _type attribute
        # If an object, returns the class itself.
        cls = cls_of_obj(obj) 

        if cls is None:
            return None
        else:
            # Return the string registered to that cls.
            return type_of(cls) 

class JsonCompatSchema(AbstractSchema):
    type_schemas = _TYPE_TO_SCHEMA_BY_TYPE['json']
    TYPE_MAPPING = base_type_mapping()

class BsonCompatSchema(AbstractSchema):
    type_schemas = _TYPE_TO_SCHEMA_BY_TYPE['bson']
    # Bson supports native datetime objects.
    TYPE_MAPPING = base_type_mapping({
        datetime: NoopField # keeps datetime as is
    })

class SerializedWrapper(dict_ops.DictWrapper):
    
    @property
    def type_(self):
        return self[TYPE_KEY]

    @type_.setter
    def type_(self, value):
        self[TYPE_KEY] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

