# -*- coding: utf-8 -*-

# from ipdb import set_trace as idebug
import pandas as pd
import numpy as np

import importlib
from .funcs import get_class_string, get_class_from_instance_dict

class NonetypePersistable():
    def to_dict(self, x):
        if x is not None:
            raise TypeError("Input object is of type %s" %(type(x)))

        out = dict()
        out['__class__'] = get_class_string(self)
        return out

    @classmethod
    def from_dict(cls, cfg):
        return None


class BasicPersistable():
    def to_dict(self, x):
        #Are there others?
        if not isinstance(x, (int, float, complex, str)):
            raise TypeError("Input object is of type %s" %(type(x)))

        out = dict()
        # idebug()
        out['__class__'] = get_class_string(self)
        out['type'] = self.get_type_of_input(x)
        out['object'] = str(x)
        return out

    @classmethod
    def from_dict(cls, cfg):
        _class = get_class_from_instance_dict(cfg)

        if _class != cls:
            raise TypeError

        # This may bite me later, but I need to do some checking before
        # performing an eval
        _type = cfg.pop('type')
        assert _type in __builtins__, "Illegal type requested: %s" %(_type)
        _type = eval(_type)
        return _type(cfg['object'])

    def get_type_of_input(self, x):
        return str(type(x))[:-2].split("'")[-1]


class FunctionPersistable():
    def to_dict(self, func):
        #TODO should I instead check that f._class__ == function?
        if not hasattr(func, '__call__'):
            raise TypeError("Input is of type %s" %(type(func)))

        out = dict()
        out['__class__'] = get_class_string(self)
        out['mod_name'] = func.__module__
        out['func_name'] = func.__name__

        if out['mod_name'] is None:
            raise ValueError("Can't find module name for func %s" %(func))

        return out

    @classmethod
    def from_dict(cls, cfg):
        _class = get_class_from_instance_dict(cfg)

        if _class != cls:
            raise TypeError

        module_name = cfg['mod_name']
        func_name = cfg['func_name']

        try:
            _module = importlib.import_module(module_name)
        except importlib.ModuleNotFoundError:
            raise ValueError("Module %s not found" %(module_name))

        try:
            _func = getattr(_module, func_name)
        except AttributeError:
            raise ValueError("Function %s not found in module %s" %(func_name, module_name))

        return _func

class NumpyPersistable():
    def to_dict(self, a):
        if not isinstance(a, np.ndarray):
            raise TypeError("Input object is of type %s" %(type(a)))

        out = dict()
        out['__class__'] = get_class_string(self)
        out['dtype'] = str(a.dtype)
        out['shape'] = list(a.shape)
        out['text'] = tuple(a.tolist())

        return out

    @classmethod
    def from_dict(cls, cfg):
        _class = get_class_from_instance_dict(cfg)

        if _class != cls:
            raise TypeError

        # dtype = np.dtype(cfg['dtype'])
        # shape = cfg['shape']
        text = cfg['text']

        arr = np.array(text)
        return arr



class PandasPersistable():
    def to_dict(self, df):
        if not isinstance(df, (pd.Series, pd.DataFrame)):
            raise TypeError("Input object is of type %s" %(type(df)))

        out = dict()
        out['__class__'] = get_class_string(self)
        out['json'] = df.to_json()
        return out

    @classmethod
    def from_dict(cls, cfg):
        _class = get_class_from_instance_dict(cfg)

        if _class != cls:
            raise TypeError

        df = pd.read_json(cfg['json'])
        return df
