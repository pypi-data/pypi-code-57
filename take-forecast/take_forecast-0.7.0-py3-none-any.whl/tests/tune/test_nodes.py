# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.5.0'

import typing as tp
import pytest
import numpy as np
import pandas as pd
from take_forecast.tune.nodes import seasonality_test
from take_forecast.tune.nodes import stationarity_test
from take_forecast.tune.nodes import autocorrelation_test
from take_forecast.tune.nodes import seasonal_autocorrelation_test
from take_forecast.tune.nodes import sarima_test
from take_forecast.tune.nodes import decompose_seasonal
from take_forecast.tune.nodes import transform_to_stationary
from take_forecast.tune.nodes import analyse_autocorrelation
from take_forecast.tune.nodes import analyse_seasonal_autocorrelation
from take_forecast.tune.nodes import split_train_test
from take_forecast.tune.nodes import tune_sarima

HP = tp.Dict[str, int]
TS = pd.Series
DF = pd.DataFrame


@pytest.fixture
def ts():
	np.random.seed(0)
	index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
	data = 100 + 20 * np.random.randn(len(index))
	return pd.Series(data, index, name='ts')


@pytest.fixture
def ts_ramp():
	np.random.seed(0)
	index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
	data = 100 + 80 * np.linspace(0, 1, len(index)) + 20 * np.random.randn(len(index))
	return pd.Series(data, index, name='ts')


@pytest.fixture
def df():
	np.random.seed(0)
	index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
	data = {
		'ts1': 100 + 20 * np.random.randn(len(index)),
		'ts2': 250 + 50 * np.random.randn(len(index))
	}
	return pd.DataFrame(data, index)


@pytest.mark.parametrize('threshold', [-3.51])
@pytest.mark.parametrize('n_diff', [2, 10, 100])
def test__stationarity_test__stationary(ts: TS, threshold: float, n_diff: int):
	d, ts_stationary = stationarity_test(ts, threshold, n_diff)
	assert isinstance(d, int)
	assert isinstance(ts_stationary, pd.Series)
	assert d >= 0
	pd.testing.assert_index_equal(ts.index, ts_stationary.index)


@pytest.mark.parametrize('threshold', [-3.51])
@pytest.mark.parametrize('n_diff', [2, 10, 100])
def test__stationarity_test__trend(ts_ramp: TS, threshold: float, n_diff: int):
	d, ts_stationary = stationarity_test(ts_ramp, threshold, n_diff)
	assert isinstance(d, int)
	assert isinstance(ts_stationary, pd.Series)
	assert d >= 0
	pd.testing.assert_index_equal(ts_ramp.index, ts_stationary.index)


@pytest.mark.parametrize('threshold', [9.21])
@pytest.mark.parametrize('s_start', [3, 4, 5])
@pytest.mark.parametrize('s_stop', [10, 50, 1000])
def test__seasonality_test(ts: TS, threshold: float, s_start: int, s_stop: int):
	is_seasonal, s = seasonality_test(ts, threshold, s_start, s_stop)
	assert isinstance(is_seasonal, bool)
	assert isinstance(s, int)
	assert s >= 0


@pytest.mark.parametrize('s', [0, 7, 30, 120])
def test__autocorrelation_test(ts: TS, s: int):
	p_max, q_max = autocorrelation_test(ts, s)
	assert isinstance(p_max, int)
	assert isinstance(q_max, int)
	assert p_max >= 0
	assert q_max >= 0


@pytest.mark.parametrize('s', [0, 7, 30])
@pytest.mark.parametrize('n_cycles', [2, 3, 10, 50])
def test__seasonal_autocorrelation_test(ts: TS, s: int, n_cycles: int):
	P_max, Q_max = seasonal_autocorrelation_test(ts, s, n_cycles)
	assert isinstance(P_max, int)
	assert isinstance(Q_max, int)
	assert P_max >= 0
	assert Q_max >= 0


@pytest.mark.parametrize('pdq', [(0, 0, 0), (0, 1, 0), (1, 0, 1), (1, 1, 1)])
@pytest.mark.parametrize('sPQ', [None])
def test__sarima_test__non_seasonal(ts: TS, pdq: tp.Tuple[int, int, int], sPQ: tp.Tuple[int, int, int]):
	kwargs = sarima_test(ts, pdq, sPQ)
	assert isinstance(kwargs, dict)
	assert len(kwargs) == 1
	
	assert 'order' in kwargs
	assert isinstance(kwargs['order'], tuple)
	assert len(kwargs['order']) == 3
	assert all(isinstance(k, int) for k in kwargs['order'])
	assert all(k >= 0 for k in kwargs['order'])
	assert kwargs['order'][0] <= pdq[0]
	assert kwargs['order'][1] == pdq[1]
	assert kwargs['order'][2] <= pdq[2]


