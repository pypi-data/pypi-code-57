# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:27:54 2020

TODO
o Doc strings
o Better error messages from persist and validate dict
x Non-string dictionary keys should be persisted.
x Straight writing of ints and strings in persist to save space
x Tidy up -- have an __init__.py
x Fix numpy bugs
x Persistable should validate
x Persist file should include metadata
    x date and user
    x file and function that called it.
x Make the eval more secure
    maybe `assert type in __builtin__.__dict__`
x Some examples -- a simple dict, one with a file pointer
x Tests for FrozenDict
x Frozendict needs a json handler
@author: fergal
"""

# from ipdb import set_trace as idebug
from . import specials
from . import funcs
import datetime
import inspect
import json
import bz2
import os

VERSION = "0.0.1"

class Persistable():
    """A base class that implements code to convert a class
    to/from a Persistable, a representation of ints and
    strings in a pattern of nested dictionaries.

    Derive your class from this class to make it easy
    to save that class to disk. See module documentation
    for more information
    """
    @classmethod
    def from_dict(cls, cfg):
        """Load a class from a dictionary.

           Creates a representation of a class as a
           dictionary of strings and ints. Can persist
           any class composed of recognised objects,
           or objects that also implement from_dict()

           If this method doesn't work out, you may
           need to implement a special purpose method
           in the daughter class itself.
        """
        _class = funcs.get_class_from_instance_dict(cfg)
        assert _class == cls
        cfg.pop('__class__')

        obj = cls.__new__(cls)

        for k in cfg:
            obj.__dict__[k] = restore(cfg[k])
        return obj


    def to_dict(self):
        """Convert a class into a dictionary.

        If this doesn't work out of the box, you may need to reimplement
        in the daughter class
        """
        out = dict()
        out['__class__'] = funcs.get_class_string(self)
        for k in self.__dict__:
            out[k] = persist(self.__dict__[k])
        return out



def persist_to_file(fn, **kwargs):
    """Persist an object, or objects to disk

    Example
    ---------
    persist_to_file('file.per', x=5, y='a string')
    """

    strict  = kwargs.pop('strict', True)
    stack_level = kwargs.pop('_metadata_stack_level', 2)

    state = persist(kwargs, strict)
    meta = create_metadata(stack_level)

    obj = {'state':state, 'meta':meta}
    with bz2.open(fn, "wt") as fp:
         fp.write( json.dumps(obj) )


def restore_from_file(fn):
    """Restore objects from a file created by persist_to_file()"""
    # idebug()
    with bz2.open(fn, "rt") as fp:
        jobj = json.loads( fp.read())
    obj = restore(jobj['state'])
    return obj, jobj['meta']


def validate_dict(x):
    """Check that the results of to_dict are json compatible

    Raises an exception if dictionary can not be validated.
    Useful for classes that reimplement to_dict and
    from_dict()
    """
    # idebug()
    try:
        return _validate(x)
    except ValueError as e:
        raise ValueError("The element is of an unsupported type: %s" %(e))

# End of the public API
#############################################
def create_metadata(n_level=1):
    """
    Calling file, func, line
    version number
    user and date
    """

    meta = dict()
    meta['user'] = os.environ.get('USER', 'unknown')
    meta['date'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    meta['format_version'] = VERSION

    #Get calling frame
    frame = inspect.currentframe()
    for i in range(n_level):
        try:
            frame = frame.f_back
        except AttributeError:
            raise AttributeError("Requested level (%i) exceeds stack depth (%i)" %(n_level, i))


    # module = frame.f_globals['__module__']
    meta['module'] = frame.f_globals['__name__']
    fn = frame.f_globals['__file__']
    meta['file']  = os.path.basename(fn)
    meta['func'] = str(frame.f_code.co_name)
    meta['line'] = str(frame.f_lineno)

    return meta


def persist(obj, strict=True):
    """Convert a dictionary of complex types into a dictionary of
    simple types that can be written to disk
    """
    special_list = [specials.NonetypePersistable,
                    specials.BasicPersistable,
                    specials.FunctionPersistable,
                    specials.NumpyPersistable,
                    specials.PandasPersistable,
                    ]

    if isinstance(obj, (int, str)):
      return obj

    if hasattr(obj, 'to_dict'):
        #If the class has a to_dict method, use it.
        return obj.to_dict()

    for sp in special_list:
        try:
            return sp().to_dict(obj)
        except TypeError:
            pass

    try:
        return IterablePersistable().to_dict(obj, strict)
    except TypeError:
        pass

    if not strict:
        return str(obj)
    raise TypeError("Failed to persist %s" %(obj))


def restore(cfg):
    if isinstance(cfg, (int, str)):
      return cfg

    _class = funcs.get_class_from_instance_dict(cfg)
    return _class.from_dict(cfg)


def _validate(x, prefix=None):
    if isinstance(x, bool):
        raise ValueError("Boolean %s is not persistable" %(x))

    if isinstance(x, (int, float, str)):
        return True

    if isinstance(x, list):
        for i,elt in enumerate(x):
            return _validate(elt, 'list[%i].' %(i))

    if isinstance(x, dict):
        for k in x:
            prefix = "dict[%s]." %(str(k))
            return _validate(k, prefix) and _validate(x[k], prefix)

    raise ValueError("Element %s%s is not persistable" %(prefix, str(x)))






class IterablePersistable():
    """This special persistable has to live here instead of the specials
    module because it calls persist and restore"""

    def to_dict(self, x, strict=True):
        if isinstance(x, str) or not hasattr(x, '__len__'):
            raise TypeError("Input object is of type %s" %(type(x)))

        # idebug()
        out = dict()
        out['__class__'] = specials.get_class_string(self)
        out['type'] = self.get_type_of_input(x)
        out['isMapping'] = str(hasattr(x, 'keys'))
        out['len'] = len(x)

        if out['isMapping'] == 'True':
            for i, k in enumerate(x):
                key = self.get_key(i)
                v = persist(x[k], strict)
                k = persist(k, strict)
                out[key] = (k, v)
        else:
            # for i in range(len(x)):
            for i, elt in enumerate(x):
                key = self.get_key(i)
                out[key] = persist(elt, strict)
        return out

    @classmethod
    def from_dict(cls, params):
        _class = specials.get_class_from_instance_dict(params)
        params.pop('__class__')

        if _class != cls:
            raise TypeError

        #This may bite me later, but I don't want to do an eval
        # without at least some checking
        _type = params.pop('type')
        assert _type in __builtins__, "Illegal type requested: %s" %(_type)
        _type = eval(_type)
        _len = params.pop('len')
        isMapping = params.pop('isMapping')

        if isMapping == 'True':
            out = dict()
            for i, key in enumerate(params):
                k, v = params[key]
                k = restore(k)
                v = restore(v)
                out[k] = v
        else:
            out = list()
            for i in range(_len):
                key = cls.get_key(i)
                obj = restore(params[key])
                out.append(obj)
        return _type(out)

    @staticmethod
    def get_key(i):
        return "k%i" %(i)

    def get_type_of_input(self, x):
        return str(type(x))[:-2].split("'")[-1]


