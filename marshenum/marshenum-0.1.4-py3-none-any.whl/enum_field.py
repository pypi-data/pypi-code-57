from enum import Enum, EnumMeta

from marshmallow import validate, ValidationError
from marshmallow.fields import Field
from marshmallow_annotations import registry


BASE_TYPES = [int, float, str, tuple]


class EnumField(Field):
    default_error_messages = {
        'invalid_value': 'Invalid enum value for {cls}: {inpt}',
        'invalid_type': 'Enum type is invalid: {inpt} is not {enum_type}'
    }

    def __init__(self, cls, *args,
                 dump_by_value=True, load_by_value=True, **kwargs):
        self._enum_cls = cls
        self._enum_type = [_type
                           for _type in BASE_TYPES
                           if issubclass(cls, _type)][0]
        self.dump_by_value = dump_by_value
        self.load_by_value = load_by_value
        kwargs['enum'] = (list(cls._value2member_map_.keys())
                          if load_by_value else cls._member_names_)
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj):
        assert isinstance(value, self._enum_cls)
        return value.value if self.dump_by_value else value.name

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        if not self.load_by_value:
            try:
                return self._enum_cls[value]
            except KeyError:
                self.fail('invalid_value', inpt=value)
            except TypeError:
                self.fail('invalid_type', inpt=value)
        try:
            value = self._enum_type(value)
        except (TypeError, ValueError):
            self.fail('invalid_type', inpt=value)
        try:
            return self._enum_cls._value2member_map_[value]
        except KeyError:
            pass
        except TypeError:
            for k, v in self._enum_cls._value2member_map_.items():
                if v == value:
                    return self._enum_cls[k]
        self.fail('invalid_value', inpt=value)

    def fail(self, key, **kwargs):
        if key in self.default_error_messages:
            msg = self.default_error_messages[key].format(
                inpt=kwargs['inpt'],
                enum_type=self._enum_type.__name__,
                cls=self._enum_cls.__name__)
            raise ValidationError(msg)
        super().fail(key, **kwargs)


class RegisteredEnumMeta(EnumMeta):
    def __new__(metacls, name, bases, cls_dict):
        by_value = cls_dict.pop('__by_value__', True)
        dump_by_value = cls_dict.pop('__dump_by_value__', by_value)
        load_by_value = cls_dict.pop('__load_by_value__', by_value)
        if (not any(base_type in base_cls.mro()
                    for base_cls in bases
                    for base_type in BASE_TYPES)
                and name != 'RegisteredEnum'):
            bases = (str, *bases)
        cls = super().__new__(metacls, name, bases, cls_dict)
        cls.load_by_value = load_by_value
        cls.dump_by_value = dump_by_value
        return cls


class RegisteredEnum(Enum, metaclass=RegisteredEnumMeta):
    def __init_subclass__(cls):
        def _enum_field_converter(converter, subtypes, opts):
            return EnumField(cls,
                             load_by_value=cls.load_by_value,
                             dump_by_value=cls.dump_by_value)

        registry.register(cls, _enum_field_converter)
