from copy import deepcopy
from lion_orm.errors import AttributeNotDefinedError


class Field(object):
    CONVERT_TYPES = {
        'STR': 'TEXT',
        'TEXTFIELD': 'TEXT',
        'STRING': 'TEXT',
        'INT': 'INTEGER',
    }
    TYPE_MAPPING = {
        'INTEGER': int,
        'TEXT': str,
    }

    def __init__(self, data_type, null=False, default=None, alarmism=False, required=True, autoincrement=False):
        self.type = self.convert_type(data_type)
        self.nullable = null
        self.default = default
        self.alarmism = alarmism
        self.required = required
        self.autoincrement = autoincrement
        self.filled = False
        self._value = None

    @property
    def value(self):
        pass

    @value.setter
    def value(self, new_value):
        current_type = self.TYPE_MAPPING[self.type]
        if type(new_value) is current_type:
            #print(new_value)
            self._value = new_value
            self.filled = True
        else:
            raise ValueError('incorrect data-type')

    @value.getter
    def value(self):
        if self._value is None and self.alarmism:
            raise AttributeNotDefinedError
        return self._value

    def convert_type(self, data_type):
        if data_type in self.TYPE_MAPPING.values():
            data_type = data_type.__name__
        data_type = data_type.upper()
        if data_type in self.CONVERT_TYPES.keys():
            data_type = self.CONVERT_TYPES[data_type]
        if not (data_type in self.TYPE_MAPPING.keys()):
            raise ValueError
        return data_type

    def copy(self):
        result = deepcopy(self)
        return result

    def __repr__(self):
        return f'<Model-field object, value={self._value}, type={self.type}, filled={self.filled}, autoincrement={self.autoincrement}, required={self.required}, default={self.default}>'
