# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import warnings as wn
import pytest
import numpy as np
import pandas as pd
with wn.catch_warnings():
	wn.simplefilter('ignore')
	from statsmodels.tsa.statespace.sarimax import SARIMAXResultsWrapper
from take_forecast.fit.nodes import fit_single_sarima
from take_forecast.fit.nodes import fit_sarima

TS = pd.Series
DF = pd.DataFrame
MODEL = SARIMAXResultsWrapper


@pytest.fixture
def ts():
	np.random.seed(0)
	index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
	N = len(index)
	exp1 = np.logspace(1, 0.5, N)
	exp2 = np.logspace(1, -2, N)
	cos1 = np.cos(np.linspace(0, 10, N) * np.pi)
	cos2 = np.cos(np.linspace(0.25, 15.75, N) * np.pi)
	sigma = np.random.randn(N)
	data = 100 + 8 * exp1 + 16 * exp2 + 12 * cos1 + 6 * cos2 + 15 * sigma
	return pd.Series(data, index, name='ts')


@pytest.fixture
def df():
	np.random.seed(0)
	index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
	N = len(index)
	exp1 = np.logspace(1, 0.5, N)
	exp2 = np.logspace(1, -2, N)
	cos1 = np.cos(np.linspace(0, 10, N) * np.pi)
	cos2 = np.cos(np.linspace(0.25, 15.75, N) * np.pi)
	sigma = np.random.randn(N)
	data = {
		'ts1': 100 + 8 * exp1 + 16 * exp2 + 12 * cos1 + 6 * cos2 + 15 * sigma,
		'ts2': 250 + 30 * cos1 * exp1 + 20 * cos2 * exp2 + 20 * sigma
	}
	return pd.DataFrame(data, index)


@pytest.mark.parametrize('p', [0, 1, 2])
@pytest.mark.parametrize('d', [0, 1])
@pytest.mark.parametrize('q', [0, 1])
def test__fit_single_sarima__non_seasonal(ts: TS, p: int, d: int, q: int):
	kwargs = {
		'order': (p, d, q)
	}
	model = fit_single_sarima(ts, kwargs)
	assert isinstance(model, MODEL)


@pytest.mark.parametrize('p', [0, 1, 2])
@pytest.mark.parametrize('d', [0, 1])
@pytest.mark.parametrize('q', [0, 1])
@pytest.mark.parametrize('s', [7, 12])
@pytest.mark.parametrize('P', [0, 1])
@pytest.mark.parametrize('D', [0])
@pytest.mark.parametrize('Q', [0, 1])
def test__fit_single_sarima__seasonal(ts: TS, p: int, d: int, q: int, s: int, P: int, D: int, Q: int):
	kwargs = {
		'order': (p, d, q),
		'seasonal_order': (P, D, Q, s)
	}
	model = fit_single_sarima(ts, kwargs)
	assert isinstance(model, MODEL)


@pytest.mark.parametrize('p', [0, 1, 2])
@pytest.mark.parametrize('d', [0, 1])
@pytest.mark.parametrize('q', [0, 1])
def test__fit_sarima__non_seasonal(df: DF, p: int, d: int, q: int):
	kwargs = {
		'order': (p, d, q)
	}
	dct_kwargs = {
		name: kwargs
		for name in df.keys()
	}
	dct_models = fit_sarima(df, dct_kwargs)
	assert isinstance(dct_models, dict)
	for name in df.keys():
		assert name in dct_models
		assert isinstance(dct_models[name], MODEL)
	assert all(k in df for k in dct_models.keys())


@pytest.mark.parametrize('p', [0, 1, 2])
@pytest.mark.parametrize('d', [0, 1])
@pytest.mark.parametrize('q', [0, 1])
@pytest.mark.parametrize('s', [7, 12])
@pytest.mark.parametrize('P', [0, 1])
@pytest.mark.parametrize('D', [0])
@pytest.mark.parametrize('Q', [0, 1])
def test__fit_sarima__seasonal(df: DF, p: int, d: int, q: int, s: int, P: int, D: int, Q: int):
	kwargs = {
		'order': (p, d, q),
		'seasonal_order': (P, D, Q, s)
	}
	dct_kwargs = {
		name: kwargs
		for name in df.keys()
	}
	dct_models = fit_sarima(df, dct_kwargs)
	assert isinstance(dct_models, dict)
	for name in df.keys():
		assert name in dct_models
		assert isinstance(dct_models[name], MODEL)
	assert all(k in df for k in dct_models.keys())
