
import dataclasses
import datetime
import pandas
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
from scipy.stats import gmean
from functools import partial
from ..data.api.basic import BasicDataApi
from ..data.struct import TAAParam, TaaTunerParam, AssetWeight
from ..data.api.derived import DerivedDataApi
from ..fund.engine.asset_helper import TAAHelper, TAAStatusMode

@dataclasses.dataclass
class SeriesStatUnit:

    start_date: datetime.date   # 序列的开始时间
    end_date: datetime.date     # 序列的结束时间
    trade_year: float           # 交易年限
    last_unit_nav: float        # 末期单位净值
    annualized_ret: float       # 年化收益
    annualized_vol: float       # 年化波动率
    sharpe: float               # 夏普率
    recent_y5_ret: float        # 近五年收益 
    mdd: float                  # 最大回撤
    mdd_date1: datetime.date    # 最大回撤开始时间
    mdd_date2: datetime.date    # 最大回撤结束时间
    ret_over_mdd: float         # Calmar 年化收益除以最大回撤
    last_mv_diff: float         # 末期市值增量              
    last_increase_rate: float   # 末期涨幅

@dataclasses.dataclass
class BenchmarkSeiesStatUnit(SeriesStatUnit):

    alpha: float                # 超额收益
    beta: float                 # 风险暴露
    track_err: float            # 跟踪误差
    ir: float                   # 信息比率

