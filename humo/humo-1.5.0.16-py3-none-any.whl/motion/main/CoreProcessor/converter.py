import numpy as np
import functools
from .HumoArray import HumoArray, HumoArrayEMG
from .divHumoArray import divHumoArray, divHumoArrayEMG
from .interHumoArray import interHumoArray, interHumoArrayEMG
from .normHumoArray import normHumoArray, normHumoArrayEMG
from collections import namedtuple


def cvt_HumoArray(argsType):
    def cvt_HumoArray_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if argsType == "general":
                if type(args[1]) == list:
                    array = HumoArray(data, args[1])
                    for name, each_data in zip(args[1], np.array(data)):
                        setattr(array, name, HumoArray(each_data))
                    return array
                else:
                    return HumoArray(data, args[1])

            elif argsType == "ForcePlate":
                if type(args[1]) == list:
                    names = ["plate" + str(i) for i in args[1]]
                    array = HumoArray(data, names)
                    for name, each_data in zip(names, np.array(data)):
                        setattr(array, name, HumoArray(each_data))
                    return array
                else:
                    return HumoArray(data, "plate" + str(args[1]))

            elif argsType == None:
                return HumoArray(data)
        return wrapper
    return cvt_HumoArray_

def cvt_divHumoArray(argsType):
    def cvt_divHumoArray_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if argsType == "general":
                if type(args[1]) == list:
                    array = divHumoArray(data, args[1])
                    for name, each_data in zip(args[1], data):
                        setattr(array, name, divHumoArray(each_data))
                    return array
                else:
                    return divHumoArray(data, args[1])

            elif argsType == "ForcePlate":
                if type(args[1]) == list:
                    names = ["plate" + str(i) for i in args[1]]
                    array = divHumoArray(data, names)
                    for name, each_data in zip(names, data):
                        setattr(array, name, divHumoArray(each_data, name))
                    return array
                else:
                    return divHumoArray(data, "plate" + str(args[1]))
            elif argsType == None:
                return divHumoArray(data)
        return wrapper
    return cvt_divHumoArray_


def cvt_interHumoArray(argsType):
    def cvt_interHumoArray_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if argsType == "general":
                if type(args[1]) == list:
                    array = interHumoArray(data, args[1])
                    for name, each_data in zip(args[1], data):
                        setattr(array, name, interHumoArray(each_data))
                    return array
                else:
                    return interHumoArray(data, args[1])
            elif argsType == "ForcePlate":
                names = ["plate" + str(i) for i in args[1]]
                if type(args[1]) == list:
                    array = interHumoArray(data, names)
                    for name, each_data in zip(names, data):
                        setattr(array, name, interHumoArray(each_data))
                    return array
                else:
                    array = interHumoArray(data, names)
                    return array
            elif argsType == None:
                return interHumoArray(data)
        return wrapper
    return cvt_interHumoArray_


def cvt_normHumoArray(argsType):
    def cvt_normHumoArray_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if argsType == "general":
                if type(args[1]) == list:
                    array = normHumoArray(data, args[1])
                    for name, each_data in zip(args[1], data):
                        setattr(array, name, normHumoArray(each_data))
                    return array
                else:
                    return normHumoArray(data, args[1])
            elif argsType == "ForcePlate":
                names = ["plate" + str(i) for i in args[1]]
                if type(args[1]) == list:
                    array = normHumoArray(data, names)
                    for name, each_data in zip(names, data):
                        setattr(array, name, normHumoArray(each_data))
                    return array
                else:
                    return normHumoArray(data, names)
            elif argsType == None:
                return normHumoArray(data)
        return wrapper
    return cvt_normHumoArray_


"""
HumoArrayEMG
"""
def cvt_HumoArrayEMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        if data.ndim == 2:
            data_ = HumoArrayEMG(data)
            for name, each_data in zip(args[1], data):
                setattr(data_, name, each_data)
            setattr(data_, "name", args[1])
            return data_
        else:
            return data
    return wrapper

def cvt_divHumoArrayEMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        if data.ndim == 3:
            data_ = divHumoArrayEMG(data)
            for name, each_data in zip(args[1], data):
                setattr(data_, name, each_data)
            setattr(data_, "name", args[1])
            return data_
        else:
            return data
    return wrapper

def cvt_interHumoArrayEMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        if data.ndim == 2:
            data_ = interHumoArrayEMG(data)
            for name, each_data in zip(args[1], data):
                setattr(data_, name, each_data)
            setattr(data_, "name", args[1])
            return data_
        else:
            return data
    return wrapper


def cvt_normHumoArrayEMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        if data.ndim == 3:
            data_ = normHumoArrayEMG(data)
            for name, each_data in zip(args[1], data):
                setattr(data_, name, each_data)
            setattr(data_, "name", args[1])
            return data_
        else:
            return data
    return wrapper
