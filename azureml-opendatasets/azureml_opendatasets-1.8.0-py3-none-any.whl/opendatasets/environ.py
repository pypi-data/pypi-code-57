# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines runtime environment classes where opendatasets are used.

Environments are used to ensure functionality is optimized for the respective environments. In general,
you will not need to instantiate environment objects or worry about the implementation.
Use the ``get_environ`` module function to return the environment.
"""

from typing import Union

from pandas import DataFrame as PdDataFrame
from pyspark.sql.dataframe import DataFrame as SparkDataFrame


class RuntimeEnv(object):
    """Defines the base class definition of runtime environments."""


class SparkEnv(RuntimeEnv):
    """Represents a Spark runtime environment."""


class PandasEnv(RuntimeEnv):
    """Represents a pandas runtime environment."""


def get_environ(data: Union[SparkDataFrame, PdDataFrame]):
    """Get the Spark runtime environment."""
    if(isinstance(data, SparkDataFrame)):
        return SparkEnv()
    return PandasEnv()
