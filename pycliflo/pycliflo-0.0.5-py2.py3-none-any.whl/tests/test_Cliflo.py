# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 09:25:41 2019

@author: michaelek
"""
import pytest
from pycliflo import Cliflo
import pandas as pd

pd.options.display.max_columns = 10

####################################
### Parameters

from_date = '2018-06-01'
to_date = '2018-06-02'

chromedriver = '/media/sdb1/Programs/Linux/selenium/chromedriver'

lat = -43.874770
lon = 170.952955
dis = 50

dataset_code = ['201']
# dataset_code = ['205']
# site = ['37255', '4772']
site = ['37255']

########################################
### Tests

cf1 = Cliflo(chromedriver)

self = Cliflo(chromedriver)


def test_get_dataset_codes():
    ds_codes = cf1.get_dataset_codes()
    assert len(ds_codes) > 30


def test_get_Sites():
    sites1 = cf1.get_sites(dataset_code, lat, lon, dis, site_owner=True)
    assert len(sites1) > 15


def test_get_ts_data():
    cf1.login('mullenkamp1', 'DWVMODJ8')
    sites2, ts1 = cf1.get_ts_data(dataset_code, site, from_date, to_date)
    cf1.logout()
    assert len(ts1) == 10










