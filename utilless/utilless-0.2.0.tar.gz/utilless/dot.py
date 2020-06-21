"""
Module: DOT
manipulates different kinds of elements using dots
"""

from .lib.bind import bind


def justdot(iterable):
    """
    Function that takes a iterable and returns a string
    with all the items separated by a dot
    Example:
    justdot(['myObject', 'toString()']) => 'myObject.toString()'"""
    return bind(iterable, ".", ".")
