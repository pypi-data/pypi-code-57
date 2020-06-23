# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp
import warnings as wn
import pytest
import numpy as np
import pandas as pd
with wn.catch_warnings():
	wn.simplefilter('ignore')
	from statsmodels.tsa.statespace.sarimax import SARIMAXResultsWrapper
	from statsmodels.tsa.statespace.mlemodel import PredictionResultsWrapper
from pytest_mock.plugin import MockFixture
from take_forecast.predict.nodes import predict_single_series
from take_forecast.predict.nodes import predict_series

TS = pd.Series
TS3 = tp.Tuple[TS, TS, TS]
DF = pd.DataFrame
MODEL = SARIMAXResultsWrapper
PREDICTION = PredictionResultsWrapper


@pytest.fixture
def dt_forecast():
	return '2020-12-31'


@pytest.fixture
def expected_pred(dt_forecast):
	np.random.seed(0)
	index = pd.period_range('2020-01-01', dt_forecast, freq='d')
	N = len(index)
	exp1 = np.logspace(1, 0.5, N)
	exp2 = np.logspace(1, -2, N)
	cos1 = np.cos(np.linspace(0, 10, N) * np.pi)
	cos2 = np.cos(np.linspace(0.25, 15.75, N) * np.pi)
	sigma = np.random.randn(N)
	data = 100 + 8 * exp1 + 16 * exp2 + 12 * cos1 + 6 * cos2 + 15 * sigma
	randn = np.random.randn(N)
	conf = np.cumsum(2 * (np.sign(randn) * randn))
	ts = pd.Series(data, index, name='ts')
	lower = pd.Series(data - conf, index, name='lower ts')
	upper = pd.Series(data + conf, index, name='upper ts')
	return ts, lower, upper


@pytest.fixture
def expected_df(dt_forecast):
	np.random.seed(0)
	index = pd.period_range('2020-01-01', dt_forecast, freq='d')
	N = len(index)
	exp1 = np.logspace(1, 0.5, N)
	exp2 = np.logspace(1, -2, N)
	cos1 = np.cos(np.linspace(0, 10, N) * np.pi)
	cos2 = np.cos(np.linspace(0.25, 15.75, N) * np.pi)
	sigma = np.random.randn(N)
	ts1 = 100 + 8 * exp1 + 16 * exp2 + 12 * cos1 + 6 * cos2 + 15 * sigma
	ts2 = 250 + 30 * cos1 * exp1 + 20 * cos2 * exp2 + 20 * sigma
	data = dict()
	for name, ts in zip(('ts1', 'ts2'), (ts1, ts2)):
		randn = np.random.randn(N)
		conf = np.cumsum(2 * (np.sign(randn) * randn))
		lower = pd.Series(ts - conf, index, name='lower ts')
		upper = pd.Series(ts + conf, index, name='upper ts')
		data[name] = ts
		data['lower {name}'.format(name=name)] = lower
		data['upper {name}'.format(name=name)] = upper
	return pd.DataFrame(data, index)


def build_mock_model(mocker, expected_ts, expected_lower, expected_upper):
	expected_conf_int = pd.DataFrame({
		expected_lower.name: expected_lower,
		expected_upper.name: expected_upper
	}, expected_ts.index)
	mock_orig_endog = mocker.MagicMock()
	mock_orig_endog.name = expected_ts.name
	mock_data = mocker.Mock()
	mock_data.orig_endog = mock_orig_endog
	mock_forecast = mocker.Mock(spec=PREDICTION)
	mock_forecast.predicted_mean = expected_ts
	mock_forecast.conf_int = mocker.Mock(side_effect=(lambda: expected_conf_int))
	mock_model = mocker.Mock(spec=MODEL)
	mock_model.data = mock_data
	mock_model.get_forecast = mocker.Mock(side_effect=(lambda dt: mock_forecast))
	return mock_model


def test__predict_single_series(mocker: MockFixture, expected_pred: TS3, dt_forecast: str):
	expected_ts, expected_lower, expected_upper = expected_pred
	mock_model = build_mock_model(mocker, expected_ts, expected_lower, expected_upper)
	
	ts, lower, upper = predict_single_series(mock_model, dt_forecast)
	assert isinstance(ts, TS)
	assert isinstance(lower, TS)
	assert isinstance(upper, TS)
	pd.testing.assert_series_equal(ts, expected_ts)
	pd.testing.assert_series_equal(lower, expected_lower)
	pd.testing.assert_series_equal(upper, expected_upper)
	mock_model.get_forecast.assert_called_once_with(dt_forecast)


def test__predict_series(mocker: MockFixture, expected_df: DF, dt_forecast: str):
	horizon = '10d'
	names = [
		name
		for name in expected_df
		if not any(map(name.startswith, ('lower ', 'upper ')))
	]
	
	expected_dt_forecast = (pd.Timestamp.now() + pd.Timedelta(horizon)).strftime('%Y-%m-%d')
	mock_models = dict()
	for name in names:
		expected_ts = expected_df[name]
		expected_lower = expected_df['lower {name}'.format(name=name)]
		expected_upper = expected_df['upper {name}'.format(name=name)]
		mock_model = build_mock_model(mocker, expected_ts, expected_lower, expected_upper)
		mock_models[name] = mock_model
	
	df = predict_series(mock_models, horizon)
	assert isinstance(df, pd.DataFrame)
	pd.testing.assert_frame_equal(df, expected_df)
	for mock_model in mock_models.values():
		mock_model.get_forecast.assert_called_once_with(expected_dt_forecast)
