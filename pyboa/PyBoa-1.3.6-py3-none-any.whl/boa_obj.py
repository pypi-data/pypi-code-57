import random
import functools
import inspect
from functools import wraps
from enum import Enum


class Dict(dict):
    def __init__(self, d):
        super().__init__({k: boa(v) for k, v in d.items()})

    def __getattribute__(self, name):
        """get, if exist, ``dict`` data then ``dict`` attribut"""
        if name in dict.keys(self):
            return dict.get(self, name)
        return super(Dict, self).__getattribute__(name)

    def __setattr__(self, name, value):
        dict.update(self, {name: boa(value)})

    def __setitem__(self, key, value):
        dict.update(self, {key: boa(value)})

    def toPython(self):
        return to_py(self)


class List(list):
    def __init__(self, li, rec=True):
        if rec:
            li = map(boa, li)
        super().__init__(li)

    def map(self, fun):
        return List(map(fun, self), rec=False)

    def reduce(self, fun):
        return functools.reduce(fun, self)

    def filter(self, fun):
        return List(filter(fun, self), rec=False)

    def index(self, elem, *args, raise_exception=True):
        try:
            return super().index(elem, *args)
        except ValueError as e:
            if raise_exception:
                raise e
            return None

    def reverse(self, side_effect=False):
        if side_effect:
            return list.reverse(self)
        return List(self[::-1], rec=False)

    def shuffle(self):
        li = List(self[:], rec=False)
        random.shuffle(li)
        return li

    def randomChoice(self):
        return random.choice(self)

    def copy(self):
        return List(self[:], rec=False)

    def append(self, el):
        list.append(self, boa(el))

    def toPython(self):
        return to_py(self)


# def check_raise(data, raise_exception):
#     if isinstance(data, List) or isinstance(data, Dict):
#         if raise_exception:
#             raise ValueError("the data given is already Boa data\n" +
#                              "if you don't want to raise an exception, pass raise_exception=False")
#         else:
#             return data


def boa(data):
    if isinstance(data, List) or isinstance(data, Dict):
        return data

    if hasattr(data.__class__, 'refresh_from_db'):
        return data  # special stop for django ORM

    if inspect.isclass(data):
        return data

    if not good_boa(data):
        return boa_wraps_obj(data)

    if callable(data):
        return boa_wraps(data)

    return to_boa(data)


def good_boa(data):
    if data is None:
        return True
    if data.__class__.__name__[0].islower():
        return True
    return False


def to_boa(data):
    """
        transforme recursively a Python ``dict``, ``list`` into a Boa
        :param data: insert any Python data
        :return: the corresponding Boa data
    """

    if isinstance(data, list) or isinstance(data, tuple):
        return List(data)
    elif isinstance(data, dict):
        return Dict(data)
    else:
        return data


def to_py(data):
    if isinstance(data, List):
        return list(map(to_py, data))
    elif isinstance(data, Dict):
        return {k: to_py(v) for k, v in data.items()}
    else:
        return data


def boa_wraps(to_wrap):
    @wraps(to_wrap)
    def dec(*args, **kwargs):
        return boa(to_wrap(*args, **kwargs))
    return dec


def boa_wraps_obj(obj):
    if isinstance(obj, Enum):
        return obj  # Cannot extend enumerations
    methods = {
        '__new__': lambda cls: super(obj.__class__, cls).__new__(cls),
        '__init__': lambda self: None,
        '__getitem__': lambda self, item: boa(obj.__getitem__(item)),
        # '__getattribute__': lambda self, name: boa(getattr(obj, name)),
        '__getattribute__': gen_getattribute(obj),
        '__doc__': obj.__doc__
    }
    magic_methods = [
        '__len__',
        '__setitem__', '__delitem__',
        '__repr__', '__str__',
        '__call__', '__contains__',

        '__le__', '__lt__', '__eq__', '__ne__', '__gt__', '__ge__',
        '__and__', '__or__', '__sub__', '__xor__',
        '__hash__',
        '__module__',
    ]
    for magic_method in magic_methods:
        if hasattr(obj, magic_method):
            methods[magic_method] = getattr(obj, magic_method)

    if hasattr(obj, '__iter__'):
        methods['__iter__'] = gen_iter(obj)

    Class = type(obj.__class__.__name__,
                 (obj.__class__,),
                 methods)

    return Class()


def gen_iter(obj):
    def it(self):
        for e in getattr(obj, '__iter__')():
            yield boa(e)
    return it


def gen_getattribute(obj):
    def getattribute(self, name):
        try:
            return boa(getattr(obj, name))
        except AttributeError as e:
            if isinstance(obj, list):
                try:
                    return attach_obj(getattr(List, name), List(obj))
                except AttributeError:
                    pass
            try:
                return boa(obj.__getitem__(name))
            except KeyError:
                raise e
    return getattribute


def attach_obj(method, obj):
    @wraps(method)
    def attach(*args, **kwargs):
        return method(obj, *args, **kwargs)
    return attach
