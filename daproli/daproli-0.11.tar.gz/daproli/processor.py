from itertools import product
from joblib import Parallel, delayed


def map(func, data, n_jobs=1, **kwargs):
    '''
    dp.map applies a transformation function to a collection of data items.

    :param func: the mapping function
    :param data: an iterable collection of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the transformed data list
    '''
    if n_jobs == 1:
        return [func(item) for item in data]

    return Parallel(n_jobs=n_jobs, **kwargs)(delayed(func)(item) for item in data)


def filter(pred, data, n_jobs=1, **kwargs):
    '''
    dp.filter applies a filter predicate to a collection of data items.

    :param pred: the filter predicate
    :param data: an iterable collection of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the filtered data list
    '''
    if n_jobs == 1:
        return [item for item in data if pred(item)]

    return Parallel(n_jobs=n_jobs, **kwargs)(delayed(lambda item: item)(item) for item in data if pred(item))


def split(func, data, n_jobs=1, **kwargs):
    '''
    dp.split applies a discriminator function to a collection of data items.

    :param func: the discriminator function
    :param data: an iterable collection of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the transformed data lists
    '''
    if n_jobs == 1:
        labels = [func(item) for item in data]
    else:
        labels = Parallel(n_jobs=n_jobs, **kwargs)(delayed(func)(item) for item in data)

    container = {label : list() for label in set(labels)}
    for item, label in zip(data, labels): container[label].append(item)

    return [container[label] for label in sorted(container)]


def expand(func, data, n_jobs=1, **kwargs):
    '''
    dp.expand applies an expansion function to a collection of data items.

    :param func: the expansion function
    :param data: an iterable collection of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the transformed data lists
    '''
    if n_jobs == 1:
        expanded = [func(item) for item in data]
    else:
        expanded = Parallel(n_jobs=n_jobs, **kwargs)(delayed(func)(item) for item in data)

    if len(expanded) == 0:
        return expanded

    assert all([len(expanded[idx]) == len(expanded[idx+1]) for idx in range(len(expanded)-1)])
    container = [list() for _ in range(len(expanded[0]))]

    for items in expanded:
        for idx, item in enumerate(items): container[idx].append(item)

    return container


def combine(func, *data, n_jobs=1, **kwargs):
    '''
    dp.combine applies a combination function to multiple collections of data items.

    :param func: the combination function
    :param data: iterable collections of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the combined data list
    '''
    if n_jobs == 1:
        return [func(*items) for items in zip(*data)]

    return Parallel(n_jobs=n_jobs, **kwargs)(delayed(func)(*items) for items in zip(*data))


def join(pred, *data, n_jobs=1, **kwargs):
    '''
    dp.join applies a join predicate to multiple collections of data items.

    :param pred: the join predicate
    :param data: iterable collections of data
    :param n_jobs: amount of used threads/processes
    :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
    :return: the joined data list
    '''
    if n_jobs == 1:
        return [items for items in product(*data) if pred(*items)]

    return Parallel(n_jobs=n_jobs, **kwargs)(delayed(lambda items : items)
            (items) for items in product(*data) if pred(*items))
