"""
test script at dev stage
"""

import warnings
warnings.filterwarnings('ignore')

import os
os.chdir('C:\\Users\\abc_h\\Desktop\\github\\foresee')

# to run in parallel add current directory to path
import sys
sys.path.append(os.getcwd())


import pandas as pd

from foresee.scripts.main import prepare_fit_report
from foresee.scripts.utils import read_csv


### one column dataframe
# sample time-series dataframe with column name 'Close'

ts_df = read_csv('basic_time_series_data.csv')
ts_df.head()

# available forecasting models
model_list = ['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax']

result, _ = prepare_fit_report(ts_df, model_list=model_list)



### multi column dataframe
# sample time-series dataframe with columns(id, date_stamp, y)

ts_df = read_csv('test_data_light.csv')
ts_df['date_stamp'] = pd.to_datetime(ts_df['date_stamp'])
ts_df.head()

# user defind parameters

# time series values column name: required if input dataframe has more than one column

endog_colname = 'y'

# time series frequency
freq = 5

# out of sample forecast length
fcst_length = 10

# available forecasting models
# model_list = ['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax']
model_list = ['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax']

# avilable run types: 'best_model', 'all_best', 'all_models'
output_format = 'all_best'

# if comparing models (run_type in 'best_model' or 'all_best') then holdout length is required

if output_format == 'all_models':
    holdout_length = None
else:
    holdout_length = 20
    
# fit-forecast computations can be done in parallel for each time series. requires dask library!!!
# for sequential processing set fit_execution_method to 'non_parallel'

fit_execution_method = 'parallel'

# if tune is True, search for best parameter. can be slow

tune = True


# since we have two time series in this dataset, time series id column name and date-time column name are required.
gbkey = 'id'
ds_colname = 'date_stamp'

result, fit_result_list = prepare_fit_report(
                                                    ts_df,
                                                    endog_colname,
                                                    ds_colname, 
                                                    gbkey,
                                                    freq, 
                                                    fcst_length, 
                                                    output_format, 
                                                    holdout_length, 
                                                    model_list,
                                                    fit_execution_method,
                                                    tune
                                            )