class Calculator:

    TRADING_DAYS_PER_YEAR = 242
    
    @staticmethod
    def get_risk_free_rate():
        return 0.025

    @staticmethod
    def get_stat_result(dates: pandas.core.series.Series,
                        values: pandas.core.series.Series):
        assert len(dates) == len(values), 'date and value has different numbers'
        
        if len(dates) > 1:
            sr = pandas.Series(values, index=dates).sort_index()
            risk_fee_rate = Calculator.get_risk_free_rate()
            start_date = sr.index[0] 
            end_date = sr.index[-1]
            trade_year = sr.shape[0] / Calculator.TRADING_DAYS_PER_YEAR
            last_unit_nav = sr[-1] / sr[0]
            annualized_ret = np.exp(np.log(last_unit_nav) / trade_year) - 1
            annualized_vol = (sr / sr.shift(1)).std(ddof=1) * np.sqrt(Calculator.TRADING_DAYS_PER_YEAR)
            sharpe = (annualized_ret - risk_fee_rate) / annualized_vol
            if sr.shape[0] > Calculator.TRADING_DAYS_PER_YEAR * 5:
                recent_y5_ret  = sr[-1] / sr[- Calculator.TRADING_DAYS_PER_YEAR * 5] - 1
            else:
                recent_y5_ret = sr[-1] / sr[0] - 1
            mdd_part =  sr[:] / sr[:].rolling(window=sr.shape[0], min_periods=1).max()
            mdd = 1 - mdd_part.min()
            mdd_date2 = mdd_part.idxmin()
            mdd_date1 = sr[:mdd_date2].idxmax()
            ret_over_mdd = annualized_ret / mdd
            last_mv_diff = sr[-1] - sr[-2]
            last_increase_rate = (sr[-1] - sr[-2])/ sr[-2]
        # 如果只输入一天，返回空
        else:
            start_date = dates[0]
            end_date = dates[0]
            trade_year = 0
            last_unit_nav = 1
            annualized_ret = 0
            annualized_vol = 0
            sharpe = 0 
            recent_y5_ret = 0
            mdd = 0
            mdd_date1 = dates[0]
            mdd_date2 = dates[0]
            ret_over_mdd = 0
            last_mv_diff = 0
            last_increase_rate = 0

        return SeriesStatUnit(
            start_date=start_date,
            end_date=end_date,
            trade_year=trade_year,
            last_unit_nav=last_unit_nav,
            annualized_ret=annualized_ret,
            annualized_vol=annualized_vol,
            sharpe=sharpe,
            recent_y5_ret=recent_y5_ret,
            mdd=mdd,
            mdd_date1=mdd_date1,
            mdd_date2=mdd_date2,
            ret_over_mdd=ret_over_mdd,
            last_mv_diff=last_mv_diff,
            last_increase_rate=last_increase_rate,
        )

    @staticmethod
    def get_benchmark_stat_result(dates: pandas.core.series.Series,
                                  values: pandas.core.series.Series,
                                  benchmark_values: pandas.core.series.Series):
        
        assert len(dates) == len(values), 'date and port_values has different numbers'
        assert len(dates) == len(benchmark_values), 'date and bench_values has different numbers'
        res = Calculator.get_stat_result(dates, values)
        sr_values  = pandas.Series(values, index=dates).sort_index()  
        sr_values = sr_values / sr_values[0]
        sr_benchmark_values = pandas.Series(benchmark_values, index=dates).sort_index()  
        sr_benchmark_values = sr_benchmark_values / sr_benchmark_values[0]
        sr_values_ret = sr_values / sr_values.shift(1)
        sr_benchmark_ret = sr_benchmark_values / sr_benchmark_values.shift(1)
        x = sr_benchmark_ret.dropna().values
        y = sr_values_ret.dropna().values
        x = sm.add_constant(x)
        model = regression.linear_model.OLS(y,x).fit()
        x = x[:,1]
        alpha = model.params[0]
        beta = model.params[1]
        track_err = (sr_values_ret - sr_benchmark_ret).std(ddof=1) * np.sqrt(Calculator.TRADING_DAYS_PER_YEAR)
        ir = alpha / track_err
        
        return BenchmarkSeiesStatUnit(
            start_date=res.start_date,
            end_date=res.end_date,
            trade_year=res.trade_year,
            last_unit_nav=res.last_unit_nav,
            annualized_ret=res.annualized_ret,
            annualized_vol=res.annualized_vol,
            sharpe=res.sharpe,
            recent_y5_ret=res.recent_y5_ret,
            mdd=res.mdd,
            mdd_date1=res.mdd_date1,
            mdd_date2=res.mdd_date2,
            ret_over_mdd=res.ret_over_mdd,
            alpha=alpha,
            beta=beta,
            track_err=track_err,
            ir=ir,
            last_mv_diff=res.last_mv_diff,
            last_increase_rate=res.last_increase_rate,
        )

    @staticmethod
    def get_benchmark(index_price: pandas.DataFrame,
                        weight_list: list,
                        index_list: list,
                        begin_date: datetime.date,
                        end_date: datetime.date)->pandas.DataFrame:

        assert len(weight_list) == len(index_list), 'weight_list and index_list has different numbers'
        assert index_price.shape[1] == len(weight_list), 'columns in index_price are not equal to index list'
        assert begin_date <= end_date, 'end date must bigger than begin date'
        if len(weight_list) < 1:
            return pandas.DataFrame()
        index_price = index_price.loc[begin_date:end_date,].fillna(method='bfill').fillna(method='ffill')
        index_price = index_price / index_price.iloc[0]
        weight_dict = [{'index_id':index_id, 'weight':weight_i } for index_id, weight_i in zip(index_list, weight_list)]
        weight_df = pandas.DataFrame(weight_dict)
        weight_df['weight'] = weight_df['weight'] / weight_df.weight.sum()
        weight_df = weight_df.set_index('index_id').T
        index_price['benchmark'] = index_price.mul(weight_df.values).sum(axis=1)
        return index_price[['benchmark']]

    @staticmethod
    def get_turnover_rate(dates: pandas.core.series.Series,
                          values: pandas.core.series.Series,
                          total_amount: float):
        year_num = len(list(set([_.year for _ in dates])))
        return total_amount / gmean(values) / 2 / year_num * 100

    @staticmethod
    def get_stat_result_from_df(df: pandas.DataFrame,
                                date_column: str,
                                value_column: str):
        dates = df[date_column].values
        values = df[value_column].values
        return Calculator.get_stat_result(dates, values)

    @staticmethod
    def get_benchmark_stat_result_from_df(df: pandas.DataFrame,
                                          date_column: str,
                                          port_value_column: str,
                                          bench_value_column: str):
        dates = df[date_column].values
        port_values = df[port_value_column].values
        bench_values = df[bench_value_column].values
        return Calculator.get_benchmark_stat_result(dates, port_values, bench_values)

    @staticmethod
    def get_benchmark_result(index_list:list,
                             weight_list:list,
                             begin_date: datetime.date,
                             end_date: datetime.date) -> pandas.DataFrame:
        '''
        index_list = ['hs300','national_debt']
        weight_list = [0.7,0.3]
        begin_date = datetime.date(2005,1,1)
        end_date = datetime.date(2020,1,1)
        Calculator.get_benchmark_result(index_list, weight_list, begin_date, end_date)
        '''                   
        basic = BasicDataApi()
        index_price = basic.get_index_price(index_list).pivot_table(index='datetime', columns='index_id', values='close')
        return Calculator.get_benchmark(index_price, weight_list, index_list, begin_date, end_date)
    
    @staticmethod
    def get_index_pct_data_df(index_id:str='hs300',
                           index_val:str=None,
                           windows:int=5*242,
                           min_periods:int=3*242,
                           pct_list:list=[0.15, 0.5, 0.6, 0.8]):
        
        assert (index_id in list(TaaTunerParam.PCT_PAIR.keys())) or (index_val is not None), \
            f'neither index_id{index_id} nor index_val {index_val} is valid'

        index_val = index_val if index_val else TaaTunerParam.PCT_PAIR[index_id]
        # load data
        index_val_data = DerivedDataApi().get_index_valuation_develop_without_date(index_ids=[index_id])
        
        values = index_val_data[index_val].values
        dates = index_val_data.datetime.values
        return  Calculator.get_index_pct_data(dates=dates,
                                            values=values,
                                            pct_list=pct_list,
                                            windows=windows,
                                            min_periods=min_periods)

    @staticmethod
    def roll_pct(x, pct_list, res):
        l = sorted(x)
        lens = len(l)
        res.append([l[int(lens*pct_i)] for pct_i in pct_list])
        return 1

    @staticmethod
    def get_index_pct_data(dates:pandas.core.series.Series,
                              values: pandas.core.series.Series,
                              pct_list:list,
                              windows:int,
                              min_periods:int):
        df = pandas.DataFrame(values, index=dates).dropna()
        res = []
        df[0].rolling(window= windows, min_periods=min_periods).apply(partial(Calculator.roll_pct, pct_list=pct_list, res=res), raw=True)
        return pandas.DataFrame(res, index=dates[-len(res):])

    @staticmethod
    def get_taa_detail(index_id:str='hs300',
                       index_val:str='roe_pct',
                       taa_param:TAAParam=TAAParam(),
                       ):
        
        # load data
        _dts = BasicDataApi().get_trading_day_list()
        dts = _dts.datetime 
        index_val_data = DerivedDataApi().get_index_valuation_develop_without_date(index_ids=[index_id])
        index_val_data = index_val_data.set_index('datetime').reindex(dts).fillna(method='ffill')
        asset_func_index = 'hs300'
        index_val_data['index_id'] = asset_func_index
        index_val_data = index_val_data.reset_index().set_index(['datetime','index_id'])
        fake_weight = AssetWeight(**{asset_func_index:1})
        taa_helper = TAAHelper(taa_params=taa_param)
        for dt in dts:
            asset_pct = index_val_data.loc[dt]
            taa_helper.on_price(dt=dt, asset_price=None, cur_saa=fake_weight, asset_pct=asset_pct, select_val={asset_func_index:index_val})
        df = pandas.DataFrame(taa_helper.tactic_history).T.dropna()
        df['last_date'] = df.index.to_series().shift(1)
        con = df[asset_func_index] != df[asset_func_index].shift(1)
        df_diff_part = df[con].copy()
        df_diff_part = df_diff_part.reset_index().rename(columns={'index':'begin_date'})
        next_date = df_diff_part['last_date'].shift(-1).tolist()
        next_date[-1] = df.index.values[-1]
        df_diff_part['end_date'] = next_date
        df_result = df_diff_part[df_diff_part[asset_func_index] != TAAStatusMode.NORMAL][['begin_date','end_date',asset_func_index]]
        df_result = df_result.rename(columns = {asset_func_index:'status'})
        return df_result.to_dict('records') 


if __name__ == "__main__":
    # get pct with select rank
    Calculator.get_index_pct_data_df()
    Calculator.get_index_pct_data_df(index_id='hs300',
                           index_val='roe',
                           windows=5*242,
                           min_periods=3*242,
                           pct_list=[0.15, 0.5, 0.6, 0.8])

    # get taa detail
    Calculator.get_taa_detail()
    Calculator.get_taa_detail(index_id='hs300',
                              index_val='pb_pct',
                              taa_param=TAAParam(),
                              )