@pytest.mark.parametrize('pdq', [(0, 0, 0), (0, 1, 0), (1, 0, 1), (1, 1, 1)])
@pytest.mark.parametrize('sPQ', [(7, 0, 0), (7, 1, 1)])
def test__sarima_test__seasonal(ts: TS, pdq: tp.Tuple[int, int, int], sPQ: tp.Tuple[int, int, int]):
	kwargs = sarima_test(ts, pdq, sPQ)
	assert isinstance(kwargs, dict)
	assert len(kwargs) == 2
	
	assert 'order' in kwargs
	assert isinstance(kwargs['order'], tuple)
	assert len(kwargs['order']) == 3
	assert all(isinstance(k, int) for k in kwargs['order'])
	assert all(k >= 0 for k in kwargs['order'])
	assert kwargs['order'][0] <= pdq[0]
	assert kwargs['order'][1] <= pdq[1]
	assert kwargs['order'][2] <= pdq[2]
	
	assert 'seasonal_order' in kwargs
	assert isinstance(kwargs['seasonal_order'], tuple)
	assert len(kwargs['seasonal_order']) == 4
	assert all(isinstance(k, int) for k in kwargs['seasonal_order'])
	assert all(k >= 0 for k in kwargs['seasonal_order'])
	assert kwargs['seasonal_order'][0] <= sPQ[1]
	assert kwargs['seasonal_order'][1] == pdq[1] - kwargs['order'][1]
	assert kwargs['seasonal_order'][2] <= sPQ[2]
	assert kwargs['seasonal_order'][3] == sPQ[0]


@pytest.mark.parametrize('threshold', [9.21])
@pytest.mark.parametrize('s_start', [3, 4, 5])
@pytest.mark.parametrize('s_stop', [10, 50, 1000])
def test__decompose_seasonal(df: DF, threshold: float, s_start: int, s_stop: int):
	df_seasonal, df_not_seasonal, dct_s = decompose_seasonal(df, threshold, s_start, s_stop)
	assert isinstance(df_seasonal, pd.DataFrame)
	assert isinstance(df_not_seasonal, pd.DataFrame)
	assert isinstance(dct_s, dict)
	for name in df.keys():
		assert name in dct_s
		assert name in df_not_seasonal
		if dct_s[name]:
			assert name in df_seasonal
		assert isinstance(dct_s[name], int)
		assert dct_s[name] >= 0
	assert all(k in df for k in dct_s.keys())
	assert all(k in df for k in df_seasonal.keys())
	assert all(k in df for k in df_not_seasonal.keys())


@pytest.mark.parametrize('threshold', [-3.51])
@pytest.mark.parametrize('n_diff', [2, 10, 100])
def test__transform_to_stationary(df: DF, threshold: float, n_diff: int):
	df_stationary, dct_d = transform_to_stationary(df, threshold, n_diff)
	assert isinstance(df_stationary, pd.DataFrame)
	assert isinstance(dct_d, dict)
	for name in df.keys():
		assert name in dct_d
		assert name in df_stationary
		assert isinstance(dct_d[name], int)
		assert dct_d[name] >= 0
	assert all(k in df for k in dct_d.keys())
	assert all(k in df for k in df_stationary.keys())


@pytest.mark.parametrize('dct_s', [{'ts1': 0, 'ts2': 0}, {'ts1': 0, 'ts2': 7}, {'ts1': 7, 'ts2': 7}])
def test__analyse_autocorrelation(df: DF, dct_s: HP):
	dct_p_max, dct_q_max = analyse_autocorrelation(df, dct_s)
	assert isinstance(dct_p_max, dict)
	assert isinstance(dct_q_max, dict)
	for name in df.keys():
		assert name in dct_p_max
		assert name in dct_q_max
		assert isinstance(dct_p_max[name], int)
		assert isinstance(dct_q_max[name], int)
		assert dct_p_max[name] >= 0
		assert dct_q_max[name] >= 0
	assert all(k in df for k in dct_p_max.keys())
	assert all(k in df for k in dct_q_max.keys())


