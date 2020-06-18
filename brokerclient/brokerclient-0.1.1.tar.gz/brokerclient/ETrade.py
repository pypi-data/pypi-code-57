from rauth import OAuth1Service
import pandas as pd
from os import path
import webbrowser
import json
import configparser
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

class keys():
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        
class devKeys(keys):
    def __init__(self):
        super().__init__(
            '034e82f343d6b1ead1d3cc7c02d3dd2d',
            '1450b0b84aac132ec10ec5ec70ee2dfa728ca562debdde49ef453f01eedceac8'
        )

class prodKeys(keys):
    def __init__(self):
        super().__init__(
            'd847c01a710843ca0320fa2e96ba935f',
            '319eefa356290b9ff95b5fcb2211c39c8a159049985b88f3f44af70a36a7a7c0'
        )
        
class urls():
    def __init__(self):
        self.base_url = "https://api.etrade.com"
        self.request_token ="{}/oauth/request_token".format(self.base_url)
        self.access_token="{}/oauth/access_token".format(self.base_url)
        self.authorize="https://us.etrade.com/e/t/etws/authorize?key={}&token={}"

class EtradeOAuth1Service(OAuth1Service):
    def __init__(self,Keys ,  Urls = None ,*args, **kwarsg):

        self.urls = urls()
        self.keys = Keys

        super().__init__(
            consumer_key= self.keys.key,
            consumer_secret=self.keys.secret,
        
            request_token_url=self.urls.request_token,
            access_token_url = self.urls.access_token,
            authorize_url=self.urls.authorize,
        )
class dateParser():
    def epochDateTime(self,time):
        if time:
            time_epoch = int(str(time)[:10])    
            return datetime.datetime.utcfromtimestamp(time_epoch)
        else:
            return None
        
class login():
    def __init__(self,Keys, Urls = None):        
        self.etrade = EtradeOAuth1Service(Keys = Keys, Urls = Urls)

    def login_web(self):
        self.req_token, self.req_token_secret = self.etrade.get_request_token(
        params={"oauth_callback": "oob", "format": "json"}     
        )        
        self.authorize_url = self.etrade.authorize_url.format(
            self.etrade.consumer_key, 
            self.req_token
        )        
        print(self.authorize_url)
        webbrowser.open_new_tab(self.authorize_url)
    
    @property
    def web_session(self):
        return self.__session
    @property
    def base_url(self):
        return self.etrade.urls.base_url

    @property
    def web_access_code(self):
        return self.__webAccessCode     
    @web_access_code.setter
    def web_access_code(self,c):
        self.__webAccessCode = c
        self.__session = self.etrade.get_auth_session(
            self.req_token,
            self.req_token_secret,
            params={"oauth_verifier":self.__webAccessCode}
        )        


class market():
    def __init__(self,aut):
        self.__session = aut.web_session
        self.__base_url = aut.base_url + "/v1/market/quote/{symbols}.json"
        
    def quotes(self,symbols):        
        response = self.__session.get(self.__base_url.format(symbols=symbols))        
        if response is not None and response.status_code == 200:
            json_response = json.loads(response.text)        
        
        df_bidask_info = pd.DataFrame([json_response['QuoteResponse']['QuoteData'][0]['All']])[
            ['bid','ask','bidSize','askSize','bidTime','askTime']
        ]
        df_prod_info = pd.DataFrame([json_response['QuoteResponse']['QuoteData'][0]['Product']])
        df = pd.concat([
            df_bidask_info,
            df_prod_info,    
        ],axis=1)
        return df
    
