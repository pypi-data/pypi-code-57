import pandas as pd
from pandas import DataFrame
from pandashape import Columns
from pandashape.transformers import Transformer
from pandashape.internal import ColumnResolver, listify


class TransformerExecutor:
    def validate(self, df, columnDefinitions):
        for columnDef in columnDefinitions:
            for transformer in listify(columnDef['transformers']):
                assert(isinstance(transformer, Transformer))

    def transform(self, df, transformations):
        # convert the transformations to an array (so people can pass
        # either an array of definitions or just one)
        transformations = listify(transformations)

        # validate the call
        self.validate(df, transformations)

        # loop and execute the transformations
        col_resolver = ColumnResolver()
        # This df holds each column that undergoes a transformation during this call.
        # At the end, we'll append its columns to the original dataframe.
        df_transformed = DataFrame()

        for transformation in transformations:
            # resolve column names (could be Columns.All, a single column name, or an array of them)
            transform_column_names = col_resolver.resolve(transformation['columns'], df)

            for transform_column_name in transform_column_names:
                df_transformed[f"{transform_column_name}_transformed"] = self.__transformColumn(
                    df[transform_column_name],
                    listify(transformation['transformers'])
                )

        # after we're done transforming, append all transformed columns to the original df
        return pd.concat([df, df_transformed], axis=1)

    def __transformColumn(self, column, transformers):
        for transformer in transformers:
            column = transformer.transform(column)

        return column
