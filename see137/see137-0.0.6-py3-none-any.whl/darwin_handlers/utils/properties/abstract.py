from typing import Optional
from loguru import logger
from jamboree import DBHandler


class MetaProperty:
    """
        NOTE: Needs to have schemas to bring out the full power of this.
        This is to interact with the properties of the individual items with a single builder pattern. 
        It should reduce amount of code directly on each object.
    """


    def __init__(self) -> None:
        self._alt = {}
        self.dbhand:Optional[DBHandler] = None
        self._schema = {}
        self._default_type_mapping = {
            int: 0,
            float: 0.0,
            str: "",
            dict: {},
            list: [],
        }


    @property
    def schema(self) -> dict:
        return self._schema

    @schema.setter
    def schema(self, _schema:dict):
        if self.is_all_type_vals(_schema):
            self._schema = _schema

    @property
    def is_schema(self) -> bool:
        lll = len(self.schema.keys())
        if lll == 0: False 
        return True


    @property
    def default_dict(self):
        schema_keys = list(self.schema.keys())
        default_keys = list(self._default_type_mapping.keys())
        defaults = {}
        if len(schema_keys) == 0: return defaults
        for skey, sval in self.schema.items():
            if sval not in default_keys:
                defaults[skey] = 0
            else:
                defaults[skey] = self._default_type_mapping[sval]
        return defaults


    def is_all_type_vals(self, _schema:dict):
        for sval in _schema.values():
            type_cast = type(sval)
            is_typing = isinstance(type_cast, type)
            if is_typing:
                return False
        return True

    def validate_schema(self, item:dict) -> bool:
        if self.is_schema: return True
        for skey, sval in self.schema.items():
            if skey not in item:
                return False
            if not isinstance(item[skey], sval):
                return False
        return True
    
    

    def check_for_methods(self):
        if self.dbhand is None:
            raise AttributeError("Didn't inject the database handler")

        if not hasattr(self.dbhand, "save") or not hasattr(self.dbhand, "processor"):
            raise AttributeError("The database handler doesn't have the appropiate functions")
    
    
    def prop(self, _alt):
        self.check_for_methods()
        self._alt = _alt
        return self

    def last(self) -> dict:
        """ Get the last of a given item"""
        return self.dbhand.last(self._alt)

    def count(self) -> int:
        return self.dbhand.count(self._alt)
    
    def reset(self):
        if self.dbhand.count(self._alt) == 0:
            default = self.default_dict
            self.dbhand.save(default, alt=self._alt)


