from lion_orm.query import Query
from lion_orm.field import Field
from lion_orm.objects import Objects
from lion_orm.errors import AttributeNotDefinedError, DeleteDeletedError


class Model(object):
    id = Field(int, autoincrement=True)

    def __init__(self, **params):
        if type(self) is Model:
            raise NotImplementedError
        self.fields = self._get_fields()
        for field in self.fields:
            object.__setattr__(self, field, self.fields[field])
        if len(self.fields) == 0:
            raise NotImplementedError
        self._create_table(self.fields)
        object.__setattr__(self, 'id', object.__getattribute__(Model, 'id').copy())
        self.query = Objects(self)
        self.save = self.query._save
        self.filled = False
        self.actual = False
        self.deleted = False
        self.blocked = True
        for parameter in params:
            setattr(self, parameter, params[parameter])

    def delete(self):
        if object.__getattribute__(self, 'deleted'):
            raise DeleteDeletedError
        object.__getattribute__(self, 'query')._delete()
        object.__setattr__(self, 'deleted', True)

    @classmethod
    def _get_fields(cls):
        current = object.__getattribute__(cls, '__dict__')
        result = {}
        for key in current:
            if not hasattr(Model, key):
                value = current[key]
                if isinstance(value, Field):
                    result[key] = value.copy()
        return result

    @classmethod
    def _create_table(cls, fields):
        table_name = cls.__name__
        columns_dict = {x: fields[x].type for x in fields}
        columns_dict['id'] = 'INTEGER'
        Query(table_name).create_table(columns_dict, if_not_exist=True)

    def _fill(self):
        fields = object.__getattribute__(self, 'fields')
        for field in fields.values():
            print(field)
            if not field.filled:
                object.__setattr__(self, 'filled', False)
                return
        object.__setattr__(self, 'filled', True)

    def __setattr__(self, name, value):
        setattr = lambda name, value: object.__setattr__(self, name, value)
        if not hasattr(self, 'blocked'):
            setattr('blocked', False)
        if not self.blocked:
            setattr(name, value)
        else:
            if name == 'id':
                setattr('blocked', False)
                field = self.id
                field.value = value
                setattr('blocked', True)
            elif name in self.fields:
                field = self.fields[name]
                field.value = value
            else:
                setattr(name, value)
            object.__getattribute__(self, '_fill')()

    def __getattribute__(self, name):
        getattr = lambda name: object.__getattribute__(self, name)
        value = getattr(name)
        if type(value) is Field:
            if getattr('blocked'):
                if name == 'id':
                    value = object.__getattribute__(self, name)
                else:
                    value = object.__getattribute__(self, 'fields')[name]
                return value.value
        return value

    def __repr__(self):
        class_name = self.__class__.__name__
        equals = [f'{x}={self.fields[x].value}' for x in self.fields]
        return f'{class_name}({", ".join(equals)})'

    def __str__(self):
        filled = 'filled' if object.__getattribute__(self, 'filled') else 'not filled'
        actual = 'actual' if object.__getattribute__(self, 'actual') else 'not actual'
        deleted = ', deleted' if object.__getattribute__(self, 'deleted') else ''
        return f'<Model object "{self.__class__.__name__}", {filled}, {actual}{deleted}>'
