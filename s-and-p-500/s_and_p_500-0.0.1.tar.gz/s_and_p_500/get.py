from bs4 import BeautifulSoup
from datetime import date, timedelta
import pandas as pd 
import numpy as np
import os
import requests
import pickle
import yfinance as yf


def get_firms():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
    
    for i in range(len(tickers)):
        temp_tick = tickers[i]
        tickers[i] = temp_tick[:-1]
        
    return tickers

def get_index(start_date=date(2000, 1, 1), end_date=date.today()) -> pd.DataFrame:
    # download s&p 500 data
    data = yf.download("^GSPC", interval="1d", start=date(2000, 1, 1), end=date.today())["Adj Close"]

    # fill in weekends for ease of use
    idx = pd.date_range(start=start_date, end=end_date-timedelta(days=1))
    data = data.reindex(idx, fill_value=np.NaN)
    data.fillna(method="ffill", inplace=True)

    # drop NaNs
    data.dropna(inplace=True)
    return data

if __name__ == "__main__":
    # idx = get_index()
    # print()
    print(get_index())
    # data = yf.download("^GSPC", interval="1d", start=date(2000, 1, 1), end=date.today())["Adj Close"]