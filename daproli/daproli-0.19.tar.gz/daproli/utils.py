from collections.abc import Iterable

import numpy as np


def _get_return_type(data):
    '''
    An utility function in order to determine the correct return type
    for the transformation functions.

    Parameters
    -----------
    :param data: an iterable collection of data
    :return: the return type
    '''
    if isinstance(data, range):
        return list

    if isinstance(data, zip):
        return list

    if isinstance(data, np.ndarray):
        return np.array

    return type(data)


def _apply_func(func, args, expand_args):
    '''
    An utility function to apply a given function with either
    zipped or unzipped args.

    Parameters
    -----------
    :param func: the function to apply
    :param args: the args to apply
    :param expand_args: true if args should be expanded, false otherwise
    :return: the function result
    '''
    if expand_args is True and isinstance(args, Iterable) and not isinstance(args, str):
        return func(*args)

    return func(args)