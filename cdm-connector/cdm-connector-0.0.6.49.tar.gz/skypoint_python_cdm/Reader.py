import abc


class Reader(metaclass=abc.ABCMeta):

        @abc.abstractmethod
        def read_df(self, locations, headers, dtypes):()