@pytest.mark.parametrize('dct_s', [{'ts1': 0, 'ts2': 0}, {'ts1': 0, 'ts2': 7}, {'ts1': 7, 'ts2': 7}])
@pytest.mark.parametrize('n_cycles', [2, 3, 10, 50])
def test__analyse_seasonal_autocorrelation(df: DF, dct_s: HP, n_cycles: int):
	dct_P_max, dct_Q_max = analyse_seasonal_autocorrelation(df, dct_s, n_cycles)
	assert isinstance(dct_P_max, dict)
	assert isinstance(dct_Q_max, dict)
	for name in df.keys():
		assert name in dct_P_max
		assert name in dct_Q_max
		assert isinstance(dct_P_max[name], int)
		assert isinstance(dct_Q_max[name], int)
		assert dct_P_max[name] >= 0
		assert dct_Q_max[name] >= 0
	assert all(k in df for k in dct_P_max.keys())
	assert all(k in df for k in dct_Q_max.keys())


@pytest.mark.parametrize('r_split', [0.0, 0.2, 0.5, 0.8, 1.0])
def test__split_train_test(df: DF, r_split: int):
	df_train, df_test = split_train_test(df, r_split)
	assert isinstance(df_train, pd.DataFrame)
	assert isinstance(df_test, pd.DataFrame)
	assert len(df_train) == int(r_split * len(df))
	assert len(df_test) == len(df) - len(df_train)
	assert all(k in df_train for k in df.keys())
	assert all(k in df_test for k in df.keys())
	assert all(k in df for k in df_train.keys())
	assert all(k in df for k in df_test.keys())


@pytest.mark.parametrize('dct_s', [{'ts1': 0, 'ts2': 0}])
@pytest.mark.parametrize('dct_d', [{'ts1': 0, 'ts2': 0}, {'ts1': 1, 'ts2': 2}])
@pytest.mark.parametrize('dct_p_max', [{'ts1': 2, 'ts2': 2}])
@pytest.mark.parametrize('dct_q_max', [{'ts1': 2, 'ts2': 2}])
@pytest.mark.parametrize('dct_P_max', [{'ts1': 2, 'ts2': 2}])
@pytest.mark.parametrize('dct_Q_max', [{'ts1': 2, 'ts2': 2}])
def test__tune_sarima__non_seasonal(df: DF, dct_s: HP, dct_d: HP, dct_p_max: HP, dct_q_max: HP, dct_P_max: HP, dct_Q_max: HP):
	dct_kwargs = tune_sarima(df, dct_s, dct_d, dct_p_max, dct_q_max, dct_P_max, dct_Q_max)
	assert isinstance(dct_kwargs, dict)
	for name in df.keys():
		assert name in dct_kwargs
		assert isinstance(dct_kwargs[name], dict)
		assert len(dct_kwargs[name]) == 1
		assert 'order' in dct_kwargs[name]
	assert all(k in df for k in dct_kwargs.keys())


@pytest.mark.parametrize('dct_s', [{'ts1': 7, 'ts2': 7}])
@pytest.mark.parametrize('dct_d', [{'ts1': 0, 'ts2': 0}, {'ts1': 1, 'ts2': 2}])
@pytest.mark.parametrize('dct_p_max', [{'ts1': 2, 'ts2': 2}])
@pytest.mark.parametrize('dct_q_max', [{'ts1': 2, 'ts2': 2}])
@pytest.mark.parametrize('dct_P_max', [{'ts1': 2, 'ts2': 2}])
@pytest.mark.parametrize('dct_Q_max', [{'ts1': 2, 'ts2': 2}])
def test__tune_sarima(df: DF, dct_s: HP, dct_d: HP, dct_p_max: HP, dct_q_max: HP, dct_P_max: HP, dct_Q_max: HP):
	dct_kwargs = tune_sarima(df, dct_s, dct_d, dct_p_max, dct_q_max, dct_P_max, dct_Q_max)
	assert isinstance(dct_kwargs, dict)
	for name in df.keys():
		assert name in dct_kwargs
		assert isinstance(dct_kwargs[name], dict)
		assert len(dct_kwargs[name]) == 2
		assert 'order' in dct_kwargs[name]
		assert 'seasonal_order' in dct_kwargs[name]
	assert all(k in df for k in dct_kwargs.keys())
