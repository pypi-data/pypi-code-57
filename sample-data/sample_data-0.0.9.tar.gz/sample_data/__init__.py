import pandas as pd

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def _getcsv(name):
    def fn():
        return pd.read_csv(f"{dir_path}/data/{name}.csv")
    return fn

countries = _getcsv('countries')
airbnb = _getcsv('airbnb')
corona = _getcsv('corona')
drinks = _getcsv('drinks')