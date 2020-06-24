# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

# 通联数据机密
# --------------------------------------------------------------------
# 通联数据股份公司版权所有 © 2013-2019
#
# 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
# 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
# 版权法保护。
# 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
# DataYes CONFIDENTIAL
# --------------------------------------------------------------------
# Copyright © 2013-2019 DataYes, All Rights Reserved.
#
# NOTICE: All information contained herein is the property of DataYes
# Incorporated. The intellectual and technical concepts contained herein are
# proprietary to DataYes Incorporated, and may be covered by China, U.S. and
# Other Countries Patents, patents in process, and are protected by trade
# secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from DataYes.

__all__ = ['ideal', 'long_only', 'long_short', 'limit_active_risk', 'limit_portfolio_risk']

import pandas as pd

from .SignalAnalysis.tears import portfolio_construction


_OPTIMIZER_RETURN_FIELDS = [
    'trade_volume',
    'trade_value',
    'expected_volume',
    'expected_active_weight',
    'expected_weight',
    'expected_holding',
    'opt_status',
]
_SIMPLE_RETURN_FIELDS = [
    'expected_weight',
]


def print_validate_factor_frame(factor_frame):
    is_all_null = factor_frame.isnull().all().all()
    if is_all_null:
        print("因子数据异常，请校验")
    return not is_all_null


def ideal(
        factor_frame, start_date, end_date, freq, universe='HS300', benchmark='HS300',
        init_cash=1e8, init_holding=None
):
    """
    :param factor_frame: 因子数据, DataFrame(factor_values, index=dates, columns=tickers)
    :param start_date: str, 'YYYYmmdd'
    :param end_date: str, 'YYYYmmdd'
    :param freq: str, 调仓频率，'day/week/month/quarter/semi-year'
    :param universe: str or dict of list, 股票池。默认是HS300，目前支持HS300/ZZ500/ZZ700/ZZ800/TLQA,
            也可为dict of list，则为自定义universe
    :param benchmark: str or dict of Series, 基准名称， 默认是HS300。取值为指数名称，如HS300（计算active return）,
                                    或者None（计算market return）/risk_free（计算excess return）
            也可为dict of Series，则为自定义benchmark
    :param init_cash: int/float, 初始资金，默认1e8
    :param init_holding: dict/pd.Series/None, 每个个股的初始市值，不包含现金
    :return: dict
    """
    if not print_validate_factor_frame(factor_frame):
        return
    # 宽格式转换为长格式
    factor_value_frame = factor_frame.copy()
    factor_value_frame.index.name = 'date'
    factor_value_frame.reset_index(inplace=True)
    factor_value_frame = pd.melt(factor_value_frame, id_vars=['date'], var_name='ticker', value_name='value')

    result = portfolio_construction(
        factor_value_frame=factor_value_frame,
        construct_method='ideal',
        start_date=start_date,
        end_date=end_date,
        frequency=freq,
        universe=universe,
        benchmark=benchmark,
        init_cash=init_cash,
        simulate=True,
        init_holding=init_holding
    )
    if result:
        result = {
            "-".join([td[:4], td[4:6], td[6:8]]): {f: result['trades'][td].get(f) for f in _OPTIMIZER_RETURN_FIELDS}
            for td in result['trades']
        }
    return result


def long_only(
        factor_frame, start_date, end_date, freq, universe='HS300', benchmark='HS300',
        top_ratio=0.2, select_type=1, weight_type='equal', init_cash=1e8, init_holding=None,
):
    """
    :param factor_frame: 因子数据, DataFrame(factor_values, index=dates, columns=tickers)
    :param start_date: str, 'YYYYmmdd'
    :param end_date: str, 'YYYYmmdd'
    :param freq: str, 调仓频率，'day/week/month/quarter/semi-year'
    :param universe: str or dict, 股票池。默认是HS300，目前支持HS300/ZZ500/ZZ700/ZZ800/TLQA,
            也可为dict of list，则为自定义universe
    :param benchmark: str, 基准名称， 默认是HS300。取值为指数名称，如HS300（计算active return）,
                                    或者None（计算market return）/risk_free（计算excess return）
            也可为dict of Series，则为自定义benchmark
    :param top_ratio: float/list 做多前多少百分比或者前百分比区间的股票，默认0.2
    :param select_type: int，组合构建的行业配比方式，默认为1。可选0/1 WHOLE_INDUSTRY = 0 EACH_INDUSTRY = 1
    :param weight_type: str, 权重配比方式，取值范围equal/risk/cap，对应为等权/风险权重/流通市值权重，默认equal
    :param init_cash: int/float, 初始资金，默认1e8
    :param init_holding: dict/pd.Series/None, 每个个股的初始市值，不包含现金
    :return: dict
    """
    if not print_validate_factor_frame(factor_frame):
        return
    # 宽格式转换为长格式
    factor_value_frame = factor_frame.copy()
    factor_value_frame.index.name = 'date'
    factor_value_frame.reset_index(inplace=True)
    factor_value_frame = pd.melt(factor_value_frame, id_vars=['date'], var_name='ticker', value_name='value')

    result = portfolio_construction(
        factor_value_frame=factor_value_frame,
        construct_method='simple_long_only',
        start_date=start_date,
        end_date=end_date,
        frequency=freq,
        universe=universe,
        benchmark=benchmark,
        top_ratio=top_ratio,
        select_type=select_type,
        weight_type=weight_type,
        init_cash=init_cash,
        init_holding=init_holding,
        simulate=True
    )
    if result:
        result = {
            "-".join([td[:4], td[4:6], td[6:8]]): {f: result['trades'][td].get(f) for f in _OPTIMIZER_RETURN_FIELDS}
            for td in result['trades']
        }
    return result


