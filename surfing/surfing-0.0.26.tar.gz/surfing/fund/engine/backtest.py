import datetime
import copy
import json
import numpy as np
import pandas as pd
import os
import time

from .asset_helper import SAAHelper, TAAHelper, FAHelper
from .trader import AssetTrader, FundTrader
from .report import ReportHelper
from ...data.manager.manager_fund import FundDataManager
from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue
from ...data.struct import FundPosition, TAAParam, AssetTradeParam, FundTradeParam, FAParam

class FundEngine:

    DEFAULT_CASH_VALUE = 1e8

    def __init__(self, data_manager: FundDataManager, trader, taa_params:TAAParam=None, fa_params:FAParam=None, taa_param_details:dict=None):
        self._dm = data_manager
        self._saa_helper = SAAHelper()
        self._taa_helper = TAAHelper(taa_params=taa_params, taa_param_details=taa_param_details) if taa_params or taa_param_details else None 
        self._fa_helper = FAHelper(fa_params=fa_params) if fa_params else None
        self._report_helper = ReportHelper()
        self._trader = trader
        self._pending_trades = []
        assert not self.is_fund_backtest or self._fa_helper, 'if this is a fund backtest, fa_helper is necessary'

    def init(self):
        if not self._dm.inited:
            self._dm.init()
        self._saa_helper.init()
        if self._taa_helper:
            self._taa_helper.init()
        self._report_helper.init()
        self._trader.init()
        # preps
        self._prep_fund_purchase_fees = None
        self._prep_fund_redeem_fees = None
        self._prep_asset_price = None
        self._prep_fund_nav = None
        self._prep_fund_unit_nav = None
        self._prep_fund_score = None
        self._prep_fund_score_raw = None
        self._prep_target_asset_allocation = None
        self._prep_target_fund_allocation = None

    def setup(self, saa: AssetWeight):
        # setup helpers
        self._saa_helper.setup(saa)
        if self._taa_helper:
            self._taa_helper.setup(saa)
        self._report_helper.setup(saa)
        self._trader.setup(saa)

    @property
    def is_fund_backtest(self):
        return isinstance(self._trader, FundTrader)

    def prep_data(self, dt):
        # basic
        if not self._prep_fund_purchase_fees:
            self._prep_fund_purchase_fees = self._dm.get_fund_purchase_fees()
        if not self._prep_fund_redeem_fees:
            self._prep_fund_redeem_fees = self._dm.get_fund_redeem_fees()
        # DATA
        self._prep_asset_price = self._dm.get_index_price_data(dt)
        self._prep_fund_nav = self._dm.get_fund_nav(dt) if self.is_fund_backtest else {}
        self._prep_fund_unit_nav = self._dm.get_fund_unit_nav(dt) if self.is_fund_backtest else {}
        self._prep_fund_score, self._prep_fund_score_raw = self._dm.get_fund_scores(dt) if self.is_fund_backtest else ({}, {})
        # ALLOCATION
        self._prep_target_asset_allocation = self.calc_asset_allocation(dt)
        self._prep_target_fund_allocation = self.calc_fund_allocation(dt) if self.is_fund_backtest else None

    def calc_trade(self, dt, cur_asset_position: AssetPosition, cur_fund_position: FundPosition=None):
        v_asset_position, asset_trade_list = self._trader.calc_asset_trade(dt, cur_asset_position, self._prep_asset_price, self._prep_target_asset_allocation)
        if asset_trade_list and self.is_fund_backtest:
            assert cur_fund_position, 'cur_fund_position should not be None in fund backtest run'
            assert self._prep_target_fund_allocation, 'target fund allocation should be prepared already'
            v_fund_position, fund_trade_list = self._trader.calc_fund_trade(
                dt, self._prep_target_fund_allocation, cur_fund_position, self._prep_fund_nav, 
                self._prep_fund_purchase_fees, self._prep_fund_redeem_fees
            )
            return fund_trade_list
        else:
            return asset_trade_list

    def finalize_trade(self, dt, trades: list, cur_asset_position: AssetPosition, cur_fund_position: FundPosition=None):
        if self.is_fund_backtest:
            assert cur_fund_position, 'cur_fund_position should not be None in fund backtest run'
            self._pending_trades, traded_list = self._trader.finalize_trade(dt, trades, self._prep_asset_price, cur_asset_position, cur_fund_position, self._prep_fund_nav, self._prep_fund_unit_nav,
                self._prep_fund_purchase_fees, self._prep_fund_redeem_fees)
        else:
            self._pending_trades, traded_list = self._trader.finalize_trade(dt, trades, self._prep_asset_price, cur_asset_position)
        return traded_list 

    def calc_asset_allocation(self, dt):
        cur_asset_price = self._dm.get_index_price_data(dt)
        cur_saa = self._saa_helper.on_price(dt, cur_asset_price)
        if self._taa_helper:
            asset_pct = self._dm.get_index_pcts_df(dt)
            cur_taa = self._taa_helper.on_price(dt, cur_asset_price, cur_saa, asset_pct, {})
        else:
            cur_taa = cur_saa
        return cur_taa

    def calc_fund_allocation(self, dt):
        return self._fa_helper.on_price(dt, self._prep_target_asset_allocation, self._prep_fund_score)

    def update_reporter(self, dt, trade_list, cur_asset_position: AssetPosition, cur_fund_position: FundPosition=None):
        self._report_helper.update(dt, cur_asset_position, self._prep_asset_price, self._pending_trades, cur_fund_position if self.is_fund_backtest else None, self._prep_fund_nav, trade_list, self._prep_fund_score, self._prep_fund_score_raw, self._prep_target_asset_allocation)

