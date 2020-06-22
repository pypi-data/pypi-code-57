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
DF = pd.DataFrame
MODEL = SARIMAXResultsWrapper
D_MODEL = tp.Dict[str, MODEL]


def fit_single_sarima(ts: TS, kwargs: KW) -> MODEL:
	"""Fit a SARIMA for data in time series and given hyper parameters.
	
	Model is optimized by maximizing likelihood with Kalman filter.
	Returned object can make predictions at train time or forecast at time before.-
	
	:param ts: Time series.
	:type ts: ``pandas.TimeSeries``
	:param kwargs: Hyper parameters for ``statsmodels.api.tsa.SARIMAX`` as kwargs.
	
		* **order** (``(int, int, int)``) - Order for AR, I and MA.
		* **seasonal_order** (``(int, int, int, int)``) - Seasonality and order for seasonals AR, I and MA.
	:type kwargs: ``dict`` from ``str`` to ``tuple`` of ``int``
	:return: Fitted SARIMA model.
	:rtype: ``statsmodels.api.tsa.MLEResult``
	"""
	with wn.catch_warnings():
		wn.simplefilter('ignore')
		return SARIMAX(ts, **kwargs).fit(disp=False)


def fit_sarima(df: DF, dct_kwargs: D_KW) -> D_MODEL:
	"""Fit SARIMA for each time series.
	
	:param df: Dataframe.
	:type df: ``pandas.DataFrame``
	:param dct_kwargs: Dict with each time series hyper parameters.
	:type dct_kwargs: ``dict`` from ``str`` to ``dict`` from ``str`` to ``tuple`` of ``int``
	:return: Dict with each time series fitted SARIMA.
	:rtype: ``dict`` from ``str`` to ``statsmodels.api.tsa.MLEResult``
	"""
	dct_model = dict()
	for name, ts in df.items():
		kwargs = dct_kwargs[name]
		dct_model[name] = fit_single_sarima(ts, kwargs)
	return dct_model
