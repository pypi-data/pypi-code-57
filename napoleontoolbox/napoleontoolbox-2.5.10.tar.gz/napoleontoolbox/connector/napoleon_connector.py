#!/usr/bin/env python3
# coding: utf-8

""" Object to connect to the NaPoleonX database. """

# Built-in packages
import datetime
import requests
import time
import json

# Third party packages
import pandas as pd
import pickle
from datetime import datetime as dt
# Local packages

__all__ = ['NaPoleonXConnector']

def save_pickled_list(list_to_save = None, local_root_directory= '../data/', list_pkl_file_name = 'my_list.pkl'):
    with open(local_root_directory+list_pkl_file_name, 'wb') as f:
        pickle.dump(list_to_save, f)

def load_pickled_list( local_root_directory= '../data/', list_pkl_file_name = 'my_list.pkl'):
    with open(local_root_directory+list_pkl_file_name, 'rb') as f:
        my_list = pickle.load(f)
    return my_list

def request_minute_data_paquet(url, me_ts, ssj):
    r = requests.get(url.format(ssj, me_ts))
    dataframe = None
    try:
        dataframe = pd.DataFrame(json.loads(r.text)['Data']['Data'])
    except Exception as e:
        print('no data')
    return dataframe

def request_hour_data_paquet(url, me_ts, ssj):
    r = requests.get(url.format(ssj, me_ts))
    dataframe = None
    try:
        dataframe = pd.DataFrame(json.loads(r.text)['Data'])
    except Exception as e:
        print('no data')
    return dataframe

def request_day_data_paquet(url, me_ts, ssj):
    r = requests.get(url.format(ssj, me_ts))
    dataframe = None
    try:
        dataframe = pd.DataFrame(json.loads(r.text)['Data'])
    except Exception as e:
        print('no data')
    return dataframe

def fetch_crypto_daily_data(ssj=None, local_root_directory=None, daily_return_pkl_filename_suffix=None, refetch_all=True,daily_crypto_starting_day='2012-01-01', daily_crypto_ending_day=None,ssj_against='USDT', exchange = 'binance'):
    dates_stub = daily_crypto_starting_day.strftime('%d_%b_%Y') + '_' + daily_crypto_ending_day.strftime('%d_%b_%Y')
    pickle_saving_path = local_root_directory+ssj+'_'+dates_stub+daily_return_pkl_filename_suffix
    if refetch_all:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.utcnow().hour
        ts = datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc).timestamp() + hour * 3600
        ts1 = ts - 2001 * 3600 * 24
        ts2 = ts1 - 2001 * 3600 * 24
        ts3 = ts2 - 2001 * 3600 * 24
        ts4 = ts3 - 2001 * 3600 * 24
        ts5 = ts4 - 2001 * 3600 * 24
        ts6 = ts5 - 2001 * 3600 * 24
        ts7 = ts6 - 2001 * 3600 * 24
        ts8 = ts7 - 2001 * 3600 * 24

        print('Loading data')
        day_url_request = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym='+ssj_against+'&e='+exchange+'&toTs={}&limit=2000'
        dataframe = None
        for me_timestamp in [ts8,ts7,ts6,ts5,ts4,ts3,ts2,ts1,ts]:
            print('waiting')
            df = request_day_data_paquet(day_url_request, me_timestamp, ssj)
            if df is not None:
                if dataframe is not None:
                    dataframe = dataframe.append(df, ignore_index=True)
                else:
                    dataframe = df.copy()


        dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
        dataframe = dataframe.sort_values(by=['time'])
        dataframe = dataframe.rename(columns={"time": "date"}, errors="raise")
        dataframe = dataframe.set_index(dataframe['date'])
        dataframe = dataframe.drop(columns=['date'])
        print('size fetched')
        print(dataframe.shape)
        dataframe = dataframe[dataframe.index >= daily_crypto_starting_day]
        dataframe = dataframe[dataframe.index <= daily_crypto_ending_day]
        print('size filtered after '+str(daily_crypto_starting_day))
        print(dataframe.shape)
        dataframe.to_pickle(pickle_saving_path)
    else:
        dataframe = pd.read_pickle(pickle_saving_path)
    return dataframe




