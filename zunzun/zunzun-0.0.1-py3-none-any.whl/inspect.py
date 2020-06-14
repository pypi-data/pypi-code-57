from inspect import *  # noqa
import inspect


def findclass(func):
    return inspect._findclass(func)
