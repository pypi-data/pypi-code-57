from pandas import DataFrame, Series
import pandas as pd
from pandashape.transformers.GenericTransformer import GenericTransformer


class MassLabelEncoder(GenericTransformer):
    def __init__(self, label_encoding_breakpoint=0):
        self.label_encoding_breakpoint = label_encoding_breakpoint

    def transform(self, df):
        assert(isinstance(df, DataFrame))
        categorical_features = (
            df
            .select_dtypes(include='object')
            .columns
            .array
            .to_numpy()
            .tolist()
        )

        # print(categorical_features)

    def transformSeries(self, series):
        unique_value_count = len(series.astype('category').cat.codes)

        if unique_value_count >= self.label_encoding_breakpoint:
            return self.__labelEncode(series)
        else:
            return self.__oneHotEncode(series)

    def __labelEncode(self, series):
        return pd.Series(name=series.name, data=series.astype('category').cat.codes)

    def __oneHotEncode(self, series):
        return pd.get_dummies(series)
