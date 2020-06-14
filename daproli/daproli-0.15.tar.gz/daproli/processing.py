from itertools import product
from joblib import Parallel, delayed

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

def map(func, data, n_jobs=1, **kwargs):
    '''
    dp.map applies a transformation function to a collection of data items.

    Parameters
    -----------
    :param func: the mapping function
    :param data: an iterable collection of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the transformed data list

    Examples
    -----------
    >>> import daproli as dp
    >>> names = ['John', 'Susan', 'Mike']
    >>> dp.map(lambda n : n.lower(), names)
    ['john', 'susan', 'mike']
    '''
    ret_type = _get_return_type(data)

    if n_jobs == 1:
        return ret_type([func(item) for item in data])

    return ret_type(Parallel(n_jobs=n_jobs, **kwargs)(delayed(func)(item) for item in data))


def filter(pred, data, n_jobs=1, **kwargs):
    '''
    dp.filter applies a filter predicate to a collection of data items.

    Parameters
    -----------
    :param pred: the filter predicate
    :param data: an iterable collection of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the filtered data list

    Examples
    -----------
    >>> import daproli as dp
    >>> names = ['John', 'Susan', 'Mike']
    >>> dp.filter(lambda n : len(n) % 2 == 0, names)
    ['John', 'Mike']
    '''
    ret_type = _get_return_type(data)

    if n_jobs == 1:
        return ret_type([item for item in data if pred(item)])

    return ret_type(Parallel(n_jobs=n_jobs, **kwargs)(delayed(lambda item: item)(item) for item in data if pred(item)))


def split(func, data, n_jobs=1, **kwargs):
    '''
    dp.split applies a discriminator function to a collection of data items.

    Parameters
    -----------
    :param func: the discriminator function
    :param data: an iterable collection of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the transformed data lists

    Examples
    -----------
    >>> import daproli as dp
    >>> numbers = [i for i in range(10)]
    >>> dp.split(lambda x : x % 2 == 0, numbers)
    [[1, 3, 5, 7, 9], [0, 2, 4, 6, 8]]
    '''
    ret_type = _get_return_type(data)

    if n_jobs == 1:
        labels = [func(item) for item in data]
    else:
        labels = Parallel(n_jobs=n_jobs, **kwargs)(delayed(func)(item) for item in data)

    container = {label : list() for label in set(labels)}
    for item, label in zip(data, labels): container[label].append(item)

    return [ret_type(container[label]) for label in sorted(container)]


def expand(func, data, n_jobs=1, **kwargs):
    '''
    dp.expand applies an expansion function to a collection of data items.

    Parameters
    -----------
    :param func: the expansion function
    :param data: an iterable collection of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the transformed data lists

    Examples
    -----------
    >>> import daproli as dp
    >>> numbers = [i for i in range(10)]
    >>> dp.expand(lambda x : (x, x**2), numbers)
    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]]
    '''
    ret_type = _get_return_type(data)

    if n_jobs == 1:
        expanded = [func(item) for item in data]
    else:
        expanded = Parallel(n_jobs=n_jobs, **kwargs)(delayed(func)(item) for item in data)

    if len(expanded) == 0:
        return ret_type(expanded)

    assert all([len(expanded[idx]) == len(expanded[idx+1]) for idx in range(len(expanded)-1)])
    container = [list() for _ in range(len(expanded[0]))]

    for items in expanded:
        for idx, item in enumerate(items): container[idx].append(item)

    return [ret_type(items) for items in container]


def combine(func, *data, n_jobs=1, **kwargs):
    '''
    dp.combine applies a combination function to multiple collections of data items.

    Parameters
    -----------
    :param func: the combination function
    :param data: iterable collections of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the combined data list

    Examples
    -----------
    >>> import daproli as dp
    >>> even_numbers = [0, 2, 4, 6, 8]
    >>> odd_numbers = [1, 3, 5, 7, 9]
    >>> dp.combine(lambda x, y : (x,y), even_numbers, odd_numbers)
    [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
    '''
    if n_jobs == 1:
        return [func(*items) for items in zip(*data)]

    return Parallel(n_jobs=n_jobs, **kwargs)(delayed(func)(*items) for items in zip(*data))


def join(pred, *data, n_jobs=1, **kwargs):
    '''
    dp.join applies a join predicate to multiple collections of data items.

    Parameters
    -----------
    :param pred: the join predicate
    :param data: iterable collections of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the joined data list

    Examples
    -----------
    >>> import daproli as dp
    >>> even_numbers = [0, 2, 4, 6, 8]
    >>> odd_numbers = [1, 3, 5, 7, 9]
    >>> dp.join(lambda x, y : y-x == 3, even_numbers, odd_numbers)
    [(0, 3), (2, 5), (4, 7), (6, 9)]
    '''
    if n_jobs == 1:
        return [items for items in product(*data) if pred(*items)]

    return Parallel(n_jobs=n_jobs, **kwargs)(delayed(lambda items : items)
            (items) for items in product(*data) if pred(*items))
