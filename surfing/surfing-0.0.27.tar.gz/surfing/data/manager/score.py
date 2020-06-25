from ..struct import FundScoreParam, ScoreFilter, ScorePenaltyParams
from .data_tables import FundDataTables
import dataclasses
import pandas as pd 
import re
import math

@dataclasses.dataclass
class ScoreFunc:

    alpha: float=0 # weight of alpha
    beta: float=0  # weight of abs(1-beta), or beta's deviation from 1
    track_err: float=0 # weight of track_err
    fee_rate: float=0 # weight of fee_rate
    ir: float=0 # weight of ir

    def get(self, data):
        return self.alpha * data.alpha + self.beta * abs(1-data.beta) + self.track_err * data.track_err + self.fee_rate * data.fee_rate + self.ir * data.ir


class FundScoreManager:

    def __init__(self, score_filter=ScoreFilter(), score_penalty_param=ScorePenaltyParams()):
        self.params = None
        self.dts = None
        self.funcs = {
            'hs300': ScoreFunc(alpha=0.3, beta=-0.6, fee_rate=-0.1),
            'csi500': ScoreFunc(alpha=0.8, beta=-0.2),
            'gem': ScoreFunc(alpha=0.2, beta=-0.4, track_err=-0.4),

            'national_debt': ScoreFunc(alpha=0.3, beta=-0.25, track_err=-0.45),#ScoreFunc(alpha=0.6, fee_rate=-0.2, track_err=-0.2),
            'mmf':ScoreFunc(alpha=0.6, fee_rate=-0.3, track_err=-0.1),
            'credit_debt': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.8),

            'sp500rmb': ScoreFunc(fee_rate=-0.2, track_err=-0.8),
            'dax30rmb': ScoreFunc(fee_rate=-0.2, track_err=-0.8),
            'n225rmb': ScoreFunc(fee_rate=-0.2, track_err=-0.8),

            'gold': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.8),
            'oil': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.8),
            'real_state': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.8),

        }
        self.score_cache = None
        self.score_raw_cache = None
        self.score_filter = score_filter
        self.score_penalty_param = score_penalty_param

    def set_param(self, score_param: FundScoreParam):
        self.params = score_param

    def set_dts(self, dts: FundDataTables):
        self.dts = dts
        self.fund_id_to_name = self.dts.fund_info[['fund_id','desc_name']].set_index('fund_id').to_dict()['desc_name']
        self.fund_name_to_id = self.dts.fund_info[['fund_id','desc_name']].set_index('desc_name').to_dict()['fund_id']

    def get_fund_score(self, dt, index_id, is_filter_c) -> dict:
        assert self.params and self.dts, 'cannot provide fund_score without params or data tables'
        score, score_raw = self._get_score(index_id, dt, is_filter_c)
        return score, score_raw

    def get_fund_scores(self, dt, index_list, is_filter_c=True) -> dict:
        if not self.score_cache:
            score = {}
            score_raw = {}
            for index_id in index_list:
                score[index_id], score_raw[index_id] = self.get_fund_score(dt, index_id, is_filter_c)
            return score, score_raw
        return self.score_cache.get(dt, {}), self.score_raw_cache.get(dt, {})

    def pre_calculate(self, is_filter_c=True) -> dict:
        self.score_cache = {}
        self.score_raw_cache = {}
        pad = self.dts.fund_indicator.pivot_table(index=['datetime', 'index_id'])
        for dt, index_id in pad.index:
            if not dt in self.score_cache:
                self.score_cache[dt] = {}
                self.score_raw_cache[dt] = {}
            score, score_raw = self._get_score(index_id, dt, is_filter_c)
            self.score_cache[dt][index_id] = score
            self.score_raw_cache[dt][index_id] = score_raw

    def _get_score(self, index_id, dt, is_filter_c):
        cur_d = self.dts.index_fund_indicator_pack.loc[index_id, dt]
        fund_id_list = cur_d.index.tolist()
        # filter with fund size and company hold rate
        fund_id_list_new = self._filter_size_and_com_hold(dt, fund_id_list, index_id)
        if  bool(set(fund_id_list) & set(fund_id_list_new)):
            cur_d = cur_d.reindex(fund_id_list_new).dropna()
        if cur_d.shape[0] > 1:
            cur_d_sta = cur_d.apply(lambda x: (x - x.mean() + 1e-6)/ (x.std() + 1e-6), axis=0)
        else:
            cur_d_sta = cur_d
        cur_d_sta['beta'] = cur_d['beta']
        cur_d_sta['year_length'] = cur_d['year_length']
        func = self.funcs.get(index_id)
        score_raw = cur_d_sta.apply(lambda x: func.get(x), axis=1)
        if index_id in self.score_penalty_param.FilterYearIndex:
            punish_funds = cur_d_sta[cur_d_sta.year_length < self.score_penalty_param.JudgeYearLength].index.tolist()
            for _fund_id in punish_funds:
                score_raw[_fund_id] += self.score_penalty_param.Penalty
        score = (score_raw - score_raw.min()) / (score_raw.max() - score_raw.min())
        if score.shape[0] == 1:
            score.values[0] = 1
        score = { fund_id: s for fund_id, s in score.iteritems() }
        score_raw = { fund_id: s for fund_id, s in score_raw.iteritems() }
        if is_filter_c:
            score = self._filter_score(score)
            score_raw = self._filter_score(score_raw)
        return score, score_raw

    def _filter_size_and_com_hold(self, dt, fund_id_list, index_id):
        if index_id not in self.score_filter.FilterIndexId:
            return fund_id_list
        if dt not in self.dts.fund_com_hold.index:
            return fund_id_list
        fund_com_hold_dt = self.dts.fund_com_hold.loc[dt]
        fund_size_dt = self.dts.fund_size.loc[dt]
        fund_com_hold_dt.name = 'com_hold'
        fund_size_dt.name = 'scale'
        fund_filter = pd.DataFrame([fund_com_hold_dt,fund_size_dt]).T.dropna()
        if fund_filter.empty:
            return fund_id_list
        else:
            fund_id_list = fund_filter[(fund_filter.com_hold <= self.score_filter.CompanyHoldLimit)
                        &(fund_filter.scale >= self.score_filter.SizeBottom)
                        &(fund_filter.scale <= self.score_filter.SizeTop)].index.tolist()
            assert len(fund_id_list) > 0, f'{dt} {index_id} no fund to select'
            return fund_id_list

    def _filter_score(self, score_index):
        # 同一天同资产 同基金A B 在 选B
        # 同一天同资产 同基金A C 在 选C
        check_char_list = ['B','C']
        for check_char in check_char_list:
            index_fund_name = [self.fund_id_to_name[_] for _ in list(score_index.keys())]
            c_list = [word for word in index_fund_name if check_char in word]
            # 如果d日, index_id资产下含有C类基金（包含假C类 如名字含有MSCI）
            if len(c_list) > 0:
                for c_fund in c_list:
                    # 替换基金名字里最后一个C 变为A， 这样可以处理假C类基金
                    a_fund = re.sub(f'{check_char}$', 'A', c_fund)
                    # 如果A类有评分， 赋值0
                    if a_fund in index_fund_name:
                        a_fund_id = self.fund_name_to_id[a_fund]
                        score_index[a_fund_id] = 0
        return score_index

    @staticmethod
    def test_func(func_str):
        for item in ScoreFunc.__dataclass_fields__.keys():
            locals()[item] = 0
        # if we cannot calculate, it just breaks
        eval(func_str)
        return True

    @staticmethod
    def get_func(func_str):
        new_func = func_str
        for item in ScoreFunc.__dataclass_fields__.keys():
            new_func = new_func.replace(item, 'x.' + item)
        return lambda x: eval(new_func)

    @staticmethod
    def score_calc(func_str, dm, index_id, dt):
        cur_d = dm.dts.index_fund_indicator_pack.loc[index_id, dt]
        f = FundScoreManager.get_func(func_str)
        return cur_d.apply(f, axis=1)