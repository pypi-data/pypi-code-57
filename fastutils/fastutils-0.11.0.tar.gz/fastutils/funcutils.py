# -*- coding: utf-8 -*-
try:
    from inspect import signature
except ImportError:
    from funcsigs import signature
from . import typingutils
import bizerror


def get_inject_params(func, data):
    params = {}
    parameters = signature(func).parameters
    for name, parameter in parameters.items():
        if parameter.default is parameter.empty: # no default value, this parameter is required
            if not name in data:
                raise bizerror.MissingParameter("Missing required parameter: {0}".format(name))
            value = data[name]
        else:
            value = data.get(name, parameter.default)
        if not parameter.annotation is parameter.empty:
            value = typingutils.smart_cast(parameter.annotation, value)
        params[name] = value
    return params


def call_with_inject(func, data):
    params = get_inject_params(func, data)
    return func(**params)


