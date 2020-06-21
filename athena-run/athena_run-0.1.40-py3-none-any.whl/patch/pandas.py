import pandas
from pandas import DataFrame, Series
from pandas.core.groupby import GroupBy

from athena.patch.statsd_config import DEFAULT_STATSD_CLIENT as STATSD_CLIENT

_read_parquet = pandas.read_parquet
_to_parquet = DataFrame.to_parquet
_merge = pandas.merge
_groupby = DataFrame.groupby
_df_apply = DataFrame.apply

_groupby_apply = GroupBy.apply
_series_apply = Series.apply

pandas_string = "pandas."


def read_parquet_patched(*args, **kwargs):
    """
    New read_parquet function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}read_parquet"):
        return _read_parquet(*args, **kwargs)


def to_parquet_patched(*args, **kwargs):
    """
    New to_parquet function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}to_parquet"):
        return _to_parquet(*args, **kwargs)


def merge_patched(*args, **kwargs):
    """
    New merge function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}merge"):
        return _merge(*args, **kwargs)


def dataframe_groupby_patched(*args, **kwargs):
    """
    New DataFrame.groupby function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}df_groupby"):
        return _groupby(*args, **kwargs)

def dataframe_apply_patched(*args, **kwargs):
    """
    New DataFrame.apply function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}df_apply",
            meta={
                'args': str(args),
                'kwargs': str(kwargs),
            }
        ):
        return _df_apply(*args, **kwargs)

def series_apply_patched(*args, **kwargs):
    """
    New Series.apply function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}series_apply",
            meta={
                'args': str(args),
                'kwargs': str(kwargs),
            }
        ):
        return _series_apply(*args, **kwargs)

def groupby_apply_patched(*args, **kwargs):
    """
    New GroupBy.apply function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}groupby_apply",
            meta={
                'args': str(args),
                'kwargs': str(kwargs),
            }
        ):
        return _groupby_apply(*args, **kwargs)


def patch():
    pandas.read_parquet = read_parquet_patched
    DataFrame.to_parquet = to_parquet_patched
    pandas.merge = merge_patched
    DataFrame.groupby = dataframe_groupby_patched
    DataFrame.apply = dataframe_apply_patched
    Series.apply = series_apply_patched
    GroupBy.apply = groupby_apply_patched