def long_short(
        factor_frame, start_date, end_date, freq, universe='HS300', benchmark='HS300',
        top_ratio=0.2, down_ratio=0.2, select_type=1, weight_type='equal', init_cash=1e8, init_holding=None,
):
    """
    :param factor_frame: 因子数据, DataFrame(factor_values, index=dates, columns=tickers)
    :param start_date: str, 'YYYYmmdd'
    :param end_date: str, 'YYYYmmdd'
    :param freq: str, 调仓频率，'day/week/month/quarter/semi-year'
    :param universe: str or dict, 股票池。默认是HS300，目前支持HS300/ZZ500/ZZ700/ZZ800/TLQA,
            也可为dict of list，则为自定义universe
    :param benchmark: str, 基准名称， 默认是HS300。取值为指数名称，如HS300（计算active return）,
                                    或者None（计算market return）/risk_free（计算excess return）
            也可为dict of Series，则为自定义benchmark
    :param top_ratio: float/list 做多前多少百分比或者前百分比区间的股票，默认0.2
    :param down_ratio: float 做空后多少百分比的股票，默认0.2
    :param select_type: int，组合构建的行业配比方式，默认为1。可选0/1 WHOLE_INDUSTRY = 0 EACH_INDUSTRY = 1
    :param weight_type: str, 权重配比方式，取值范围equal/risk/cap，对应为等权/风险权重/流通市值权重，默认equal
    :param init_cash: int/float, 初始资金，默认1e8
    :param init_holding: dict/pd.Series/None, 每个个股的初始市值，不包含现金
    :return: dict
    """
    if not print_validate_factor_frame(factor_frame):
        return
    # 宽格式转换为长格式
    factor_value_frame = factor_frame.copy()
    factor_value_frame.index.name = 'date'
    factor_value_frame.reset_index(inplace=True)
    factor_value_frame = pd.melt(factor_value_frame, id_vars=['date'], var_name='ticker', value_name='value')

    result = portfolio_construction(
        factor_value_frame=factor_value_frame,
        construct_method='simple_long_short',
        start_date=start_date,
        end_date=end_date,
        frequency=freq,
        universe=universe,
        benchmark=benchmark,
        top_ratio=top_ratio,
        down_ratio=down_ratio,
        select_type=select_type,
        weight_type=weight_type,
        init_cash=init_cash,
        init_holding=init_holding,
    )
    if result:
        result = {
            "-".join([td[:4], td[4:6], td[6:8]]): {f: result[td].get(f) for f in _OPTIMIZER_RETURN_FIELDS}
            for td in result
        }
    return result


def limit_active_risk(
        factor_frame, start_date, end_date, freq, universe='HS300', benchmark='HS300', price_type='open',
        target_risk=0.3, target_turnover=None, fee=0, init_cash=1e8, init_holding=None,
        asset_lower_boundary=0, asset_upper_boundary=1,
        factor_exposure_lower_boundary=0, factor_exposure_upper_boundary=0,
        sector_exposure_lower_boundary=0, sector_exposure_upper_boundary=0,
):
    """
    :param factor_frame:
    :param start_date: str, 'YYYYmmdd'
    :param end_date: str, 'YYYYmmdd'
    :param freq: str, 调仓频率，'day/week/month/quarter/semi-year'
    :param universe: str or dict, 股票池。默认是HS300，目前支持HS300/ZZ500/ZZ700/ZZ800/TLQA,
            也可为dict of list，则为自定义universe
    :param benchmark: str, 基准名称， 默认是HS300。取值为指数名称，如HS300（计算active return）,
                                    或者None（计算market return）/risk_free（计算excess return）
            也可为dict of Series，则为自定义benchmark
    :param price_type: str, 估值价格，取值范围open/close,默认open.
            open 为使用开盘价进行组合估值，close 为使用收盘价进行组合估值。
    :param target_risk: float, 默认值0.3
    :param target_turnover: float/int/None, 目标换手率约束，默认值为None
    :param fee: float/int, 交易费用线性系数
    :param init_cash: int/float, 初始资金，默认1e8
    :param init_holding: dict/pd.Series/None, 每个个股的初始市值，不包含现金
    :param asset_lower_boundary: float/Series，个股仓位下限，默认为0
    :param asset_upper_boundary: float/Series，个股仓位上限，默认为1
    :param factor_exposure_lower_boundary: float/Series，风格因子暴露下限，默认为0
    :param factor_exposure_upper_boundary: float/Series，风格因子暴露上限，默认为0
    :param sector_exposure_lower_boundary: float/Series，行业因子暴露下限，默认为0
    :param sector_exposure_upper_boundary: float/Series，行业因子暴露上限，默认为0
    :return: dict
    """
    if not print_validate_factor_frame(factor_frame):
        return
    # 宽格式转换为长格式
    factor_value_frame = factor_frame.copy()
    factor_value_frame.index.name = 'date'
    factor_value_frame.reset_index(inplace=True)
    factor_value_frame = pd.melt(factor_value_frame, id_vars=['date'], var_name='ticker', value_name='value')

    result = portfolio_construction(
        factor_value_frame=factor_value_frame,
        construct_method='limit_active_risk',
        start_date=start_date,
        end_date=end_date,
        frequency=freq,
        universe=universe,
        benchmark=benchmark,
        price_type=price_type,
        target_risk=target_risk,
        target_turnover=target_turnover,
        fee=fee,
        init_cash=init_cash,
        init_holding=init_holding,
        asset_lower_boundary=asset_lower_boundary,
        asset_upper_boundary=asset_upper_boundary,
        factor_exposure_lower_boundary=factor_exposure_lower_boundary,
        factor_exposure_upper_boundary=factor_exposure_upper_boundary,
        sector_exposure_lower_boundary=sector_exposure_lower_boundary,
        sector_exposure_upper_boundary=sector_exposure_upper_boundary,
    )
    if result:
        result = {
            "-".join([td[:4], td[4:6], td[6:8]]): {f: result[td].get(f) for f in _OPTIMIZER_RETURN_FIELDS}
            for td in result
        }
    return result


