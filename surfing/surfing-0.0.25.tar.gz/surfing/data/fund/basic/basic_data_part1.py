
import pandas as pd
import traceback
import datetime
from ...api.raw import RawDataApi
from ...api.basic import BasicDataApi
from ...view.basic_models import *
from .basic_data_helper import BasicDataHelper


class BasicDataPart1(object):

    def __init__(self, data_helper: BasicDataHelper):
        self._data_helper = data_helper
        self._basic_data_api = BasicDataApi()
        self._index_info_df = self._basic_data_api.get_index_info()
        self._fund_info_df = self._basic_data_api.get_fund_info()

    def _status_mapping(self, x):
        if x == 'Open':
            return 0
        elif x == 'Suspended':
            return 1
        elif x == 'Limited':
            return 2
        elif x == 'Close':
            return 3
        else:
            return None

    def _find_tag(self, symbol, wind_class_II):
        if '沪深300' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型基金']:
            return 'A股大盘'
        elif '中证500' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型基金']:
            return 'A股中盘'
        elif '标普500' in symbol:
            return '美股大盘'
        elif '创业板' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型基金']:
            return '创业板'
        elif '德国' in symbol:
            return '德国大盘'
        elif '日本' in symbol or '日经' in symbol:
            return '日本大盘'
        elif (('国债' in symbol or '利率' in symbol or '金融债' in symbol)
              and wind_class_II in ['短期纯债型基金', '中长期纯债型基金', '被动指数型债券基金']):
            return '利率债'
        elif (('信用' in symbol or '企债' in symbol or '企业债' in symbol)
              and wind_class_II in ['短期纯债型基金', '中长期纯债型基金', '被动指数型债券基金']):
            return '信用债'
        elif '黄金' in symbol:
            return '黄金'
        elif '原油' in symbol or '石油' in symbol or '油气' in symbol:
            return '原油'
        elif ('地产' in symbol or '金融' in symbol) and ('美国'not in symbol):
            return '房地产'
        else:
            return 'null'

    def fund_info(self):
        # Update manually
        # Not verified
        track_index_df = pd.read_csv('./data/fund_track_index.csv', index_col=0)
        wind_fund_info = RawDataApi().get_wind_fund_info()
        fund_fee = RawDataApi().get_fund_fee()
        wind_fund_info['order_book_id'] = [_.split('!')[0].split('.')[0] for _ in wind_fund_info['wind_id'] ]
        res = []
        for i in wind_fund_info['wind_id']:
            if not '!' in i:
                res.append(0)
            else:
                res_i = int(i.split('!')[1].split('.')[0])
                res.append(res_i)
        wind_fund_info['transition'] = res
        wind_fund_info['fund_id'] = [o + '!' + str(t) for o, t in zip(wind_fund_info['order_book_id'], wind_fund_info['transition'])]
        wind_fund_info = wind_fund_info.set_index('fund_id')
        fund_fee = fund_fee.drop(['id','desc_name'], axis = 1).set_index('fund_id')
        wind_fund_info = wind_fund_info.join(fund_fee)
        wind_fund_info['fund_id'] = wind_fund_info.index
        wind_fund_info['asset_type'] = [self._find_tag(symbol, wind_class_II) for symbol, wind_class_II in zip(wind_fund_info['desc_name'],wind_fund_info['wind_class_2'])]
        wind_fund_info = wind_fund_info[[i.split('.')[1] == 'OF' for i in wind_fund_info['wind_id']]]
        wind_fund_info = wind_fund_info.set_index('wind_id')
        dic = {k:v for k,v in zip(self._index_info_df['desc_name'], self._index_info_df['index_id'])}
        wind_fund_info = wind_fund_info.join(track_index_df[['track_index']])
        wind_fund_info['wind_id'] = wind_fund_info.index
        wind_fund_info['track_index'] = wind_fund_info['track_index'].map(lambda x: dic.get(x,'none'))
        self._data_helper._upload_basic(wind_fund_info, FundInfo.__table__.name)

    def index_info(self):
        # Update manually
        # Not verified
        df = pd.read_csv('./data/index_info.csv')
        self._data_helper._upload_basic(df, IndexInfo.__table__.name)

    def fund_nav_from_rq(self, start_date, end_date):
        df = RawDataApi().get_rq_fund_nav(start_date, end_date)
        df['fund_id'] = df.apply(
            lambda x: self._data_helper._get_fund_id_from_order_book_id(x['order_book_id'], x['datetime']), axis=1)
        df['subscribe_status'] = df['subscribe_status'].map(self._status_mapping)
        df['redeem_status'] = df['redeem_status'].map(self._status_mapping)
        df = df[df['fund_id'].notna()]
        self._data_helper._upload_basic(df, FundNav.__table__.name)

    def fund_nav(self, start_date, end_date):
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y%m%d') - datetime.timedelta(days=5)
            del_date = start_date + datetime.timedelta(days=1)
            start_date = start_date.strftime('%Y%m%d')
            df = RawDataApi().get_em_fund_nav(start_date, end_date)
            df['fund_id'] = df.apply(
                lambda x: self._data_helper._get_fund_id_from_order_book_id(x['CODES'].split('.')[0], x['DATES']), axis=1)
            df = df.drop(['CODES'], axis=1)
            df = df[df['fund_id'].notna()]
            df = df.rename(columns={
                    'DATES': 'datetime',
                    'ORIGINALUNIT': 'unit_net_value',
                    'ORIGINALNAVACCUM': 'acc_net_value',
                    'ADJUSTEDNAV': 'adjusted_net_value',
                    'UNITYIELD10K': 'daily_profit',
                    'YIELDOF7DAYS': 'weekly_yield'
                })
            df['change_rate'] = df.adjusted_net_value / df.adjusted_net_value.shift(1) - 1
            df['weekly_yield'] = df['weekly_yield'].map(lambda x: x / 100.0)
            end_date = datetime.datetime.strptime(end_date, '%Y%m%d').date()
            BasicDataApi().delete_fund_nav(del_date, end_date)
            df = df[df.datetime >= del_date.date()]
            self._data_helper._upload_basic(df, FundNav.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def index_price(self, start_date, end_date):
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y%m%d') - datetime.timedelta(days=3)
            start_date = start_date.strftime('%Y%m%d')
            cm_index_price = RawDataApi().get_raw_cm_index_price_df(start_date, end_date)
            cxindex_index_price = RawDataApi().get_cxindex_index_price_df(start_date, end_date)
            yahoo_index_price = RawDataApi().get_yahoo_index_price_df(start_date, end_date)
            rq_index_price = RawDataApi().get_rq_index_price_df(start_date, end_date)

            df_list = []
            index_list = ['sp500', 'dax30', 'n225']
            cm_index_list = ['sp500rmb', 'dax30rmb', 'n225rmb']
            for i, c in zip(index_list, cm_index_list):
                cm_index = yahoo_index_price.copy()
                df = cm_index[cm_index['index_id'] == i]
                df = cm_index_price.set_index('datetime').join(df.drop(['_update_time'], axis=1).set_index('datetime'))
                df = df.fillna(method='ffill')
                df['close'] = df['close'] * df['usd_central_parity_rate']
                df = df[['close']]
                df['datetime'] = df.index
                df['open'] = float('Nan')
                df['high'] = float('Nan')
                df['low'] = float('Nan')
                df['volume'] = float('Nan')
                df['total_turnover'] = float('Nan')
                df['index_id'] = c
                df['ret'] = df.close / df.close.shift(1) -1
                df_list.append(df.copy())

            index_dic = {k: v for k, v in zip(
                self._index_info_df['order_book_id'], self._index_info_df['index_id']) if k != 'not_available'}
            rq_index_price['index_id'] = rq_index_price['order_book_id'].map(
                lambda x: index_dic[x])
            res = []
            for index_i in list(set(rq_index_price['order_book_id'].tolist())):
                # update gold index data from em not rq
                if index_dic[index_i] == 'gold':
                    continue 
                dftmp = rq_index_price[rq_index_price['order_book_id'] == index_i].copy()
                dftmp['ret'] = dftmp.close / dftmp.close.shift(1) - 1
                res.append(dftmp)
            rq_index_price = pd.concat(res)
            df_list.append(yahoo_index_price)
            df_list.append(cxindex_index_price)
            df_list.append(rq_index_price)

            df = pd.concat(df_list).drop(['order_book_id'], axis=1)
            df['datetime'] = pd.to_datetime(df['datetime'])
            end_date = datetime.datetime.strptime(end_date, '%Y%m%d').date()
            df = df[df.datetime == end_date]
            self._data_helper._upload_basic(df, IndexPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def fund_rating_latest(self):
        try:
            fund_rating_df = RawDataApi().get_fund_rating()
            fund_info = self._fund_info_df[['fund_id', 'order_book_id', 'start_date', 'end_date']]
            score_name = ['zs', 'sh3', 'sh5', 'jajx']
            score_dic = {}
            for s in score_name:
                score_df = fund_rating_df[['order_book_id', 'datetime', s]]
                datelist = sorted(list(set(score_df.dropna().datetime.tolist())))
                score_dic[s] = datelist[-1]
            res = []
            for s, d in score_dic.items():
                try:
                    df = fund_rating_df[['order_book_id', 'datetime', s]]
                    df = df[df['datetime'] == d]
                    con1 = fund_info['start_date'] <= d
                    con2 = fund_info['end_date'] >= d
                    fund_info_i = fund_info[con1 & con2]
                    dic = {row['order_book_id']: row['fund_id']
                        for index, row in fund_info_i.iterrows()}
                    df['fund_id'] = df['order_book_id'].map(lambda x: dic[x])
                    df = df[['fund_id', s]].copy().set_index('fund_id')
                    res.append(df)
                except Exception as e:
                    print(e)
            df = pd.concat(res, axis=1, sort=False)
            df['fund_id'] = df.index
            df['update_time'] = datetime.date.today()
            self._data_helper._upload_basic(df, FundRatingLatest.__table__.name, to_truncate=True)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def rq_stock_price(self, start_date, end_date):
        try:
            stock_price_df = RawDataApi().get_rq_stock_price(start_date, end_date)
            stock_post_price_df = RawDataApi().get_rq_stock_post_price(start_date, end_date)

            stock_post_price_df['adj_close'] = stock_post_price_df['close']
            stock_post_price_df = stock_post_price_df.filter(items=['adj_close', 'datetime', 'order_book_id'],
                axis='columns')

            stock_price_merge_df = stock_price_df.merge(stock_post_price_df, how='left', on=['datetime', 'order_book_id'])
            stock_price_merge_df['post_adj_factor'] = stock_price_merge_df['adj_close'] / stock_price_merge_df['close']
            stock_price_merge_df = stock_price_merge_df.rename(columns={'order_book_id': 'stock_id'})
            self._data_helper._upload_basic(stock_price_merge_df, StockPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def rq_fund_ret(self, start_date, end_date):
        try:
            column_rename_dict = {
                'sharp_ratio': 'sharpe_ratio',
                'last_week_return': 'w1_ret',
                'last_month_return': 'm1_ret',
                'last_three_month_return': 'm3_ret',
                'last_six_month_return': 'm6_ret',
                'last_twelve_month_return': 'y1_ret',
                'max_drop_down': 'mdd',
                'annualized_returns': 'annual_ret',
                'average_size': 'avg_size',
                'information_ratio': 'info_ratio',
                'to_date_return':'to_date_ret'
            }
            column_drop_list = ['order_book_id', 'year_to_date_return', 'annualized_risk']

            df = RawDataApi().get_rq_fund_indicator(start_date, end_date)
            df['fund_id'] = df.apply(
                lambda x: self._data_helper._get_fund_id_from_order_book_id(x['order_book_id'], x['datetime']), axis=1)
            df = df.rename(columns=column_rename_dict).drop(columns=column_drop_list)
            df = df[df['fund_id'].notnull()]

            self._data_helper._upload_basic(df, FundRet.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def stock_info(self):
        try:
            df = RawDataApi().get_stock_info()
            self._data_helper._upload_basic(df, StockInfo.__table__.name, to_truncate=True)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def fund_size(self, start_date, end_date):
        try:
            # Since fund_size in basic db is latest snapshot, we only use end_date as param
            df = RawDataApi().get_em_fund_scale(end_date, end_date)
            df['fund_id'] = df.apply(
                lambda x: self._data_helper._get_fund_id_from_order_book_id(x['CODES'].split('.')[0], x['DATES']), axis=1)
            df = df.drop(['CODES', 'DATES'], axis = 1).rename(columns={'FUNDSCALE': 'latest_size'})
            df = df[df['fund_id'].notnull()]
            self._data_helper._upload_basic(df, FundSize.__table__.name, to_truncate=True)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def trading_day_list(self, start_date, end_date):
        try:
            df = RawDataApi().get_em_tradedates(start_date, end_date)
            df = df.rename(columns={'TRADEDATES': 'datetime'})
            self._data_helper._upload_basic(df, TradingDayList.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def em_index_price(self, start_date, end_date):
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y%m%d') - datetime.timedelta(days=5)
            del_date = start_date + datetime.timedelta(days=1)
            start_date = start_date.strftime('%Y%m%d')
            index_info = BasicDataApi().get_index_info()
            em_id_list = index_info['em_id'].dropna().tolist()
            raw_index_price = RawDataApi().get_em_index_price(start_date, end_date, em_id_list)
            res = [] 
            index_id_list = []
            for em_id in em_id_list:
                df = raw_index_price[raw_index_price['em_id'] == em_id].copy()
                index_id = index_info[index_info['em_id'] == em_id].index_id.values[0]
                df.drop(['em_id'], axis = 1, inplace=True)
                df['index_id'] = index_id
                df['high'] = float('nan')
                df['low'] = float('nan')
                df['open'] = float('nan')
                df['total_turnover'] = float('nan')
                df['volume'] = float('nan')
                df['ret'] = df.close / df.close.shift(1) - 1
                res.append(df)
                if not df.empty:
                    index_id_list.append(index_id)
            BasicDataApi().delete_index_price(index_id_list, del_date, end_date)
            df = pd.concat(res, axis=0, sort=False)
            df = df[df.datetime >= del_date.date()]
            self._data_helper._upload_basic(df, IndexPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def fund_size_hold_rate_history(self):
        start_date = '20100101'
        end_date = '20200612'
        raw = RawDataApi()
        basic = BasicDataApi()
        fund_holding_rate = raw.get_em_fund_holding_rate(start_date=start_date)
        fund_scale = raw.get_em_fund_scale(start_date=start_date, end_date=end_date)
        fund_holding_rate['fund_id'] = fund_holding_rate.apply(
            lambda x: self._data_helper._get_fund_id_from_order_book_id(x['CODES'].split('.')[0], x['DATES']), axis=1)
        fund_scale['fund_id'] = fund_scale.apply(
            lambda x: self._data_helper._get_fund_id_from_order_book_id(x['CODES'].split('.')[0], x['DATES']), axis=1)
        fund_holding_rate = fund_holding_rate.drop(['CODES', '_update_time'], axis=1).rename(columns={'DATES':'datetime','HOLDPERSONALHOLDINGPCT':'personal_holds','HOLDINSTIHOLDINGPCT':'institution_holds'})
        fund_scale = fund_scale.drop(['CODES','_update_time'], axis=1).rename(columns={'DATES':'datetime','FUNDSCALE':'size'})
        fund_scale = fund_scale.dropna().drop_duplicates(subset=['size','fund_id'],keep='first')
        fund_holding_rate = fund_holding_rate.dropna()
        fund_list = list(set(fund_scale.fund_id))
        res = []
        for fund_id in fund_list:
            fund_hold_i = fund_holding_rate[fund_holding_rate.fund_id == fund_id].drop('fund_id',axis=1).set_index('datetime')
            fund_scale_i = fund_scale[fund_scale.fund_id == fund_id].drop('fund_id',axis=1).set_index('datetime')
            _df = fund_scale_i.join(fund_hold_i).fillna(method='ffill').reset_index()
            _df['fund_id'] = fund_id
            res.append(_df)
        df = pd.concat(res)
        df = df.drop_duplicates(subset=['datetime','fund_id'],keep='first')
        df = df.fillna(0)
        con_list = (df.personal_holds + df.institution_holds) == 100
        df = df[con_list]
        self._data_helper._upload_basic(df, Fund_size_and_hold_rate.__table__.name)

    def process_all(self, start_date, end_date):
        failed_tasks = []

        # Depend on RQ
        # if not self.rq_fund_ret(start_date, end_date):
        #     failed_tasks.append('rq_fund_ret')

        # # Depend on RQ
        # if not self.stock_info():
        #     failed_tasks.append('stock_info')

        # Depend on RQ
        # if not self.rq_stock_price(start_date, end_date):
        #     failed_tasks.append('rq_stock_price')

        # TODO: Depend on RQ, change to EM
        if not self.index_price(start_date, end_date):
            failed_tasks.append('index_price')

        # TODO: Depend on RQ, change to EM
        if not self.fund_rating_latest():
            failed_tasks.append('fund_rating_latest')

        if not self.fund_size(start_date, end_date):
            failed_tasks.append('fund_size')

        if not self.fund_nav(start_date, end_date):
            failed_tasks.append('fund_nav')

        if not self.em_index_price(start_date, end_date):
            failed_tasks.append('em_index_price')

        if not self.trading_day_list(start_date, end_date):
            failed_tasks.append('trading_day_list')

        return failed_tasks


if __name__ == '__main__':
    bdp = BasicDataPart1()
    # start_date = '20200428'
    # end_date = '20200428'
    # bdp.index_price(start_date, end_date)
    # bdp.em_index_price(start_date, end_date)
    # bdp.rq_stock_price(start_date, end_date)
    # bdp.rq_fund_ret(start_date, end_date)
    # bdp.fund_rating_latest()
    bdp.fund_size('20200513', '20200513')
