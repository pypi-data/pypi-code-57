import numpy as np
import matplotlib.pyplot as mpl
import sys
import yfinance as yf
import datetime


def getStockDetails(s):
    stockTicker = yf.Ticker(s)
    #stock = stockTicker.info
    #print("Stock Name : ",stock['shortName'])
    print("Stock Name : ",s)
    today = datetime.datetime.today().isoformat()
    today = today[:10]
    tickerDf = stockTicker.history(period='1d',start='2020-06-01',end=today)
    lastInvestment = tickerDf['Close'].iloc[-1]
    yestInvestment = tickerDf['Close'].iloc[-2]
    
    print("Last Price : ",lastInvestment)
    #print("Change     : ",lastInvestment-yestInvestment)
    print("Change     :{:7.2f}".format(lastInvestment-yestInvestment))
    print("Change %   :{:6.2f}%".format(((lastInvestment-yestInvestment)/yestInvestment)*100))
    print(tickerDf)

def plotStockDetails(s):
    mpl.figure(figsize=(17,10))
    today = datetime.datetime.today().isoformat()
    today = today[:10]
    for i in range(0,len(s)):
        data = yf.download(s[i], start="2000-01-01", end=today)
        mpl.plot(data['Close'])
    mpl.legend(s)
    mpl.show()  

def downloadStockDetailsCSV(s, years):
    stocks = yf.Ticker(s)
    stocks = stocks.history(years)
    stocks.to_csv('StockData['+s+'].csv')