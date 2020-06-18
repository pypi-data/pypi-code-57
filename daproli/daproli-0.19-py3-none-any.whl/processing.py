from itertools import product
from joblib import Parallel, delayed
from tqdm import tqdm

from .utils import _get_return_type, _apply_func


def map(func, data, expand_args=True, n_jobs=1, verbose=0, **kwargs):
    '''
    dp.map applies a transformation function to a collection of data items.

    Parameters
    -----------
    :param func: the mapping function
    :param data: an iterable collection of data
    :param expand_args: true if args should be expanded, false otherwise
    :param n_jobs: amount of used threads/processes
    :param verbose: verbosity level for tqdm / joblib
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
    func_ = lambda args : _apply_func(func, args, expand_args)

    if n_jobs == 1:
        return ret_type([func_(item) for item in tqdm(data, disable=verbose < 1)])

    return ret_type(Parallel(n_jobs=n_jobs, verbose=verbose, **kwargs)(delayed(func_)(item) for item in data))


def filter(pred, data, expand_args=True, n_jobs=1, verbose=0, **kwargs):
    '''
    dp.filter applies a filter predicate to a collection of data items.

    Parameters
    -----------
    :param pred: the filter predicate
    :param data: an iterable collection of data
    :param expand_args: true if args should be expanded, false otherwise
    :param n_jobs: amount of used threads/processes
    :param verbose: verbosity level for tqdm / joblib
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
    pred_ = lambda args: _apply_func(pred, args, expand_args)

    if n_jobs == 1:
        return ret_type([item for item in tqdm(data, disable=verbose < 1) if pred_(item)])

    return ret_type(Parallel(n_jobs=n_jobs, verbose=verbose, **kwargs)
            (delayed(lambda item: item)(item) for item in data if pred_(item)))


def split(func, data, return_labels=False, expand_args=True, n_jobs=1, verbose=0, **kwargs):
    '''
    dp.split applies a discriminator function to a collection of data items.

    Parameters
    -----------
    :param func: the discriminator function
    :param data: an iterable collection of data
    :param return_labels: true if the associated labels should be returned, false otherwise
    :param expand_args: true if args should be expanded, false otherwise
    :param n_jobs: amount of used threads/processes
    :param verbose: verbosity level for tqdm / joblib
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the transformed data lists

    Examples
    -----------
    >>> import daproli as dp
    >>> numbers = range(10)
    >>> dp.split(lambda x : x % 2 == 0, numbers)
    [[1, 3, 5, 7, 9], [0, 2, 4, 6, 8]]
    '''
    ret_type = _get_return_type(data)
    func_ = lambda args: _apply_func(func, args, expand_args)

    if n_jobs == 1:
        labels = [func_(item) for item in tqdm(data, disable=verbose < 1)]
    else:
        labels = Parallel(n_jobs=n_jobs, verbose=verbose, **kwargs)(delayed(func_)(item) for item in data)

    container = {label : list() for label in set(labels)}
    for item, label in zip(data, labels): container[label].append(item)

    if return_labels:
        return [(label, ret_type(container[label])) for label in sorted(container)]

    return [ret_type(container[label]) for label in sorted(container)]


def expand(func, data, expand_args=True, n_jobs=1, verbose=0, **kwargs):
    '''
    dp.expand applies an expansion function to a collection of data items.

    Parameters
    -----------
    :param func: the expansion function
    :param data: an iterable collection of data
    :param expand_args: true if args should be expanded, false otherwise
    :param n_jobs: amount of used threads/processes
    :param verbose: verbosity level for tqdm / joblib
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the transformed data lists

    Examples
    -----------
    >>> import daproli as dp
    >>> numbers = range(10)
    >>> dp.expand(lambda x : (x, x**2), numbers)
    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]]
    '''
    ret_type = _get_return_type(data)
    func_ = lambda args: _apply_func(func, args, expand_args)

    if n_jobs == 1:
        expanded = [func_(item) for item in tqdm(data, disable=verbose < 1)]
    else:
        expanded = Parallel(n_jobs=n_jobs, verbose=verbose, **kwargs)(delayed(func_)(item) for item in data)

    if len(expanded) == 0:
        return ret_type(expanded)

    assert all([len(expanded[idx]) == len(expanded[idx+1]) for idx in range(len(expanded)-1)])
    container = [list() for _ in range(len(expanded[0]))]

    for items in expanded:
        for idx, item in enumerate(items): container[idx].append(item)

    return [ret_type(items) for items in container]


def combine(func, *data, expand_args=True, n_jobs=1, verbose=0, **kwargs):
    '''
    dp.combine applies a combination function to multiple collections of data items.

    Parameters
    -----------
    :param func: the combination function
    :param data: iterable collections of data
    :param expand_args: true if args should be expanded, false otherwise
    :param n_jobs: amount of used threads/processes
    :param verbose: verbosity level for tqdm / joblib
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the combined data list

    Examples
    -----------
    >>> import daproli as dp
    >>> even_numbers = range(0, 10, 2)
    >>> odd_numbers = range(1, 10, 2)
    >>> dp.combine(lambda x, y : (x,y), even_numbers, odd_numbers)
    [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
    '''
    func_ = lambda args: _apply_func(func, args, expand_args)

    if n_jobs == 1:
        return [func_(items) for items in tqdm(zip(*data), disable=verbose < 1)]

    return Parallel(n_jobs=n_jobs, verbose=verbose, **kwargs)(delayed(func_)(items) for items in zip(*data))


def join(pred, *data, expand_args=True, n_jobs=1, verbose=0, **kwargs):
    '''
    dp.join applies a join predicate to multiple collections of data items.

    Parameters
    -----------
    :param pred: the join predicate
    :param data: iterable collections of data
    :param expand_args: true if args should be expanded, false otherwise
    :param n_jobs: amount of used threads/processes
    :param verbose: verbosity level for tqdm / joblib
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the joined data list

    Examples
    -----------
    >>> import daproli as dp
    >>> even_numbers = range(0, 10, 2)
    >>> odd_numbers = range(1, 10, 2)
    >>> dp.join(lambda x, y : y-x == 3, even_numbers, odd_numbers)
    [(0, 3), (2, 5), (4, 7), (6, 9)]
    '''
    pred_ = lambda args: _apply_func(pred, args, expand_args)

    if n_jobs == 1:
        return [items for items in tqdm(product(*data), disable=verbose < 1) if pred_(items)]

    return Parallel(n_jobs=n_jobs, verbose=verbose, **kwargs)(delayed(lambda items : items)
            (items) for items in product(*data) if pred_(items))

