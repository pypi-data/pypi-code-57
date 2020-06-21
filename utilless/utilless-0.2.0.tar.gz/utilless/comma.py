# comma.py
"""
Module: COMMA
manipulates different kinds of elements using commas

A very common use case is to get a list and put all its items
in a string separated by comma. [name, job, age] => 'name,job,age'
"""

from .lib.bind import bind


def justcomma(iterable):
    """
    Function that takes a iterable and returns a string
    with all the items separated by a comma
    Example:
    justcomma(['apples', 'bananas', 'tofu', 'cats']) =>
       'apples,bananas,tofu,cats'
    """
    return bind(iterable, ",", ",")


def commaspace(iterable):
    """
    Function that takes a iterable and returns a string
    with all the items separated by a comma and a space.
    Example:
    commaspace(['apples', 'bananas', 'tofu', 'cats']) =>
       'apples, bananas, tofu, cats'
    """
    return bind(iterable, ", ", ", ")


def commaand(iterable, lastcomma=", and "):
    """
    Function that takes a iterable and returns a string
    with all the items separated by a comma and a space,
    with and inserted before the last item.

    You can specify a second argument (default = ', and '),
    like commaand(['comma', 'and', 'dot'], ' & ') => 'comma, and & dot'
    """
    return bind(iterable, ", ", str(lastcomma))


# TODO: How to handle nested iterables, v.g. [[1, 2], ['foo', 'bar']]
