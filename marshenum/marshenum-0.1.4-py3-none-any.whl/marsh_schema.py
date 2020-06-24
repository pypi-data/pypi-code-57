import attr
from copy import copy
from functools import wraps
import marshmallow as ma
from marshmallow.exceptions import ValidationError
from marshmallow_annotations.ext.attrs import AttrsSchema


def attr_with_schema(**kwargs):
    def decorator(cls):
        schema_meta = getattr(cls, 'SchemaMeta', object)
        fields = attr.fields(cls)
        class Schema(AttrsSchema):
            class Meta(schema_meta):
                locals().update(kwargs)
                target = cls

        for field in fields:
            if field.default == attr.NOTHING:
                Schema._declared_fields[field.name].required = True

        cls.schema = Schema
        Schema.__name__ = cls.__name__ + "Schema"

        def attr_iter(self):
            return iter(self.__dict__.items())

        cls.__iter__ = attr_iter
        return cls
    return decorator


def derive(from_, *, exclude=None):
    if exclude is None:
        exclude = []
    exclude = set(exclude)
    def decorator(cls):
        @wraps(cls, updated=[])
        class Wrapped(cls):
            locals().update({attr.name: attr.default
                             for attr in from_.__attrs_attrs__
                             if attr.name not in exclude})
        Wrapped.__annotations__ = copy(getattr(cls, '__annotations__', {}))
        for k in Wrapped.__annotations__.keys():
            if hasattr(cls, k):
                setattr(Wrapped, k, getattr(cls, k))
        Wrapped.__annotations__.update({attr.name: attr.type
                                        for attr in from_.__attrs_attrs__
                                        if attr.name not in exclude})
        return Wrapped
    return decorator
