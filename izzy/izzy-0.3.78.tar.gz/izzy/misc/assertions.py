"""
assertions.py
=============
written in Python3

author: C. Lockhart
"""

import inspect


# Decorator to assert signature of functions
def assert_signature(*arg_types):
    """
    Asserts that the signature of a function matches types


    Parameters
    ----------
    arg_types : list, set, or tuple
        Represents the types of the function's arguments

    Examples
    --------
    >>> @assert_signature(int, int, int)
    >>> def my_function(a, b, c):
    >>>     return (a + b) / c
    >>> my_function(1, 2,, 3)
    1

    >>> my_function(1, 2, '3')
    AttributeError
    """

    def _execute_function(func):
        def _execute_arguments(*arg_values):
            # Sanity
            if len(arg_types) != len(arg_values):
                raise AttributeError('{0} assert_signature needs {1} arguments'.format(func.__name__, len(arg_values)))

            # Loop over and make sure types match
            arg_names = inspect.signature(func).parameters.keys()
            for arg_value, arg_name, arg_type in zip(arg_values, arg_names, arg_types):
                if not isinstance(arg_value, arg_type):
                    raise AttributeError('{0} must be of type {1}'.format(arg_name, arg_type.__name__))

        return _execute_arguments

    return _execute_function


# assert types
def assert_type(x, types, none_okay=False, error_message='type check failed'):
    """
    Checks that `x` is an instance of `types`

    If this is not true, raise an `AttributeError`

    Parameters
    ----------
    x : any
        A value
    types : class or list or tuple of classes
        The types of `x` to assert
    none_okay : bool
        Is it okay if `x` is None?
    error_message : str
        Message to return if `x` is not of `types`
    """

    # Logic here could be made clearer
    # We pass if none_okay is True and x is None OR if x is types. Fail otherwise.
    if not ((none_okay and x is None) or isinstance(x, types)):
        raise AttributeError(error_message)
