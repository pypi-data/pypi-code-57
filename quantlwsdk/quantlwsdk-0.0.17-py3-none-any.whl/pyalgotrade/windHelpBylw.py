# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:33:56 2018

@author: SH
"""

import pandas as pd

import datetime

from pyalgotrade import calendayBylw


def windDataToDf(windData):
    datadict = {}
    datadict['tradeDate'] = windData.Times
    for i in range(len(windData.Fields)):
        datadict[windData.Fields[i]] = windData.Data[i]

    dfData = pd.DataFrame(datadict)
    return dfData

