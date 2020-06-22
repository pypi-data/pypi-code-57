import pandas as pd
from functools import reduce


def set_index_and_sort(df, index=("code"), inplace=False):
    """
    对DataFrame设置索引，并按索引排序，目的是确保多个DataFrame在使用时行的顺序一致
    :param df: 待排序的DataFrame
    :param index: List, 需要建立索引的列名
    :return:
    """
    if inplace:
        df.set_index(index, inplace=True)
        df.sort_index(inplace=True)
    else:
        return df.set_index(index).sort_index()


def nans_row(df):
    """找到dataframe中包含nan的行"""
    return df[df.isnull().any(axis=1)]


def find_rows_without_nan(df):
    """返回不含有nan的行"""
    return df[df.notnull().all(axis=1)]


def check_index_equal(a, b):
    """检查两个dataframe的index是否一致"""
    return a.index.equals(b.index)


def transform_to_stock_time_series(from_df, field, stock_field="symbol", date_field="date"):
    # 在包含symbol,date,field的dataframe中，以某字段field作为转换对象，转成形如(N,T)的dataframe
    return from_df[[stock_field, date_field, field]].set_index([stock_field, date_field]).\
        sort_index().unstack().stack(level=0).reset_index(level=1, drop=True)


def transform_to_time_series_stock(from_df, field, stock_field="symbol", date_field="date"):
    # 在包含symbol,date,field的dataframe中，以某字段field作为转换对象，转成形如(T,N)的dataframe
    return from_df[[stock_field, date_field, field]].set_index([date_field, stock_field]).\
        sort_index().unstack().stack(level=0).reset_index(level=1, drop=True)


def ravel_time_series_stock_df(from_df, output_field_name):
    """
    将(T,N)的dataframe转成(stock,date,1)的形式
    """
    return from_df.unstack().reset_index().dropna().rename(columns={0: output_field_name})


def merge_dataframe(left, right, how, on, left_index=False, right_index=False):
    """
    合并2个dataframe的非重复列
    """
    cols_to_use = pd.Index([on] + right.columns.difference(left.columns).tolist())
    return pd.merge(left=left, right=right[cols_to_use], how=how, on=on, left_index=left_index, right_index=right_index)


def merge_multiple_dataframe(data_frames, how="inner", on=None, left_index=True, right_index=True):
    """
    合并多个dataframe, 列拼接
    :param data_frames: List
    """
    df_merged = reduce(lambda left, right: pd.merge(left, right, how=how, on=on,
                                                    left_index=left_index, right_index=right_index), data_frames)
    return df_merged