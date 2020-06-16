"""Typing framework for the ARCHICAD JSON interface
"""

from typing import List, Dict, ClassVar, Any, Callable, Union, Optional, Set, Tuple
from enum import Enum, EnumMeta
from uuid import UUID
import abc

_GENERIC_TYPE_ = type(List)

def is_class(typ) -> bool:
    """Returns True if the parameter is a class type
    """
    return isinstance(typ, type) and typ is not type(None)


def is_generic_list(typ) -> bool:
    """Returns True if the parameter is a generic list
    """
    return type(typ) is _GENERIC_TYPE_ and typ.__origin__ is list


def is_union(typ) -> bool:
    return type(typ) is _GENERIC_TYPE_ and typ.__origin__ is Union


def none_constructor(*args, **kwargs) -> None:
    if not args and not kwargs:
        return None
    if len(args) == 1 and len(kwargs) == 0 and args[0] is None:
        return None
    raise TypeError('"None" can\'t be initialized with parameters')


def acbasetype_constructor_wrapper(acbasetyp: type):
    typ = acbasetyp
    def constructor(*args, **kwargs):
        if not args:
            return typ(**dict({k:v for k,v in kwargs.items() if v is not None}))
        if args and kwargs:
            # Ha valaki a sok None-t ki akarja hagyni, előfordulhat ez az eset is.
            # pl: ehelyett: (navigatorItemId, None, myNewId)  
            #     ez:       (navigatorItemId, newId=myNewId)
            return typ(*tuple(arg for arg in args if arg is not None), **dict({k:v for k,v in kwargs.items() if v is not None}))
        if isinstance(args[0], dict):
            return typ(**args[0])
        if isinstance(args[0], typ):
            return args[0]
        if issubclass(typ, _ACUnionType) and type(args[0]) in typ.constructor.optional_types:
            return args[0]
        if not kwargs:
            # Jelenlegi generált kódban tartva van a sorrend,
            # tehát ha a None-okat kiszedjük, akkor probléma mentesen működik.
            return typ(*tuple(arg for arg in args if arg is not None))
        raise TypeError(f'{typ} can\'t be initialized with theese parameters.')
    return constructor


def _get_constructor(typ) -> Callable:
    """Returns the corresponding constructor callable to the type.
    """
    if is_generic_list(typ):
        return _ListBuilder(typ.__args__[0])
    if is_union(typ):
        return _ConstructUnion(typ)
    if is_class(typ):
        if issubclass(typ, _ACBaseType):
            return acbasetype_constructor_wrapper(typ)
        else:
            return typ
    if typ is type(None):
        return none_constructor
    raise NotImplementedError()


class _ListBuilder:
    """A constructor object for the type-annotated generic lists
    """
    def __init__(self, item_type):
        self.constructor = _get_constructor(item_type)

    def __call__(self, items: list):
        assert isinstance(items, list)
        return [self.constructor(item) for item in items]


class _ConstructUnion:
    __slots__ = ('optional_types',)

    def __init__(self, union_type: Union[Any]):
        if is_union(union_type):
            self.optional_types: tuple = union_type.__args__
        elif is_class(union_type):
            self.optional_types = (union_type,)

    def __call__(self, *args, **kwargs):
        valid_results = []
        for one_type in self.optional_types:
            try:
                valid_results.append(_get_constructor(one_type)(*args, **kwargs))
            except Exception as e:
                pass
        if not valid_results:
            raise TypeError("This initialization is not applicable for this union type")
        assert len(valid_results) == 1
        return valid_results[0]


class _ClassInfo:    
    def __init__(self):
        self.fields: Dict[str, Any] = {}
        self.value_validators: Dict[str, Tuple[Callable[[Any], bool], ...]] = {}
        self.instance_validators: Tuple[Callable[[Any], bool], ...] = ()

    def __contains__(self, name: str):
        return name in self.fields

    def add_field(self, field_name: str, field_type: Any, *validators: Callable[[Any], bool]):
        assert field_name not in self
        assert is_class(field_type) or is_generic_list(field_type) or is_union(field_type)
        self.fields[field_name] = field_type
        if validators:
            self.value_validators[field_name] = validators
        
    def is_valid_value(self, name: str, value: Any) -> bool:
        if value is None:
            return True
        return all([validator(value) for validator in self.value_validators.get(name, ())])
    
    def add_instance_validators(self, *validators: Callable[[Any], bool]):
        self.instance_validators = validators
    
    @staticmethod
    def is_valid_instance(obj):
        return all(validator(obj) for validator in obj.get_classinfo().instance_validators)


class _ACBaseType(abc.ABC):
    _class_info: ClassVar[_ClassInfo]

    __slots__ = ()

    @classmethod
    def get_classinfo(cls) -> _ClassInfo:
        """Returns the ClassInfo object of the type. If not exists, it will be created.
        """
        if '_class_info' not in cls.__dict__:
            cls._class_info = _ClassInfo()
        return cls._class_info

    # member functions

    def __setattr__(self, name, value):
        attr_type = self.get_classinfo().fields[name]

        type_match = isinstance(attr_type, type) and isinstance(value, attr_type)
        is_union_instance = (
            (is_union(attr_type) and type(value) in attr_type.__args__) or
            (is_class(attr_type) and issubclass(attr_type, _ACUnionType) and type(value) in attr_type.constructor.optional_types)
        )
        is_actype_with_dict = is_class(attr_type) and issubclass(attr_type, _ACBaseType) and isinstance(value, dict)
        is_list = is_generic_list(attr_type) and isinstance(value, list)
        is_uuid = attr_type is UUID and isinstance(value, str)
        int_to_float = attr_type == float and type(value) == int

        value_to_set = None
        if type_match or is_union_instance:
            value_to_set = value
        elif is_list or is_uuid or is_union(attr_type) or is_actype_with_dict or int_to_float:
            value_to_set = _get_constructor(attr_type)(value)
        else:
            raise TypeError(f'{name} cannot be initialized with {type(value)}')

        if self.get_classinfo().is_valid_value(name, value_to_set):
            super().__setattr__(name, value_to_set)
        else:
            raise ValueError(f"{value} is not allowed for {name}")


    def to_dict(self) -> Dict[str, Any]:
        """Returns the dict representation of the object.
        """
        def deserialize(value):
            if isinstance(value, _ACBaseType):
                return value.to_dict()
            if isinstance(value, UUID):
                return str(value).upper()
            if isinstance(value, list):
                return [deserialize(item) for item in value]
            return value

        return {fieldname: deserialize(self.__getattribute__(fieldname))
                    for fieldname in self.__slots__
                        if self.__getattribute__(fieldname) is not None}

    def __repr__(self):
        return type(self).__name__ + ' ' + str(self.to_dict())

class _ACUnionType(_ACBaseType):
    constructor: _ConstructUnion