class FundBacktestEngine(FundEngine):

    def run(self, saa: AssetWeight, start_date: datetime.date=None, end_date: datetime.date=None, cash: float=None, print_time=False):
        cash = cash or self.DEFAULT_CASH_VALUE
        # init position
        self.cur_asset_position = AssetPosition(cash=cash)
        self.cur_fund_position = FundPosition(cash=cash) if self.is_fund_backtest else None

        self._pending_trades = []

        # init days
        start_date = start_date or self._dm.start_date
        end_date = end_date or self._dm.end_date

        # setup helpers
        self.setup(saa)

        # loop trading days
        _dts = self._dm.get_trading_days()
        dts = _dts[(_dts.datetime >= start_date) & (_dts.datetime <= end_date)].datetime # df with datetime.date
        for t in dts:
            self._run_on(t, print_time=print_time)
        # init report data
        self._report_helper.plot_init(self._dm, self._taa_helper)
        #print(self._report_helper.get_fund_stat())

    def _run_on(self, dt, print_time=False):
        _tm_start = time.time()
        # prep data
        self.prep_data(dt)
        _tm_prep_data = time.time()
        # finalize trade
        traded_list = self.finalize_trade(dt, self._pending_trades, self.cur_asset_position, self.cur_fund_position)
        _tm_finalize_trade = time.time()
        # calc trade
        trade_list = self.calc_trade(dt, self.cur_asset_position, self.cur_fund_position)
        _tm_calc_trade = time.time()
        # book trade
        self.book_trades(trade_list)
        # update
        self.update_reporter(dt, traded_list, self.cur_asset_position, self.cur_fund_position)        
        _tm_finish = time.time()

        if print_time:
            print(f'{dt} (tot){_tm_finish - _tm_start} (finalize){_tm_finalize_trade - _tm_start} (calc){_tm_calc_trade - _tm_finalize_trade} (misc){_tm_finish - _tm_calc_trade}')

    def book_trades(self, trade_list: list):
        if trade_list and len(trade_list) > 0:
            self._pending_trades += trade_list

    def get_asset_result(self):
        return self._report_helper.get_asset_stat()

    def get_fund_result(self):
        return self._report_helper.get_fund_stat()

    def get_asset_trade(self):
        return self._report_helper.get_asset_trade()

    def get_fund_trade(self):
        return self._report_helper.get_fund_trade()
        
    def plot(self, is_asset:bool=True, is_fund:bool=True):
        if is_asset:
            self._report_helper.backtest_asset_plot()
        if is_fund:
            self._report_helper.backtest_fund_plot()
    
    def plot_score(self, index_id, is_tuning=False):
        #['csi500', 'gem', 'gold', 'hs300', 'national_debt', 'sp500rmb']
        self._report_helper._plot_fund_score(index_id, is_tuning)

    def plot_taa(self, saa_mv, taa_mv, index_id):
        #['csi500', 'hs300', 'gem', 'sp500rmb']
        self._report_helper._plot_taa_saa(saa_mv, taa_mv, index_id)
        self._report_helper._index_pct_plot(index_id, saa_mv, taa_mv)

    def get_last_position(self):
        return self._report_helper.get_last_position()

    def get_last_target_fund_allocation(self):
        return self._report_helper.get_last_target_fund_allocation(self._prep_target_fund_allocation.funds)

