# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import sys
import pandas as pd
import numpy as np

import foresee
os.path.abspath(foresee.__file__)

from foresee.scripts import main
from foresee.scripts import utils

# sample time-series dataframe with columns(id, date_stamp, y)

ts_df = utils.read_csv('test_data_light.csv')
ts_df['date_stamp'] = pd.to_datetime(ts_df['date_stamp'])
ts_df.head()

# user defind parameters

# time series values column name: required if input dataframe has more than one column

endog_colname = 'y'

if len(ts_df.columns) > 1 and endog_colname is None:
    raise ValueError('time series column name is required!!!')

# time series frequency
freq = 5

# out of sample forecast length
fcst_length = 10

# available forecasting models
model_list = ['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax']

# avilable run types: 'best_model', 'all_best', 'all_models'
run_type = 'all_best'

# if comparing models (run_type in 'best_model' or 'all_best') then holdout length is required

if run_type == 'all_models':
    holdout_length = None
else:
    holdout_length = 20
    
# fit-forecast computations can be done in parallel for each time series. requires dask library!!!
# for sequential processing set fit_execution_method to 'non_parallel'

fit_execution_method = 'parallel'


# since we have two time series in this dataset, time series id column name and date-time column name are required.
gbkey = 'id'
ds_column = 'date_stamp'


'''
result:  dataframe containing fitted values and future forecasts
fit_results_list:  list of dictionaries containing fitted values, forecasts, and errors (useful for debuging)
'''

result, fit_result_list = main.collect_result(
                                                    ts_df.copy(),
                                                    endog_colname,
                                                    gbkey,
                                                    ds_column, 
                                                    freq, 
                                                    fcst_length, 
                                                    run_type, 
                                                    holdout_length, 
                                                    model_list,
                                                    fit_execution_method,
                                            )

result.head()

