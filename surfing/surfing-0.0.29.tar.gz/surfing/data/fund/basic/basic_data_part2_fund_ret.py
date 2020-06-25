
import pandas as pd
import numpy as np
import datetime
import traceback
from ...api.raw import RawDataApi
from ...api.basic import BasicDataApi
from .basic_data_part1 import BasicDataPart1
from ...view.basic_models import *
from .basic_data_helper import BasicDataHelper


class BasicFundRet(BasicDataPart1):
    # inport end date , none std,
    W_1 = 5
    M_1 = 20
    M_3 = 60
    M_6 = 121
    Y_1 = 242
    SMALL_NUMBER = 1e-8

    def __init__(self, data_helper: BasicDataHelper):
        self._data_helper = data_helper
        self.raw_api = RawDataApi()
        self.basic_api = BasicDataApi()
        BasicDataPart1.__init__(self, self._data_helper)

    def init(self, start_date, end_date):
        self.start_date = start_date if isinstance(start_date, datetime.date) else datetime.datetime.strptime(start_date,'%Y%m%d').date()
        self.end_date = end_date if isinstance(end_date, datetime.date) else datetime.datetime.strptime(end_date,'%Y%m%d').date()
        self.fund_list = self._fund_info_df.fund_id.tolist()
        self.fund_nav = self.basic_api.get_fund_nav_with_date(self.start_date, self.end_date, self.fund_list)
        self.fund_scale = self.raw_api.get_em_fund_scale(self.start_date, self.end_date)
        self.index_list = list(set(self._fund_info_df.index_id))
        self._fund_to_enddate_dict = self._fund_info_df[['fund_id', 'end_date']].set_index('fund_id').to_dict()['end_date']
        self.fund_nav = self.fund_nav.pivot_table(index='datetime', columns='fund_id', values='adjusted_net_value').fillna(method='ffill')

        # 超过基金终止日的基金净值赋空
        for fund_id in self.fund_nav.columns:
            fund_end_date = self._fund_to_enddate_dict[fund_id]
            if self.end_date > fund_end_date:
                self.fund_nav.loc[fund_end_date:,fund_id] = np.nan
        # 基金规模数据表更新fund_id
        self.fund_scale['fund_id'] = self.fund_scale.apply(
            lambda x: self._data_helper._get_fund_id_from_order_book_id(x['CODES'].split('.')[0], x['DATES']), axis=1)
        self.fund_scale = self.fund_scale.rename(columns={'DATES':'datetime'})[['datetime','FUNDSCALE','fund_id']].pivot_table(index='datetime',values='FUNDSCALE',columns='fund_id')
        self.fund_scale = self.fund_scale.reindex(self.fund_nav.index).fillna(method='ffill').iloc[-1]
        # 基金天数
        _get_days = lambda x : pd.Series(x).count()
        self.days = self.fund_nav.count() - 1

    def get_annual_ret(self):
        '''
        累积年化收益
        exp(log(p[-1] / p[0]) / (trade_days / 242)) - 1
        '''
        self.log_total_ret = np.log(self.total_ret)
        ret_yearly = self.days / self.Y_1
        return np.exp(self.log_total_ret / ret_yearly) - 1

    def get_annual_vol(self):
        '''
        累积年化波动率
        (p.shift(1) / p).std(ddof=1) * np.sqrt((days - 1) / year)
        '''
        diff = self.fund_nav.shift(1) / self.fund_nav
        std = diff.std(ddof=1)
        std_yearly = np.sqrt((self.days - 1) / (self.days / self.Y_1))
        return std * std_yearly

    def get_mdd(self):
        '''
        累积最大回撤
        1 - (p / p.cummax()).min()
        '''
        return 1 - (self.fund_nav / self.fund_nav.cummax()).min()

    def calculate_one_date(self):
        self.w1_ret = self.fund_nav.iloc[-1] / self.fund_nav.iloc[-1 - self.W_1 ] - 1
        self.m1_ret = self.fund_nav.iloc[-1] / self.fund_nav.iloc[-1 - self.M_1 ] - 1
        self.m3_ret = self.fund_nav.iloc[-1] / self.fund_nav.iloc[-1 - self.M_3 ] - 1
        self.m6_ret = self.fund_nav.iloc[-1] / self.fund_nav.iloc[-1 - self.M_6 ] - 1
        self.y1_ret = self.fund_nav.iloc[-1] / self.fund_nav.iloc[-1 - self.Y_1 ] - 1

        self.total_ret = self.fund_nav.iloc[-1] / self.fund_nav.fillna(method = 'bfill').iloc[0]
        self.to_date_ret = self.total_ret - 1
        self.annual_ret = self.get_annual_ret()
        self.annual_vol = self.get_annual_vol()
        self.sharpe_ratio = self.annual_ret / self.annual_vol
        self.mdd = self.get_mdd()

        data_list = [self.w1_ret, self.m1_ret, self.m3_ret, self.m6_ret, self.y1_ret, self.to_date_ret, self.fund_scale, self.annual_ret, self.sharpe_ratio, self.mdd]
        fac_list = ['w1_ret', 'm1_ret', 'm3_ret', 'm6_ret', 'y1_ret', 'to_date_ret', 'avg_size', 'annual_ret', 'sharpe_ratio', 'mdd']
        self.res = []
        for name, data in zip(fac_list, data_list):
            df = pd.DataFrame(data).rename(columns = {0:name,self.fund_nav.index[-1]:'avg_size'})
            self.res.append(df)
        self.result = pd.concat(self.res, axis=1, sort=True).reset_index().rename(columns={'index':'fund_id'})
        self.result['datetime'] = self.fund_nav.index[-1]

    def process_all(self, end_date):
        failed_tasks = []
        try:
            default_begin_date = '20050101'#算累积指标用较久对起始日
            self.init(default_begin_date, end_date)
            self.calculate_one_date()
            self._data_helper._upload_basic(self.result, FundRet.__table__.name)

        except Exception as e:
            print(e)
            traceback.print_stack()
            failed_tasks.append('fund_score')

        return failed_tasks
