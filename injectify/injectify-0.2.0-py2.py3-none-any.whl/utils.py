"""This module contains the utility functions that power Injectify."""

import ast
import inspect
from textwrap import dedent

from .inspect_mate import getsource


def parse_object(obj):
    """Parse the source into an AST node."""
    source = getsource(obj)
    for _ in range(5):
        try:
            return ast.parse(source)
        except IndentationError:
            source = dedent(source)


def get_defining_class(obj):
    """Return the class that defines the given object or ``None`` if there is
    no class."""
    if inspect.ismethod(obj):
        for cls in inspect.getmro(obj.__self__.__class__):
            if cls.__dict__.get(obj.__name__) is obj:
                return cls
        obj = obj.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(obj):
        class_name = obj.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
        try:
            cls = getattr(inspect.getmodule(obj), class_name)
        except AttributeError:
            cls = obj.__globals__.get(class_name)
        if isinstance(cls, type):
            return cls
    if inspect.isclass(obj):
        class_path = obj.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)
        parent = inspect.getmodule(obj)
        for p in class_path[:-1]:
            parent = getattr(parent, p)
        return parent
    return getattr(obj, '__objclass__', None)  # handle special descriptor objects


def tryattrs(obj, *attrs):
    """Return the first value of the named attributes found of the given object."""
    for attr in attrs:
        try:
            return getattr(obj, attr)
        except AttributeError:
            pass
    obj_name = obj.__name__
    raise AttributeError("'{}' object has no attribute in {}", obj_name, attrs)


def caninject(obj):
    """Check whether the given object can be injected with code."""
    return not (inspect.ismodule(obj)
                or inspect.isclass(obj)
                or inspect.ismethod(obj)
                or inspect.isfunction(obj))
