#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   data_wrapper.py
@Time    :   2020/06/22 19:46:57
@Author  :   nicholas wu 
@Version :   1.0
@Contact :   nicholas_wu@aliyun.com
@License :    
@Desc    :   None
'''
import pandas as pd
from pandarallel.utils.tools import chunk


class DataWrapper(object):

    @staticmethod
    def get_chunks(nb_workers, *iterables):
        for chunk_ in chunk(iterables[0].__len__(), nb_workers):
            yield tuple([data[chunk_] for data in iterables])


    @staticmethod
    def worker(func, *iterables):
        return pd.Series(map(func, *iterables), index=iterables[0].index)


    @staticmethod
    def reduce(results):
        return pd.concat(results).sort_index().tolist()

