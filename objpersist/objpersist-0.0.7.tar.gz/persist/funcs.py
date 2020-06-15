# -*- coding: utf-8 -*-

# from ipdb import set_trace as idebug
import importlib


def get_class_string(obj):
    mod_name = str(obj.__module__)
    class_name = str(obj.__class__)
    class_name = class_name[:-2].split('.')[-1]

    return "%s.%s" %(mod_name, class_name)



def get_class_from_instance_dict(params):
    try:
        class_name = params['__class__']
    except KeyError as e:
        raise KeyError("Keyword __class__ missing: %s" %(e))

    tokens = class_name.split('.')
    if len(tokens) < 2:
        raise ValueError("Class module not specified: Have %s, need module.%s" \
                         %(class_name, class_name))

    module_name = ".".join(tokens[:-1])
    class_name = tokens[-1]

    try:
        _module = importlib.import_module(module_name)
    except importlib.ModuleNotFoundError:
        raise ValueError("Module %s not found" %(module_name))

    try:
        _class = getattr(_module, class_name)
    except AttributeError:
        raise ValueError("Class %s not found in module %s" %(class_name, module_name))

    return _class


