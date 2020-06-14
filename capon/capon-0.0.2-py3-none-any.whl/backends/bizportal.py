import json
import pandas as pd
import requests
import os

# ROOT = "tests/test_stocke"
ROOT = os.path.dirname(__file__)

"""
# YEARLY
curl \
	'https://www.bizportal.co.il/forex/quote/ajaxrequests/paperdatagraphjson?period=yearly&paperID=50100176' \
	-H 'authority: www.bizportal.co.il' \
	-H 'accept: */*' \
	-H 'sec-fetch-dest: empty' \
	-H 'x-requested-with: XMLHttpRequest' \
	-H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' \
	-H 'sec-fetch-site: same-origin' \
	-H 'sec-fetch-mode: cors' \
	-H 'referer: https://www.bizportal.co.il/foreign/quote/generalview/50100176' \
	-H 'accept-language: en-US,en;q=0.9,he;q=0.8' \
	-H 'cookie: ASP.NET_SessionId=25qbhllu0jmpyznocrcqfqvc; bizNewArticle778515=1; _ga=GA1.3.1307258880.1584625340; __gads=ID=60e580a8f44092f7:T=1584625367:S=ALNI_MZyUiI4u3LdI0SMCeKwTwF3jc9Cyg; desktopPoweredLink=https%3A%2F%2Ftoolkit.ex.co%2Fwatermark_lp%2F%3Futm_campaign%3DWatermark%26utm_source%3Dwatermark; _hjid=bd7bc8aa-4987-40b7-88d7-167c784145f4; OB-USER-TOKEN=e09a8001-cd06-4ec9-8828-80a9ea5f8239; bizNewArticle778966=1; AMUUID=kkoGa7Goq1JR%2BxJSk%2Fu1h0422dYWIxgQYi7h1e4b228oJRvUTyW9LTgxzQWAo%2BXY; bizNewArticle778968=1; _gid=GA1.3.550940330.1586347717; vad-loc-code=il; ServerId=5202639310; _gat_gtag_UA_6254881_1=1' \
	--compressed


# Daily
curl 'https://www.bizportal.co.il/forex/quote/ajaxrequests/paperdatagraphjson?period=daily&paperID=50100176' \
    -H 'authority: www.bizportal.co.il' \
    -H 'accept: */*' \
    -H 'sec-fetch-dest: empty' \
    -H 'x-requested-with: XMLHttpRequest' \
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' \
    -H 'sec-fetch-site: same-origin' \
    -H 'sec-fetch-mode: cors' \
    -H 'referer: https://www.bizportal.co.il/foreign/quote/generalview/50100176' \
    -H 'accept-language: en-US,en;q=0.9,he;q=0.8' 
    -H 'cookie: ASP.NET_SessionId=25qbhllu0jmpyznocrcqfqvc; bizNewArticle778515=1; _ga=GA1.3.1307258880.1584625340; __gads=ID=60e580a8f44092f7:T=1584625367:S=ALNI_MZyUiI4u3LdI0SMCeKwTwF3jc9Cyg; desktopPoweredLink=https%3A%2F%2Ftoolkit.ex.co%2Fwatermark_lp%2F%3Futm_campaign%3DWatermark%26utm_source%3Dwatermark; _hjid=bd7bc8aa-4987-40b7-88d7-167c784145f4; OB-USER-TOKEN=e09a8001-cd06-4ec9-8828-80a9ea5f8239; bizNewArticle778966=1; AMUUID=kkoGa7Goq1JR%2BxJSk%2Fu1h0422dYWIxgQYi7h1e4b228oJRvUTyW9LTgxzQWAo%2BXY; bizNewArticle778968=1; _gid=GA1.3.550940330.1586347717; vad-loc-code=il; ServerId=5202639310; vadDirectV2-loc-code=il; _gat_gtag_UA_6254881_1=1' \
    --compressed
"""



periods = ['fiveyearly', 'yearly', 'daily']

def stock_get(fund_id, period='yearly', save=False,):
    headers = {
        'authority': 'www.bizportal.co.il',
        'accept': '*/*',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': f'https://www.bizportal.co.il/foreign/quote/generalview/{fund_id}',
        'accept-language': 'en-US,en;q=0.9,he;q=0.8',
        'cookie': 'ASP.NET_SessionId=25qbhllu0jmpyznocrcqfqvc; bizNewArticle778515=1; _ga=GA1.3.1307258880.1584625340; __gads=ID=60e580a8f44092f7:T=1584625367:S=ALNI_MZyUiI4u3LdI0SMCeKwTwF3jc9Cyg; desktopPoweredLink=https%3A%2F%2Ftoolkit.ex.co%2Fwatermark_lp%2F%3Futm_campaign%3DWatermark%26utm_source%3Dwatermark; _hjid=bd7bc8aa-4987-40b7-88d7-167c784145f4; OB-USER-TOKEN=e09a8001-cd06-4ec9-8828-80a9ea5f8239; bizNewArticle778966=1; AMUUID=kkoGa7Goq1JR%2BxJSk%2Fu1h0422dYWIxgQYi7h1e4b228oJRvUTyW9LTgxzQWAo%2BXY; bizNewArticle778968=1; _gid=GA1.3.550940330.1586347717; vad-loc-code=il; ServerId=5202639310; _gat_gtag_UA_6254881_1=1',
    }

    proxies = {
        # 'http': 'http://proxy:8080',
        # 'https': 'http://proxy:8080',
    }
    url = f'https://www.bizportal.co.il/forex/quote/ajaxrequests/paperdatagraphjson?period={period}&paperID={fund_id}'
    response = requests.get(url, headers=headers)
    print("%s.. %d" % (response.url,response.status_code))

    if save:
        with open('%s/biz/funds/bizportal_%d.json'%(ROOT,fund_id), 'w') as outf:
            outf.write(response.content)

    jo = response.json()
    return jo


