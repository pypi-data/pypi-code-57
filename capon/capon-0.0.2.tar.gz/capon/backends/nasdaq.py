import logging
import requests
import json

import pandas as pd


def get_json(url, headers={}):
    response = requests.get(url, headers=headers)
    logging.info(f'{response.url}.. {response.status_code}')
    
    jo = {}
    if response.status_code==200:
        jo = response.json()
        
    return jo


if False:
    symbol = 'ACEL+'
    print(symbol)
    
    url = f'https://api.nasdaq.com/api/company/{symbol}/company-profile'
    jo = get_json(url)
    
    print(jo)


def get_metadata(symbol):
    url = f'https://api.nasdaq.com/api/company/{symbol}/company-profile'
    headers = {}
    jo = get_json(url, headers)

    metadata = pd.Series([], name=symbol)
    if ('data' in jo) and (jo['data'] is not None):
        metadata = pd.DataFrame(jo['data']).loc['value'].rename(symbol)
    
    return metadata


if False:
    pd.concat([get_metadata(s) for s in ['AMZN', 'GOOGL', 'AAAU']], axis=1).T