def fetch_crypto_minutely_data(ssj=None, local_root_directory=None, minutely_return_pkl_filename_suffix=None, running_date= None, daily_crypto_starting_day='2012-01-01', daily_crypto_ending_day=None, refetch_all=True, ssj_against='USDT', exchange = 'binance'):
    dates_stub = daily_crypto_starting_day.strftime('%d_%b_%Y') + '_' + daily_crypto_ending_day.strftime('%d_%b_%Y')
    pickle_saving_path = local_root_directory+ssj+'_'+dates_stub+minutely_return_pkl_filename_suffix
    if refetch_all:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.utcnow().hour
        ts = datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc).timestamp() + hour * 3600
        ts1 = ts - 2001 * 60
        ts2 = ts1 - 2001 * 60
        ts3 = ts2 - 2001 * 60
        ts4 = ts3 - 2001 * 60
        ts5 = ts4 - 2001 * 60
        ts6 = ts5 - 2001 * 60
        ts7 = ts6 - 2001 * 60
        ts8 = ts7 - 2001 * 60
        ts9 = ts8 - 2001 * 60
        ts10 = ts9 - 2001 * 60
        ts11 = ts10 - 2001 * 60
        ts12 = ts11 - 2001 * 60
        print('Loading data')
        binance_min_usdt_url = 'https://min-api.cryptocompare.com/data/v2/histominute?fsym={}&tsym='+ssj_against+'&e='+exchange+'&toTs={}&limit=2000'

        dataframe = None
        for me_timestamp in [ts12,ts11,ts10,ts9,ts8,ts7,ts6,ts5,ts4,ts3,ts2,ts1,ts]:
            print('waiting')
            df = request_minute_data_paquet(binance_min_usdt_url, me_timestamp, ssj)
            if df is not None:
                if dataframe is not None:
                    dataframe = dataframe.append(df, ignore_index=True)
                else:
                    dataframe = df.copy()

        dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
        dataframe = dataframe.sort_values(by=['time'])
        dataframe = dataframe.rename(columns={"time": "date"}, errors="raise")
        dataframe = dataframe.set_index(dataframe['date'])
        dataframe = dataframe.drop(columns=['date'])
        print('size fetched')
        print(dataframe.shape)
        dataframe.to_pickle(pickle_saving_path)
    else:
        dataframe = pd.read_pickle(pickle_saving_path)
    return dataframe


def fetch_crypto_hourly_data(ssj=None, local_root_directory=None, hourly_return_pkl_filename_suffix=None,refetch_all=True, daily_crypto_starting_day='2012-01-01', daily_crypto_ending_day=None, ssj_against='USDT', exchange = 'binance'):
    dates_stub = daily_crypto_starting_day.strftime('%d_%b_%Y') + '_' + daily_crypto_ending_day.strftime('%d_%b_%Y')
    pickle_saving_path = local_root_directory + ssj + '_' + dates_stub + hourly_return_pkl_filename_suffix
    if refetch_all:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.utcnow().hour
        ts = datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc).timestamp() + hour * 3600
        ts1 = ts - 2001 * 3600
        ts2 = ts1 - 2001 * 3600
        ts3 = ts2 - 2001 * 3600
        ts4 = ts3 - 2001 * 3600
        ts5 = ts4 - 2001 * 3600
        ts6 = ts5 - 2001 * 3600
        ts7 = ts6 - 2001 * 3600
        ts8 = ts7 - 2001 * 3600
        ts9 = ts8 - 2001 * 3600
        ts10 = ts9 - 2001 * 3600
        ts11 = ts10 - 2001 * 3600
        ts12 = ts11 - 2001 * 3600
        ts13 = ts12 - 2001 * 3600
        print('Loading data')
        hours_url_request = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=' + ssj_against + '&e=' + exchange + '&toTs={}&limit=2000'
        dataframe = None
        for me_timestamp in [ts13, ts12, ts11, ts10, ts9, ts8, ts7, ts6, ts5, ts4, ts3, ts2, ts1, ts]:
            print('waiting')
            df = request_hour_data_paquet(hours_url_request, me_timestamp, ssj)
            if df is not None:
                if dataframe is not None:
                    dataframe = dataframe.append(df, ignore_index=True)
                else:
                    dataframe = df.copy()

        dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
        dataframe = dataframe.sort_values(by=['time'])
        dataframe = dataframe.rename(columns={"time": "date"}, errors="raise")
        dataframe = dataframe.set_index(dataframe['date'])
        dataframe = dataframe.drop(columns=['date'])
        print('size fetched')
        print(dataframe.shape)
        dataframe = dataframe[dataframe.index >= daily_crypto_starting_day]
        print('size filtered after '+str(daily_crypto_starting_day))
        print(dataframe.shape)
        dataframe.to_pickle(pickle_saving_path)
    else:
        dataframe = pd.read_pickle(pickle_saving_path)
    return dataframe