def stock(stock_id, period='yearly', normalize=False, cache=True):
    if cache:
        # http://www.bizportal.co.il/mutualfunds/quote/generalview/5117759
        with open('%s/biz/funds/bizportal_%d.json'%(ROOT,stock_id)) as data_file:
            jo = json.load(data_file)
    else:
        jo = stock_get(stock_id, period=period)

    points = jo['points']
    df = pd.DataFrame(points) \
        .rename({'C_p':'Price', 'D_p':'Date', 'T_p':'C', 'V_p':'Delta'}, axis=1) \
        .assign(PaperId=jo['paperId'], PaperName=jo['paperName'])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

    if normalize:
        df["Price"] -= df["Price"].min()
        df["Price"] /= (df["Price"].max()-df["Price"].min())

    return df


def funds_list():
    return pd.read_csv("%s/biz/Funds_en.csv"%ROOT)


GOOGL = 50100267
AMZN = 50100010
TSLA = 50100261

ALLY = 90911156
DFS = 90200944

if False:
    stock_id = AMZN
    period = 'yearly'
    # period = 'daily'


    jo = stock_get(stock_id, period=period)
    s = stock(stock_id, period=period, cache=False)
    s.plot('Date', 'Price')

    stock(TSLA, period=period, cache=False).plot('Date', 'Price')

if False:

    stock_ids = [GOOGL, AMZN]
    stocks = pd.concat([stock(stock_id, period=period, cache=False) for stock_id in stock_ids])

    import seaborn as sns
    sns.lineplot(x='Date', y='Price', hue='PaperName', data=stocks)

    import plotly.express as px
    px.defaults.template = 'plotly_dark'
    px.line(stocks, x='Date', y='Price', color='PaperName')




if True:
    # Yahoo Finance

    def get_stock(symbol):
        # 1Y (w)
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?region=US&lang=en-US&includePrePost=false&interval=1wk&range=1y&corsDomain=finance.yahoo.com&.tsrc=finance'
        # 1Y (d)
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?region=US&lang=en-US&includePrePost=false&interval=1d&range=1y&corsDomain=finance.yahoo.com&.tsrc=finance'

        # # 1d
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'


        headers = {}
        response = requests.get(url, headers=headers)
        print("%s.. %d" % (response.url, response.status_code))

        jo = response.json()

        return jo

    # jo = get_stock('AMZN')
    # jo = get_stock('ALLY')
    # print(jo.keys(), 
    #     jo['chart'].keys(), 
    #     len(jo['chart']['result']), 
    #     jo['chart']['result'][0].keys(), 
    #     jo['chart']['result'][0]['indicators'].keys(), 
    #     len(jo['chart']['result'][0]['indicators']['quote'])
    # )


    def stock(symbol):
        jo = get_stock(symbol)

        result = jo['chart']['result'][0]
        metadata = result['meta']
        ts = pd.DataFrame({'timestamp': pd.to_datetime(result['timestamp'], unit='s')}).assign(symbol=metadata['symbol'])
        quote = pd.DataFrame(result['indicators']['quote'][0])
        adjclose = pd.DataFrame(result['indicators']['adjclose'][0]) if 'adjclose' in result['indicators'] else None

        # len(ts), len(quote), len(adjclose)
        stock = pd.concat([ts, quote, adjclose], axis=1)        
        return stock

    s = stock('AMZN')
    display(s)

    # stock.plot(x='timestamp', y='close')

    import plotly.express as px; px.defaults.template = 'plotly_dark'
    px.line(s, x='timestamp', y='close', color='symbol')



    stock_ids = ['GOOGL', 'AMZN']
    stock_ids = ['ALLY', 'DFS']
    stocks = pd.concat([stock(stock_id) for stock_id in stock_ids])
    px.line(stocks, x='timestamp', y='close', color='symbol')


    a, b = stocks['symbol'].unique()
    a, b = stocks[stocks['symbol']==a], stocks[stocks['symbol']==b]
    a, b = a['close'].fillna(0), b['close'].fillna(0)

    import numpy as np
    import matplotlib.pyplot as plt
    c = np.correlate(a, b, 'full')
    plt.plot(c)

    plt.xcorr(a, b, usevlines=True, maxlags=50, normed=True, lw=2)