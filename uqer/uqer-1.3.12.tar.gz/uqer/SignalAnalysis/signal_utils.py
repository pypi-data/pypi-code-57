# -*- coding: UTF-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

__author__ = 'xinhua.sun'


REFRESH_RATE_LIST = ['fri', 'month']
REFRESH_RATE_MAP = {}


def _validate_field(field, valid_fields):
    return field in valid_fields


def print_validate_frequency(freq):
    validation_result = _validate_field(
        freq, ['day', 'week', 'month', 'quarter', 'semi-year'])
    if not validation_result:
        print("frequency参数：%s暂不支持，支持范围：[day/week/month/quarter/semi-year]" % freq)
    return validation_result


def print_validate_universe(univ):
    validation_result = _validate_field(
        univ, ['HS300', 'ZZ500', 'TLQA', 'ZZ700', 'ZZ800'])
    custom_universe = isinstance(univ, dict)
    validation_result = validation_result or custom_universe
    if not validation_result:
        print('''universe参数：%s暂不支持，支持范围：[HS300/ZZ500/ZZ700/ZZ800/
        TLQA]或者自定义universe''' % univ)
    return validation_result


def print_validate_benchmark(benchmark):
    validation_result = benchmark is None or _validate_field(
        benchmark, ['HS300', 'ZZ500', 'TLQA', 'ZZ700', 'ZZ800', 'risk_free'])
    custom_benchmark = isinstance(benchmark, dict)
    validation_result = validation_result or custom_benchmark
    if not validation_result:
        print('''benchmark参数：%s暂不支持，支持范围：None值或者[HS300/ZZ500/
        ZZ700/ZZ800/TLQA/risk_free]或者自定义benchmark''' % benchmark)
    return validation_result


def print_validate_weight_type(weight_type):
    validation_result = _validate_field(weight_type, ['equal', 'cap', 'risk'])
    if not validation_result:
        print("weight_type参数：%s暂不支持，支持范围：equal/cap/risk" % weight_type)
    return validation_result


def print_validate_select_type(select_type):
    validation_result = _validate_field(select_type, [0, 1])
    if not validation_result:
        print("select_type参数：%s暂不支持，支持范围：0/1" % select_type)
    return validation_result


def print_validate_construct_method(construct_method):
    validation_result = _validate_field(construct_method,
                                        ['simple_long_only',
                                         'simple_long_short',
                                         'ideal', 'limit_active_risk',
                                         'limit_portfolio_risk',
                                         'max_sharpe_ratio'])
    if not validation_result:
        print('''select_type参数：%s暂不支持，支持范围：simple_long_only/
        simple_long_short/ideal/limit_active_risk/limit_portfolio_risk/
        max_sharpe_ratio''' % construct_method)
    return validation_result