# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

import typing as tp
import warnings as wn
import pandas as pd
with wn.catch_warnings():
	wn.simplefilter('ignore')
	from statsmodels.tsa.statespace.sarimax import MLEResults


KW = tp.Dict[str, tp.Any]
TS = pd.Series
TS3 = tp.Tuple[TS, TS, TS]
MODEL = MLEResults


def predict_series(model: MODEL, horizon: str) -> TS3:
	"""Predict a time series with a fitted SARIMA model and date up to forecast.
	
	Gives prediction and confidence interval limits.
	
	:param model: Fitted SARIMA model.
	:type model: ``statsmodels.api.tsa.statespace.mlemodel.MLEResults``
	:param horizon: Horizon to define up to forecast since today.
	:type horizon: ``str``
	:return: Results in tuple:
	
		* **ts_pred** (``pandas.Series``) - Prediction.
		* **ts_lower** (``pandas.Series``) - Lower limit.
		* **ts_upper** (``pandas.Series``) - Upper limit.
	:rtype: ``(pandas.Series, pandas.Series, pandas.Series)``
	"""
	dt_forecast = pd.Timestamp.now() + pd.Timedelta(horizon)
	pred = model.get_forecast(dt_forecast)
	ts_pred = pred.predicted_mean
	conf_int = pred.conf_int()
	name = model.data.orig_endog.name
	ts_lower = conf_int['lower {name}'.format(name=name)]
	ts_upper = conf_int['upper {name}'.format(name=name)]
	ts_pred.name = name
	ts_lower.name = 'lower {name}'.format(name=name)
	ts_upper.name = 'upper {name}'.format(name=name)
	return ts_pred, ts_lower, ts_upper
