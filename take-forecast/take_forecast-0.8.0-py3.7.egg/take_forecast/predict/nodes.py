# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp
import warnings as wn
import pandas as pd
with wn.catch_warnings():
	wn.simplefilter('ignore')
	from statsmodels.tsa.statespace.sarimax import SARIMAX, SARIMAXResultsWrapper

KW = tp.Dict[str, tp.Any]
D_KW = tp.Dict[str, KW]
TS = pd.Series
TS3 = tp.Tuple[TS, TS, TS]
DF = pd.DataFrame
MODEL = SARIMAXResultsWrapper
D_MODEL = tp.Dict[str, MODEL]


def predict_single_series(model: MODEL, dt_forecast: str) -> TS3:
	"""Predict a time series with a fitted SARIMA model and date up to forecast.
	
	Gives prediction and confidence interval limits.
	
	:param model: Fitted SARIMA model.
	:type model: ``statsmodels.api.tsa.MLEResult``
	:param dt_forecast: Date to forecast.
	:type dt_forecast: ``str``
	:return: Results in tuple:
	
		* **ts_pred** (``pandas.TimeSeries``) - Prediction.
		* **ts_lower** (``pandas.TimeSeries``) - Lower limit.
		* **ts_upper** (``pandas.TimeSeries``) - Upper limit.
	:rtype: ``(pandas.TimeSeries, pandas.TimeSeries, pandas.TimeSeries)``
	"""
	pred = model.get_forecast(dt_forecast)
	ts_pred = pred.predicted_mean
	conf_int = pred.conf_int()
	name = model.data.orig_endog.name
	ts_pred.name = name
	ts_lower = conf_int['lower {name}'.format(name=name)]
	ts_upper = conf_int['upper {name}'.format(name=name)]
	return ts_pred, ts_lower, ts_upper


def predict_series(dct_model: D_MODEL, horizon: str) -> DF:
	"""Predict a time series for each fitted SARIMA model up to horizon forward.
	
	:param dct_model: Dict with each time series fitted SARIMA.
	:type dct_model: ``dict`` from ``str`` to ``statsmodels.api.tsa.MLEResult``
	:param horizon: Horizon to define up to forecast since today.
	:type horizon: ``str``
	:return: Dataframe with predictions and confidence intervals.
	:rtype: ``pandas.DataFrame``
	"""
	data = dict()
	dt_forecast = (pd.Timestamp.now() + pd.Timedelta(horizon)).strftime('%Y-%m-%d')
	for name, model in dct_model.items():
		ts_pred, ts_lower, ts_upper = predict_single_series(model, dt_forecast)
		data[ts_pred.name] = ts_pred
		data[ts_lower.name] = ts_lower
		data[ts_upper.name] = ts_upper
	return pd.DataFrame(data)
