import pandas as pd
from pandashape import Columns
from pandashape.internal import listify


class ColumnResolver:
    def __init__(self):
        pass

    # both describers and transformers use column definitions to indicate which columns
    # should be targeted for description/transformation. a column definition can be a member
    # of the Columns enum, a single string column name, or an array of column names. this
    # function takes any of these as an input and returns the resolved column NAMES
    def resolve(self, definition, df):
        if definition == Columns.All:
            return df.columns
        elif definition == Columns.Numeric:
            return df.select_dtypes(include='number').columns
        else:
            return [column for column in definition if column in df.columns]
