# -*- coding: utf-8 -*-


import pandas as pd
import os
from main import collect_result
import utils

root = os.path.dirname(os.getcwd())

# sample time series dataframe with columns(id, datestamp, y)

raw_fact = utils.read_csv(root, 'test_data.csv')
raw_fact['date_stamp'] = pd.to_datetime(raw_fact['date_stamp'])
raw_fact.info()

model_list = ['fft', 'holt_winters', 'sarimax', 'ewm_model', 'prophet']
gbkey = 'id'

result = collect_result(raw_fact, model_list, gbkey)






