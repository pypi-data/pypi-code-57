from joblib import Parallel, delayed

from .processing import map, filter, split, expand, combine, join


class BaseTransformer:
    '''
    The BaseTransformer defines a generic data transformation pattern that
    can be implemented with a number of data processing concepts.
    '''
    def transform(self, data, *args, **kwargs):
        raise NotImplementedError()


class MapTransformer(BaseTransformer):

    def __init__(self, func, n_jobs=1, **kwargs):
        '''
        dp.MapTransformer is the respective transformer for dp.map.

        Parameters
        -----------
        :param func: the mapping function
        :param n_jobs: amount of used threads/processes
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.n_jobs = n_jobs
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return map(self.func, data, self.n_jobs, **self.kwargs)


class FilterTransformer(BaseTransformer):

    def __init__(self, pred, n_jobs=1, **kwargs):
        '''
        dp.FilterTransformer is the respective transformer for dp.filter.

        Parameters
        -----------
        :param pred: the filter predicate
        :param n_jobs: amount of used threads/processes
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.pred = pred
        self.n_jobs = n_jobs
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return filter(self.pred, data, self.n_jobs, **self.kwargs)


class SplitTransformer(BaseTransformer):

    def __init__(self, func, n_jobs=1, **kwargs):
        '''
        dp.SplitTransformer is the respective transformer for dp.split.

        Parameters
        -----------
        :param func: the discriminator function
        :param n_jobs: amount of used threads/processes
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.n_jobs = n_jobs
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return split(self.func, data, self.n_jobs, **self.kwargs)


class ExpandTransformer(BaseTransformer):

    def __init__(self, func, n_jobs=1, **kwargs):
        '''
        dp.ExpandTransformer is the respective transformer for dp.expand.

        Parameters
        -----------
        :param func: the expansion function
        :param n_jobs: amount of used threads/processes
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.n_jobs = n_jobs
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return expand(self.func, data, self.n_jobs, **self.kwargs)


class CombineTransformer(BaseTransformer):

    def __init__(self, func, n_jobs=1, **kwargs):
        '''
        dp.CombineTransformer is the respective transformer for dp.combine.

        Parameters
        -----------
        :param func: the combination function
        :param n_jobs: amount of used threads/processes
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.n_jobs = n_jobs
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return combine(self.func, *data, n_jobs=self.n_jobs, **self.kwargs)


class JoinTransformer(BaseTransformer):

    def __init__(self, func, n_jobs=1, **kwargs):
        '''
        dp.JoinTransformer is the respective transformer for dp.join.

        Parameters
        -----------
        :param func: the join function
        :param n_jobs: amount of used threads/processes
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.func = func
        self.n_jobs = n_jobs
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return join(self.func, *data, n_jobs=self.n_jobs, **self.kwargs)


class DataTransformer(BaseTransformer):

    def __init__(self, func, *args, **kwargs):
        '''
        dp.DataTransformer is a transformer to manipulate the entire collection of data items.

        Parameters
        -----------
        :param func: the manipulation function
        :param args: additional args for func
        :param kwargs: additional kwargs for func
        '''
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        return self.func(data, *self.args, **self.kwargs)


class MultiTransformer(BaseTransformer):

    def __init__(self, *transformers, n_jobs=1, **kwargs):
        '''
        dp.MultiTransformer is a construct to manipulate mutli-collections of data tiems.

        Parameters
        -----------
        :param transformers: the transformers for the respective collections of data items
        :param n_jobs: amount of used threads/processes
        :param kwargs: additional arguments for joblib.Parallel, e.g. backend='loky'
        '''
        self.transformers = transformers
        self.n_jobs = n_jobs
        self.kwargs = kwargs

    def transform(self, data, *args, **kwargs):
        if self.n_jobs == 1:
            return [transformer.transform(items, *args, **kwargs)
                    for transformer, items in zip(self.transformers, data)]

        return Parallel(n_jobs=self.n_jobs, **self.kwargs)(delayed(transformer.transform)
                (items, *args, **kwargs) for transformer, items in zip(self.transformers, data))


class PipelineTransformer(BaseTransformer):

    def __init__(self, *transformers):
        '''
        dp.PipelineTransformer is a construct to pipe a collection of transformers.

        Parameters
        -----------
        :param transformers: the transformer sequence to apply
        '''
        self.transformers = transformers

    def transform(self, data, *args, **kwargs):
        res = data

        for transformer in self.transformers:
            res = transformer.transform(res, *args, **kwargs)

        return res