def saa_backtest(m: FundDataManager, saa: AssetWeight):
    asset_param = AssetTradeParam() # type in here
    t = AssetTrader(asset_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=None)
    b.init()
    b.run(saa=saa)

def taa_backtest(m: FundDataManager, saa: AssetWeight):
    taa_param = TAAParam()  # type in here
    asset_param = AssetTradeParam() # type in here
    t = AssetTrader(asset_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=taa_param)
    b.init()
    b.run(saa=saa)

def fund_backtest_without_taa(m: FundDataManager, saa: AssetWeight):
    asset_param = AssetTradeParam() # type in here
    fund_param = FundTradeParam() # type in here
    t = FundTrader(asset_param, fund_param)
    fa_param = FAParam() # type in here
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=None, fa_params=fa_param)
    b.init()
    b.run(saa=saa)

def fund_backtest(m: FundDataManager, saa: AssetWeight):
    asset_param = AssetTradeParam() # type in here
    fund_param = FundTradeParam(EnableCommission=True) # type in here
    t = FundTrader(asset_param, fund_param)
    taa_param = TAAParam()  # type in here
    fa_param = FAParam() # type in here
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=taa_param, fa_params=fa_param)
    b.init()
    b.run(saa=saa)

def fund_realtime(m: FundDataManager, saa: AssetWeight):
    asset_param = AssetTradeParam() # type in here
    fund_param = FundTradeParam() # type in here
    t = FundTrader(asset_param, fund_param)
    taa_param = TAAParam()  # type in here
    fa_param = FAParam() # type in here
    b = FundEngine(data_manager=m, trader=t, taa_params=taa_param, fa_params=fa_param)
    b.init()
    b.setup(saa)
    _dts = m.get_trading_days()
    dts = _dts[(_dts.datetime >= m.start_date) & (_dts.datetime <= m.end_date)].datetime
    calc_dt = dts.iloc[0]
    final_dt = dts.iloc[1]
    cash = b.DEFAULT_CASH_VALUE
    cur_asset_position = AssetPosition(cash=cash)
    cur_fund_position = FundPosition(cash=cash)

    b.prep_data(calc_dt)
    trade_list = b.calc_trade(calc_dt, cur_asset_position, cur_fund_position)
    b.prep_data(final_dt)
    traded_list = b.finalize_trade(final_dt, trade_list, cur_asset_position, cur_fund_position)
    print(trade_list)
    print(traded_list)
    print(cur_fund_position)
    print(cur_asset_position)

def taa_result(m: FundDataManager):
    start_date=datetime.date(2010,1,1)
    end_date=datetime.date(2020,5,20)
    index_id = 'hs300'
    taaParam = TAAParam(HighThreshold = 1,
                        HighStop = 0.45,
                        HighMinus = 0.07,
                        LowStop = 0.43,
                        LowThreshold = 0.15,
                        LowPlus = 0.06) 
    return ReportHelper.get_taa_result(index_id=index_id, start_date=start_date, end_date=end_date, taaParam=taaParam, dm=m)

def test():
    from ...data.manager.score import FundScoreManager
    m = FundDataManager('20150101', '20160101', score_manager=FundScoreManager())
    m.init()

    saa = AssetWeight(
        hs300=15/100,
        csi500=5/100,
        gem=3/100,
        sp500rmb=7/100,
        national_debt=60/100,
        gold=10/100,
        cash=5/100
    )
    
    #saa_backtest(m, saa)
    #taa_backtest(m, saa)
    #fund_backtest_without_taa(m, saa)
    fund_backtest(m, saa)
    #fund_realtime(m, saa)

if __name__ == '__main__':
    # profile(file_name='/Users/cjiang/taa_perf1.txt', func=fund_backtest)
    test()