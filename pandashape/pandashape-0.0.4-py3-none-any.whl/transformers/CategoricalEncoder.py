import pandas as pd
from pandas import DataFrame, Series
from pandashape.transformers.Transformer import Transformer


class CategoricalEncoder(Transformer):
    def __init__(self, column_label=None, label_encoding_breakpoint=0):
        self.column_label = column_label
        self.label_encoding_breakpoint = label_encoding_breakpoint

    def transform(self, series):
        assert(isinstance(series, pd.Series))

        unique_value_count = len(series.astype('category').cat.codes)

        if unique_value_count >= self.label_encoding_breakpoint:
            return self.__labelEncode(series)
        else:
            return self.__oneHotEncode(series)

    def __labelEncode(self, series):
        return pd.Series(name=series.name, data=series.astype('category').cat.codes)

    def __oneHotEncode(self, series):
        return pd.get_dummies(series)