class ordersManager():
    def __init__(self,aut):
        self.__login=aut
        self.__session = aut.web_session
        self.__base_url = aut.base_url
        self.__account = {}
        self.__dateParser = dateParser()
        self.accountmanager = accountManager(self.__login)
        self.current_accountIdKey = self.accountmanager.first_account

    @property
    def current_accountIdKey(self):        
        return self.__accountIdKey        
    @current_accountIdKey.setter
    def current_accountIdKey(self,key):
        self.__accountIdKey = key

    def __request_data(self, url):
        response = self.__session.get(url,header_auth=True)
        if response is not None and response.status_code == 200:
            json_response = json.loads(response.text)
            return json_response
        return response.text
    
    def __parse_to_dataframe(self,ordersResponses):
        ret = []
        for ordersResponse in ordersResponses:
            for order in ordersResponse['OrdersResponse']['Order']:
                for order_detail in order.get('OrderDetail'):
                    for instrument in order_detail.get('Instrument'):
                        ret.append(
                            {
                                'orderId':order.get('orderId'),
                                'orderType':order.get('orderType'),                    
                                'symbol':instrument.get('Product').get('symbol'),
                                'status':order_detail.get('status'),
                                'order_action':instrument.get('orderAction'),
                                'priceType':order_detail.get('priceType'),
                                'limitPrice':order_detail.get('limitPrice'),
                                'placedTime':self.__dateParser.epochDateTime(order_detail.get('placedTime')),
                                'executedTime':self.__dateParser.epochDateTime(order_detail.get('executedTime')),
                                'filledQuantity':instrument.get('filledQuantity'),
                                'averageExecutionPrice':instrument.get('averageExecutionPrice'),
                                'estimatedCommission':instrument.get('estimatedCommission'),
                                'estimatedFees':instrument.get('estimatedFees'),
                            }
                        )
        return pd.DataFrame(ret)
    
    def orders_list_all(self,accountIdKey=None,json=False):
        if accountIdKey:
            self.current_accountIdKey = accountIdKey
        
        first_bach = self.orders_list(accountIdKey,json=True)        
        oldest_order = first_bach['OrdersResponse']['Order'][-1]#['orderId']
        
        older_orders_list =[]
        
        for i in range(1,oldest_order['orderId']-1):
                first_bach['OrdersResponse']['Order'].insert(
                    0,
                    self.order_detail(i)['OrdersResponse']['Order'][0]
                )
            
        if json:
            return first_bach
        else:
            return self.__parse_to_dataframe([first_bach])

        
        
    def orders_list(self,accountIdKey=None,json=False):
        
        if accountIdKey:
            self.current_accountIdKey = accountIdKey

        url = self.__base_url + "/v1/accounts/{accountIdKey}/orders.json".format(
            accountIdKey = self.current_accountIdKey
        )
        
        json_ret = self.__request_data(url)
        
        if json:
            return json_ret
        else:
            return self.__parse_to_dataframe([json_ret])

    def order_detail(self,orderId):
        url = self.__base_url + "/v1/accounts/{accountIdKey}/orders/{id}.json".format(
            accountIdKey = self.current_accountIdKey,
            id = orderId
        )
        return self.__request_data(url)

class accountManager():
    def __init__(self,aut):
        self.__session = aut.web_session
        self.__base_url = aut.base_url
        self.__account = {}
    
    def account_list(self, json_out = False):
        url = self.__base_url + "/v1/accounts/list.json"
        response = self.__session.get(url,header_auth=True)
        if json_out:
            return json.loads(response.text)
        
        if response is not None and response.status_code == 200:
            json_response = json.loads(response.text)                    

            return pd.DataFrame(
                json_response['AccountListResponse']['Accounts']['Account']
            )
        
    def __parse_product(self,row):
        row['symbol'] = row['Product']['symbol']
        row['securityType']= row['Product']['securityType']
        return row
    
    def __parse_quick(self,row):
        for k,v in row['Quick'].items():
            row['security_'+k]=v
        return row
        
    @property
    def first_account(self):
        return self.account_list().iloc[0].accountIdKey

    def portfolio(self,account_key=None):

        if not account_key:
            account_key = self.first_account

        url =self.__base_url + "/v1/accounts/{acc_key}/portfolio.json".format(
            acc_key=account_key
        )        
        response = self.__session.get(url, header_auth=True)
        if response is not None and response.status_code == 200:
            json_response = json.loads(response.text)
        
            df = pd.DataFrame(
                json_response['PortfolioResponse']['AccountPortfolio'][0]['Position']
            )
            
            df = df.apply(self.__parse_product,axis=1)
            df = df.apply(self.__parse_quick,axis=1)
            
            return df[[x for x in df.columns if x not in ['Product','Quick']]]
        return None