def fetch_crypto_tuple_hourly_data(ssj=None, pickle_saving_path=None, refetch_all=True, frequency=4):
    if refetch_all:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.utcnow().hour
        ts = datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc).timestamp() + hour * 3600
        ts1 = ts - 2001 * 3600
        ts2 = ts1 - 2001 * 3600
        ts3 = ts2 - 2001 * 3600
        ts4 = ts3 - 2001 * 3600
        ts5 = ts4 - 2001 * 3600
        ts6 = ts5 - 2001 * 3600
        ts7 = ts6 - 2001 * 3600
        ts8 = ts7 - 2001 * 3600
        ts9 = ts8 - 2001 * 3600
        ts10 = ts9 - 2001 * 3600
        ts11 = ts10 - 2001 * 3600
        ts12 = ts11 - 2001 * 3600
        ts13 = ts12 - 2001 * 3600
        print('Loading data')
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts13))
        dataframe = pd.DataFrame(json.loads(r.text)['Data'])
        print('waiting')
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts12))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        print('waiting')
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts11))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        print('waiting')
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts10))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        print('waiting')
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts9))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        print('waiting')
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts8))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        print('waiting')
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts7))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        print('waiting')
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts6))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        print('waiting')
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts5))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        time.sleep(1)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts4))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts3))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts2))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts1))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)
        r = requests.get(
            'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&toTs={}&limit=2000'.format(ssj, ts))
        df = pd.DataFrame(json.loads(r.text)['Data'])
        dataframe = dataframe.append(df, ignore_index=True)

        dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
        dataframe = dataframe.sort_values(by=['time'])
        dataframe = dataframe.rename(columns={"time": "date"}, errors="raise")
        dataframe = dataframe.set_index(dataframe['date'])
        dataframe = dataframe.drop(columns=['date'])
        dataframe = dataframe.iloc[::frequency, :]
        print('size fetched')
        print(dataframe.shape)
        dataframe.to_pickle(pickle_saving_path)
    else:
        dataframe = pd.read_pickle(pickle_saving_path)
    return dataframe



