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
import time
import json
import logging

import pandas as pd

from uqer.config import BRAIN_HOST
from .signal_utils import *
from uqer.uqer import session


def _get_task_result(url, api, post_data):
    res = session.post('%s/%s' % (url, api), json=post_data)
    task_id = json.loads(res.content)['data']
    while True:
        status_res = session.get('%s/status/%s' % (url, task_id))
        format_res = json.loads(status_res.content)
        status = format_res['state']
        if status == 'FINISH':
            break
        time.sleep(3)
    return format_res['task_result']


# 不带回测的construction
def portfolio_construction(factor_value_frame, construct_method, start_date, end_date, frequency, construct_type='end',
                           simulate=False, universe='HS300', benchmark='HS300', top_ratio=0.2, down_ratio=0.2,
                           select_type=1, weight_type='equal', is_factor_constrained=True, target_risk=0.3,
                           target_turnover=None, fee=0, init_cash=1e8, init_holding=None, asset_lower_boundary=0,
                           asset_upper_boundary=1, asset_cons_method='absolute', asset_cons_type='by_value',
                           asset_group_lower_boundary={}, asset_group_upper_boundary={},
                           factor_exposure_lower_boundary=0, factor_exposure_upper_boundary=0,
                           sector_exposure_lower_boundary=0, sector_exposure_upper_boundary=0, **kwargs):
    """
    :param factor_value_frame:DataFrame of factor value，因子数据，
                    需包含三列: date(str), ticker(str), value(float)
    :param construct_method: 组合构建方式，
            'simple_long_only/simple_long_short/ideal/limit_active_risk/limit_portfolio_risk'
    :param start_date: str, 'YYYYmmdd'
    :param end_date: str, 'YYYYmmdd'
    :param frequency: str, 调仓频率，'day/week/month/quarter/semi-year'
    :param construct_type: str, 'start/end', 期初调仓还是期末调仓
    :param simulate: boolean, 是否回测
    :param universe: str or dict, 股票池。默认是HS300，目前支持HS300/ZZ500/ZZ700/ZZ800/TLQA,
            也可为dict of list，则为自定义universe
    :param benchmark: str, 基准名称， 默认是HS300。取值为指数名称，如HS300（计算active return）,
                                    或者None（计算market return）/risk_free（计算excess return）
            也可为dict of Series，则为自定义benchmark
    :param top_ratio: float/list 做多前多少百分比或者前百分比区间的股票，默认0.2
    :param down_ratio: float 做空后多少百分比的股票，默认0.2
    :param select_type: int，组合构建的行业配比方式，默认为1。可选0/1 WHOLE_INDUSTRY = 0 EACH_INDUSTRY = 1
    :param weight_type: str, 权重配比方式，取值范围equal/risk/cap，对应为等权/风险权重/流通市值权重，默认equal
    :param is_factor_constrained: ideal构建参数，是否对行业风格因子中性
    :param target_risk: float, 默认值0.3
    :param target_turnover: float/int/None, 目标换手率约束，默认值为None
    :param fee: float/int, 交易费用线性系数
    :param init_cash: int/float, 初始资金，默认1e8
    :param init_holding: dict/pd.Series/None, 每个个股的初始市值，不包含现金
    :param asset_lower_boundary: float/Series，个股仓位下限，默认为0
    :param asset_upper_boundary: float/Series，个股仓位上限，默认为1
    :param asset_cons_method: 资产权重上下界约束方法，'absolute'：绝对权重约束；'active'：主动权重约束
    :param asset_cons_type: 资产主动权重约束类型，'by_value'：具体值主动约束；'by_percent'：百分比主动约束
    :param factor_exposure_lower_boundary: float/Series，风格因子暴露下限，默认为0
    :param factor_exposure_upper_boundary: float/Series，风格因子暴露上限，默认为0
    :param sector_exposure_lower_boundary: float/Series，行业因子暴露下限，默认为0
    :param sector_exposure_upper_boundary: float/Series，行业因子暴露上限，默认为0
    :param asset_group_lower_boundary: 分组资产权重总和约束下界, dict, key为调仓日期，value为list of Series
    :param asset_group_upper_boundary: 分组资产权重总和约束上界, dict, key为调仓日期，value为list of Series
    :return: dict
    """
    if end_date < start_date:
        print("end_date应当大于start_date,请校验后重新输入")
        return
    if not (print_validate_frequency(frequency)
            and print_validate_benchmark(benchmark)
            and print_validate_weight_type(weight_type)
            and print_validate_select_type(select_type)
            and print_validate_construct_method(construct_method)):
        return
    if type(universe) in (type(u''), type(b'')):
        if not print_validate_universe(universe):
            return
    elif not isinstance(universe, dict):
        print("universe类型输入有误,请校验后重新输入")
        return

    alpha_signals = factor_value_frame.to_json()
    asset_lower_boundary = asset_lower_boundary.to_json() \
        if isinstance(asset_lower_boundary,
                      pd.Series) else asset_lower_boundary
    asset_upper_boundary = asset_upper_boundary.to_json() \
        if isinstance(asset_upper_boundary,
                      pd.Series) else asset_upper_boundary
    factor_exposure_lower_boundary = factor_exposure_lower_boundary.to_json() \
        if isinstance(factor_exposure_lower_boundary, pd.Series) \
        else factor_exposure_lower_boundary
    factor_exposure_upper_boundary = factor_exposure_upper_boundary.to_json() \
        if isinstance(factor_exposure_upper_boundary, pd.Series) \
        else factor_exposure_upper_boundary
    sector_exposure_lower_boundary = sector_exposure_lower_boundary.to_json() \
        if isinstance(sector_exposure_lower_boundary, pd.Series) \
        else sector_exposure_lower_boundary
    sector_exposure_upper_boundary = sector_exposure_upper_boundary.to_json() \
        if isinstance(sector_exposure_upper_boundary, pd.Series) \
        else sector_exposure_upper_boundary
    if init_holding is not None:
        init_holding = init_holding.to_dict() if isinstance(
            init_holding, pd.Series) else init_holding
    asset_group_lower_boundary_list_dict = {k: [g.to_json() for g in v]
                                            for k, v in asset_group_lower_boundary.items()}
    asset_group_upper_boundary_list_dict = {k: [g.to_json() for g in v]
                                            for k, v in asset_group_upper_boundary.items()}
    price_type = kwargs.get('price_type', 'open')
    risk_model_type = kwargs.get('risk_model_type', None)
    opt_params = kwargs.get('opt_params', dict())

    if isinstance(benchmark, dict):
        try:
            benchmark = {td: v.to_dict() for td, v in benchmark.items()}
        except:
            print('自定义benchmark格式有问题，请检查')
            return

    construct_data = {
        "a_signal": alpha_signals,
        "construct_method": construct_method,
        "start_date": start_date, "simulate": simulate,
        "construct_type": construct_type,
        "end_date": end_date, "frequency": frequency,
        "universe": universe, "benchmark": benchmark,
        "top_ratio": top_ratio, "down_ratio": down_ratio,
        "init_cash": init_cash, "init_holding": init_holding,
        "select_type": select_type, "weight_type": weight_type,
        "target_risk": target_risk,
        "is_factor_constrained": is_factor_constrained,
        "target_turnover": target_turnover, "fee": fee,
        "asset_lower_boundary": asset_lower_boundary,
        "asset_upper_boundary": asset_upper_boundary,
        "asset_cons_method": asset_cons_method,
        "asset_cons_type": asset_cons_type,
        "factor_exposure_lower_boundary": factor_exposure_lower_boundary,
        "factor_exposure_upper_boundary": factor_exposure_upper_boundary,
        "sector_exposure_lower_boundary": sector_exposure_lower_boundary,
        "sector_exposure_upper_boundary": sector_exposure_upper_boundary,
        "risk_model_type": risk_model_type,
        "price_type": price_type,
        "asset_group_lower_boundary_list_dict": asset_group_lower_boundary_list_dict,
        "asset_group_upper_boundary_list_dict": asset_group_upper_boundary_list_dict,
        "opt_params": opt_params,
    }
    try:
        print('正在进行组合构建分析，花费的时长受股票数量和分析区间的影响，请稍等...')
        result = _get_task_result(BRAIN_HOST, "portfolio_construction_async", construct_data)
    except Exception as e:
        logging.exception("error")
        print(str(e))
        print("组合构建引擎出现问题，请稍后再试。")
        return

    if result.get('status'):
        msg = result.get('status').get('msg')
        logging.exception("error")
        print(msg)
        print("组合构建引擎出现问题，请稍后再试。")
        return
    else:
        return result