def limit_portfolio_risk(
        factor_frame, start_date, end_date, freq, universe='HS300', benchmark='HS300', price_type='open',
        target_risk=0.3, target_turnover=None, fee=0, init_cash=1e8, init_holding=None,
        asset_lower_boundary=0, asset_upper_boundary=1,
        factor_exposure_lower_boundary=0, factor_exposure_upper_boundary=0,
        sector_exposure_lower_boundary=0, sector_exposure_upper_boundary=0,
):
    """
    :param factor_frame:
    :param start_date: str, 'YYYYmmdd'
    :param end_date: str, 'YYYYmmdd'
    :param freq: str, 调仓频率，'day/week/month/quarter/semi-year'
    :param universe: str or dict, 股票池。默认是HS300，目前支持HS300/ZZ500/ZZ700/ZZ800/TLQA,
            也可为dict of list，则为自定义universe
    :param benchmark: str, 基准名称， 默认是HS300。取值为指数名称，如HS300（计算active return）,
            或者None（计算market return）/risk_free（计算excess return）
            也可为dict of Series，则为自定义benchmark
    :param price_type: str, 估值价格，取值范围open/close,默认open.
            open 为使用开盘价进行组合估值，close 为使用收盘价进行组合估值。
    :param target_risk: float, 默认值0.3
    :param target_turnover: float/int/None, 目标换手率约束，默认值为None
    :param fee: float/int, 交易费用线性系数
    :param init_cash: int/float, 初始资金，默认1e8
    :param init_holding: dict/pd.Series/None, 每个个股的初始市值，不包含现金
    :param asset_lower_boundary: float/Series，个股仓位下限，默认为0
    :param asset_upper_boundary: float/Series，个股仓位上限，默认为1
    :param factor_exposure_lower_boundary: float/Series，风格因子暴露下限，默认为0
    :param factor_exposure_upper_boundary: float/Series，风格因子暴露上限，默认为0
    :param sector_exposure_lower_boundary: float/Series，行业因子暴露下限，默认为0
    :param sector_exposure_upper_boundary: float/Series，行业因子暴露上限，默认为0
    :return: dict
    """
    if not print_validate_factor_frame(factor_frame):
        return
    # 宽格式转换为长格式
    factor_value_frame = factor_frame.copy()
    factor_value_frame.index.name = 'date'
    factor_value_frame.reset_index(inplace=True)
    factor_value_frame = pd.melt(factor_value_frame, id_vars=['date'], var_name='ticker', value_name='value')

    result = portfolio_construction(
        factor_value_frame=factor_value_frame,
        construct_method='limit_portfolio_risk',
        start_date=start_date,
        end_date=end_date,
        frequency=freq,
        universe=universe,
        benchmark=benchmark,
        price_type=price_type,
        target_risk=target_risk,
        target_turnover=target_turnover,
        fee=fee,
        init_cash=init_cash,
        init_holding=init_holding,
        asset_lower_boundary=asset_lower_boundary,
        asset_upper_boundary=asset_upper_boundary,
        factor_exposure_lower_boundary=factor_exposure_lower_boundary,
        factor_exposure_upper_boundary=factor_exposure_upper_boundary,
        sector_exposure_lower_boundary=sector_exposure_lower_boundary,
        sector_exposure_upper_boundary=sector_exposure_upper_boundary,
    )
    if result:
        result = {
            "-".join([td[:4], td[4:6], td[6:8]]): {f: result[td].get(f) for f in _OPTIMIZER_RETURN_FIELDS}
            for td in result
        }
    return result