class NaPoleonXConnector(object):
    """ Object to connect to the NaPoleonX database.

    Parameters
    ----------
    username, password, client_id, client_secret : str
        Identifier to request the API.

    Attributes
    ----------
    token : str
        token to identify client.

    Methods
    -------
    get_data
    get_dataframe

    """

    url_auth = 'https://api.napoleonx.ai/auth-service/oauth/token'
    url = 'https://api.napoleonx.ai/quote-service/v1/eod-quote/filter'
    signal_url = 'https://api.napoleonx.ai/position-service/v1/signal-computation/filter'
    url_product = 'https://api.napoleonx.ai/product-service/v1/product/'
    data = {
        'grant_type': 'password',
        # 'username': 'arthur',
        # 'password': 'arthurBernard-coiffeur!digital_with-machine&learning',
        'scope': 'read write'
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }

    # client_id = 'postman'
    # client_secret = 'bKTn8a2vp4'

    def __init__(self, username, password, client_id, client_secret):
        """ Initialize object. """
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

        self.data.update({'username': username, 'password': password})

        response = requests.post(
            self.url_auth,
            data=self.data,
            headers=self.headers,
            auth=auth
        ).json()

        # Set token
        self.token = response['access_token']
        self.token_type = response['token_type']
        self._set_header()

    def _set_header(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': "{} {}".format(
                self.token_type,
                self.token
            ),
            'cache-control': "no-cache"
        }

    def _post_request(self, url, **kwargs):
        data = json.dumps(kwargs)
        return requests.post(url, data=data, headers=self.headers).json()

    def _get_request(self, url, **kwargs):
        data = json.dumps(kwargs)
        return requests.get(url, data=data, headers=self.headers).json()

    def get_signal_data(self, productCodes, minTs, maxTs, lastOnly):
        return self._post_request(
            self.signal_url,
            productCodes=productCodes,
            minTs=minTs,
            maxTs=maxTs,
            lastOnly=lastOnly
        )

    def get_data(self, productCodes, minDate, maxDate):
        """ Request data.

        Parameters
        ----------
        productCodes : list of str
            List of codes of assets.
        minDate, maxDate : str
            Respectively the first and last date of the data.
        kwargs
            Key word arguments for requests the database.

        Returns
        -------
        dict
            Data.

        """
        return self._post_request(
            self.url,
            productCodes=productCodes,
            minDate=minDate,
            maxDate=maxDate,
            lastOnly = True
        )

    def get_product_data(self, productCodes):
        return self._post_request(
            self.url_product,
            productCodes=productCodes
        )

    def _set_dataframe(self, data, assets, keep=['close']):
        """ Clean, sort and set data into the dataframe.

        Parameters
        ----------
        data : pandas.DataFrame
            Dataframe of not ordered data.
        assets : list of str
            List of code of assets.
        keep : list of str
            List of columns to keep into the dataframe.

        Returns
        -------
        pandas.DataFrame
            Where each column is an asset price and each row is a date.

        """
        columns, asset_col = {}, []
        for asset in assets:
            if len(keep) > 1:
                columns[asset] = {k: k + '_' + asset for k in keep}
                asset_col += [k + '_' + asset for k in keep]

            else:
                columns[asset] = {keep[0]: asset}
                asset_col += [asset]

        df = pd.DataFrame(
            columns=asset_col,
            index=sorted(data.date.drop_duplicates()),
        )

        for asset in assets:
            sub_df = (data.loc[data.productCode == asset, keep + ['date']]
                          .set_index('date')
                          .sort_index()
                          .rename(columns=columns[asset]))
            asset_col = list(columns[asset].values())
            df.loc[sub_df.index, asset_col] = sub_df.loc[:, asset_col]
        return df

    def get_vm_rates_dataframe(self, productCodes, minDate, maxDate):
        currencies = set([self.get_currency(product_code) for product_code in productCodes])
        vm_rates_product_codes = [f'VM-EUR-{currency}' for currency in currencies if currency != 'EUR']
        return self.get_dataframe(vm_rates_product_codes, minDate, maxDate)

    def get_dataframe(self, productCodes, minDate, maxDate, keep=['close'],
                      process_na=None):
        """ Request data, clean, sort, and set into pandas dataframe.

        Parameters
        ----------
        productCodes : list of str
            List of codes of assets.
        minDate, maxDate : str
            Respectively the first and last date of the data.
        keep : list of str
            List of columns to keep into the dataframe.
        process_na : {None, 'fill', 'drop'}
            - If None don't return dataframe with nan values.
            - If 'fill' replace nan by the last observation or by the next one.
            - If 'drop' drop the nan values.

        Returns
        -------
        pd.DataFrame
            Cleaned dataframe.

        """
        data = pd.DataFrame(self.get_data(productCodes, minDate, maxDate))
        df = self._set_dataframe(data, assets=productCodes, keep=keep)
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

        if process_na == 'fill':

            return df.fillna(method='ffill').fillna(method='bfill')

        elif process_na == 'drop':

            return df.dropna()

        return df

    def get_signal_dataframe(self, productCodes, minDate, maxDate):
        minTs = dt.strptime(minDate, '%Y-%m-%d').strftime('%Y-%m-%d') + 'T00:00:00'
        maxTs = dt.strptime(maxDate, '%Y-%m-%d').strftime('%Y-%m-%d') + 'T23:59:59'
        signals_df = pd.DataFrame(self.get_signal_data(productCodes,  minTs, maxTs, True))
        return signals_df

    def get_underlyings(self, productCode):
        data = self._get_request(self.url_product + productCode)
        return data['underlyings']

    def get_currency(self, productCode):
        data = self._get_request(self.url_product + productCode)
        return data['currency']

