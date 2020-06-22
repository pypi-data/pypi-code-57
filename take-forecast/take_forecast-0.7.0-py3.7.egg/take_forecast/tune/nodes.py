# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.8.1'

import itertools as it
import typing as tp
import warnings as wn
import numpy as np
import pandas as pd
with wn.catch_warnings():
	wn.simplefilter('ignore')
	import statsmodels.api as sm

KW = tp.Dict[str, tp.Any]
HP = tp.Dict[str, int]
MHP = tp.Dict[str, KW]
TS = pd.Series
DF = pd.DataFrame
HP_HP = tp.Tuple[HP, HP]
DF_HP = tp.Tuple[DF, HP]
DF_DF = tp.Tuple[DF, DF]
DF_DF_HP = tp.Tuple[DF, DF, HP]


def _try_default_(function: tp.Callable, exceptions: tp.Tuple[tp.Type], default: tp.Any) -> tp.Callable:
	def decorator(*args, **kwargs):
		try:
			return function(*args, **kwargs)
		except exceptions:
			return default
	return decorator


def stationarity_test(ts: TS, threshold: float, n_diff: int) -> tp.Tuple[int, TS]:
	"""Find best estimated number of unit roots.
	
	This test uses Augmented Dickey Fuller test to check stationarity.
	Each time the tests finds transitory, witch means unit roots presence, take difference.
	Number of differences up to stationarity is estimated number of unit roots.
	
	:param ts: Time series.
	:type ts: ``pandas.TimeSeries``
	:param threshold: Threshold for Dickey Fuller.
	:type threshold: ``float``
	:param n_diff: Maximum number of differences to take.
	:type n_diff: ``int``
	:return: Results in tuple.
	
		* **d** (``int``) - Estimated number of unit roots.
		* **ts_stationary** (``pandas.TimeSeries``) - Stationary time series.
	:rtype: ``(int, pandas.TimeSeries)``
	"""
	d = 0
	ts_stationary = ts.dropna()
	
	for k in range(n_diff):
		adf, *_ = sm.tsa.adfuller(ts_stationary[k:])
		if adf > threshold:
			d += 1
			ts_stationary = ts_stationary.diff()
		else:
			break
	return d, ts_stationary


def seasonality_test(ts: TS, threshold: float, s_start: int, s_stop: int) -> tp.Tuple[bool, int]:
	"""Find best seasonal period.
	
	This test uses Jung Box at first two cycles and check maximum Q statistics for seasonal period.
	If all Jung Box Q statistics is lower that threshold, time series has no seasonality.
	
	:param ts: Time series.
	:type ts: ``pandas.TimeSeries``
	:param threshold: Threshold for Jung Box Q statistics.
	:type threshold: ``float``
	:param s_start: Start for seasonal period in test.
	:type s_start: ``int``
	:param s_stop: Stop for seasonal period in test.
	:type s_stop: ``int``
	:return: Results in tuple.
	
		* **is_seasonal** (``bool``) - True or false for seasonality.
		* **s** (``int``) - Seasonal period.
	:rtype: ``(bool, int)``
	"""
	ts = ts.dropna()
	s_stop = min(s_stop, ts.shape[0] // 4)
	is_seasonal = False
	s_range = list(range(s_start, s_stop))
	qstats = list()
	n = len(ts)
	
	for s in s_range:
		ts_mean = ts.rolling(3 * s, 1, center=True).mean()
		ts_std = ts.rolling(3 * s, 1, center=True).std()
		ts_norm = (ts - ts_mean) / ts_std
		acf = sm.tsa.acf(ts_norm, alpha=None, nlags=2 * s_stop, fft=False)
		mask = np.array([s, 2 * s])
		qstats.append(n * (n + 2) * np.sum(np.square(np.clip(acf[mask], 0, np.inf)) / (n - mask)))
		if qstats[-1] > threshold:
			is_seasonal = True
	return is_seasonal, s_range[int(np.argmax(qstats))]


def autocorrelation_test(ts: TS, s: int) -> tp.Tuple[int, int]:
	"""Find maximum number of lags for AR and MA model components based on autocorrelation.
	
	AR number of lags is found by partial autocorrelation, where null hypothesis is not more rejected.
	MA number of lags is found by autocorrelation, where null hypothesis is not more rejected.
	
	:param ts: Time series.
	:type ts: ``pandas.TimeSeries``
	:param s: Seasonal period. If not seasonal, 0.
	:type s: ``int``
	:return: Results in tuple.
	
		* **p_max** (``int``) - Maximum number of lags for AR.
		* **q_max** (``int``) - Maximum number of lags for MA.
	:rtype: ``(int, int)``
	"""
	nlags = (s - 1) if s else min(15, ts.shape[0] // 2)
	ts = ts.dropna()
	acf, acf_confint = sm.tsa.stattools.acf(ts, alpha=0.05, nlags=nlags, fft=False)
	pacf, pacf_confint = sm.tsa.stattools.pacf(ts, alpha=0.05, nlags=nlags)
	
	acf_nnull = acf_confint.prod(axis=1) > 0
	pacf_nnull = pacf_confint.prod(axis=1) > 0
	q_max = next(filter(acf_nnull.__getitem__, range(len(acf_nnull) - 1, -1, -1)))
	p_max = next(filter(pacf_nnull.__getitem__, range(len(pacf_nnull) - 1, -1, -1)))
	
	return p_max, q_max


def seasonal_autocorrelation_test(ts: TS, s: int, n_cycles: int) -> tp.Tuple[int, int]:
	"""Find maximum number of lags for seasonal AR and MA model components based on autocorrelation.
	
	Seasonal AR number of lags is found by partial autocorrelation, where null hypothesis is not more rejected.
	Seasonal MA number of lags is found by autocorrelation, where null hypothesis is not more rejected.
	If time series is not seasonal, returns zero for each one.
	
	:param ts: Time series.
	:type ts: ``pandas.TimeSeries``
	:param s: Seasonal period. If not seasonal, 0.
	:type s: ``int``
	:param n_cycles: Maximum number of cycles to analyse.
	:type n_cycles: ``int``
	:return: Results in tuple.
	
		* **P_max** (``int``) - Maximum number of lags for seasonal AR.
		* **Q_max** (``int``) - Maximum number of lags for seasonal MA.
	:rtype: ``(int, int)``
	"""
	if s == 0:
		return 0, 0
	
	n_cycles = min(n_cycles, int(0.5 * ts.shape[0] / s))
	nlags = s * n_cycles
	acf, acf_confint = sm.tsa.stattools.acf(ts, alpha=0.05, nlags=nlags, fft=False)
	pacf, pacf_confint = sm.tsa.stattools.pacf(ts, alpha=0.05, nlags=nlags)
	
	acf = acf[::s]
	acf_confint = acf_confint[::s]
	pacf = pacf[::s]
	pacf_confint = pacf_confint[::s]
	
	acf_nnull = acf_confint.prod(axis=1) > 0
	pacf_nnull = pacf_confint.prod(axis=1) > 0
	acf_nnull[np.abs(acf) > 1] = False
	pacf_nnull[np.abs(pacf) > 1] = False
	Q_max = next(filter(acf_nnull.__getitem__, range(len(acf_nnull) - 1, -1, -1)))
	P_max = next(filter(pacf_nnull.__getitem__, range(len(pacf_nnull) - 1, -1, -1)))
	
	return P_max, Q_max


def sarima_test(ts: TS, pdq: tp.Tuple[int, int, int], sPQ: tp.Optional[tp.Tuple[int, int, int]]=None) -> KW:
	"""Find best hyper parameters for SARIMA model.
	
	SARIMA is evaluated by AIC on given time series.
	Best hyper parameters is those minimize AIC.
	Hyper parameters are:
	
	- order: ``(p, d, q)``
	- seasonal order: ``(P, D, Q, s)``
	
	Where:
	
	- ``p`` is number of lags for AR
	- ``d`` is number of unit roots
	- ``q`` is number of lags for MA
	- ``P`` is number of lags for seasonal AR
	- ``D`` is number of seasonal roots
	- ``Q`` is number of lags for seasonal MA
	- ``s`` is seasonal period
	
	All combinations are tested in these constraints:
	
	- 0 <= ``p`` <= ``p_max``
	- 0 <= ``q`` <= ``q_max``
	- ``d`` + ``D`` = number of unit roots
	- 0 <= ``d``, ``D`` <= number of unit roots
	- 0 <= ``P`` <= ``P_max``
	- 0 <= ``Q`` <= ``Q_max``
	- ``s`` is given
	
	:param ts: Time series.
	:type ts: ``pandas.TimeSeries``
	:param pdq: Tuple with ``(p_max, unit_roots, q_max)``
	
		* **p_max** (``int``) - Maximum p.
		* **unit_roots** (``int``) - number of unit roots.
		* **q_max** (``int``) - Maximum q.
	:type pdq: ``(int, int, int)``
	:param sPQ: None for non seasonal or tuple with ``(s, P_max, Q_max)``
	
		* **s** (``int``) - Seasonal period.
		* **P_max** (``int``) - Maximum P.
		* **Q_max** (``int``) - Maximum Q.
	:type sPQ: ``(int, int, int)`` or ``None``
	:return: Hyper parameters for ``statsmodels.api.tsa.SARIMAX`` as kwargs.
	:rtype: ``dict`` from ``str`` to ``tuple`` of ``int``
	"""
	if sPQ:
		ranges = [range(lim + 1) for lim in (pdq[0], pdq[1], pdq[2], sPQ[1], sPQ[2])]
		to_kwargs = (lambda params: {
			'order': (params[0], params[1], params[2]),
			'seasonal_order': (params[3], (pdq[1] - params[1]), params[4], sPQ[0])
		})
	else:
		ranges = [range(lim + 1) for lim in (pdq[0], pdq[2])]
		to_kwargs = (lambda params: {
			'order': (params[0], pdq[1], params[1])
		})
	aic = (lambda kwargs: sm.tsa.SARIMAX(ts, **kwargs).fit(disp=False).aic)
	nan_aic = _try_default_(aic, (np.linalg.LinAlgError,), np.nan)
	
	with wn.catch_warnings():
		wn.simplefilter('ignore')
		return min(map(to_kwargs, it.product(*ranges)), key=nan_aic)


def transform_to_stationary(df: DF, threshold: float, n_diff: int) -> DF_HP:
	"""Transform each time series into stationary.
	
	Also finds estimated number of unit roots for each time series.
	
	:param df: Dataframe.
	:type df: ``pandas.DataFrame``
	:param threshold: Threshold for Dickey Fuller.
	:type threshold: ``float``
	:param n_diff: Maximum number of differences to take.
	:type n_diff: ``int``
	:return: Results in tuple.
	
		* **df_stationary** (``pandas.DataFrame``) - Dataframe with each time series stationary.
		* **dct_d** (``dict`` from ``str`` to ``int``) - Dict with each time series number of unit roots.
	:rtype: ``(pandas.DataFrame, dict)``
	"""
	dct_d = dict()
	df_stationary = pd.DataFrame(columns=df.columns)
	for name, ts in df.items():
		d, ts_stationary = stationarity_test(ts, threshold, n_diff)
		dct_d[name] = d
		df_stationary[name] = ts_stationary
	return df_stationary, dct_d


def decompose_seasonal(df: DF, threshold: float, s_start: int, s_stop: int) -> DF_DF_HP:
	"""Decompose each time series on dataframe in seasonal and non seasonal components.
	
	Also finds seasonal periods for each time series.
	For non seasonal time series, seasonal dataframe do not contains and seasonal period is zero.
	
	:param df: Dataframe.
	:type df: ``pandas.DataFrame``
	:param threshold: Threshold for Jung Box.
	:type threshold: ``float``
	:param s_start: Start for seasonal period in test.
	:type s_start: ``int``
	:param s_stop: Stop for seasonal period in test.
	:type s_stop: ``int``
	:return: Results in tuple.
	
		* **df_seasonal** (``pandas.DataFrame``) - Dataframe with seasonal components of seasonal time series.
		* **df_not_seasonal** (``pandas.DataFrame``) - Dataframe with non seasonal components of each time series.
		* **dct_s** (``dict`` from ``str`` to ``int``) - Dict with each time series seasonal period.
	:rtype: ``(pandas.DataFrame, pandas.DataFrame, dict)``
	"""
	dct_s = dict()
	df_seasonal = pd.DataFrame(columns=df.columns)
	df_not_seasonal = pd.DataFrame(columns=df.columns)
	for name, ts in df.items():
		is_seasonal, s = seasonality_test(ts, threshold, s_start, s_stop)
		if is_seasonal:
			dct_s[name] = s
			result = sm.tsa.STL(ts.dropna(), period=s).fit()
			df_seasonal[name] = result.seasonal
			df_not_seasonal[name] = result.trend + result.resid
		else:
			dct_s[name] = 0
			df_not_seasonal[name] = ts
	return df_seasonal, df_not_seasonal, dct_s


def analyse_autocorrelation(df: DF, dct_s: HP) -> HP_HP:
	"""Analyse each time series autocorrelation to find orders for AR and MA components.
	
	AR order is found by partial autocorrelation.
	MA order is found by autocorrelation.
	
	:param df: Dataframe.
	:type df: ``pandas.DataFrame``
	:param dct_s: Dict with each time series seasonal period.
	:type dct_s: ``dict`` from ``str`` to ``int``
	:return: Results in tuple.
	
		* **dct_p_max** (``dict`` from ``str`` to ``int``) - Dict with each time series maximum order for AR.
		* **dct_q_max** (``dict`` from ``str`` to ``int``) - Dict with each time series maximum order for MA.
	:rtype: ``(dict, dict)``
	"""
	dct_p_max = dict()
	dct_q_max = dict()
	for name, ts in df.items():
		p_max, q_max = autocorrelation_test(ts, dct_s[name])
		dct_p_max[name] = p_max
		dct_q_max[name] = q_max
	return dct_p_max, dct_q_max


def analyse_seasonal_autocorrelation(df: DF, dct_s: HP, n_cycles: int) -> HP_HP:
	"""Analyse each time series seasonal autocorrelation to find maximum orders for seasonal AR and MA 	components.
	
	AR order is found by partial autocorrelation.
	MA order is found by autocorrelation.
	
	:param df: Dataframe.
	:type df: ``pandas.DataFrame``
	:param dct_s: Dict with each time series seasonal period.
	:type dct_s: ``dict`` from ``str`` to ``int``
	:param n_cycles: Maximum number of cycles to analyse.
	:type n_cycles: ``int``
	:return: Results in tuple.
	
		* **dct_P_max** (``dict`` from ``str`` to ``int``) - Dict with each time series maximum order for seasonal AR.
		* **dct_Q_max** (``dict`` from ``str`` to ``int``) - Dict with each time series maximum order for seasonal MA.
	:rtype: ``(dict, dict)``
	"""
	dct_P_max = dict()
	dct_Q_max = dict()
	for name, ts in df.items():
		P_max, Q_max = seasonal_autocorrelation_test(ts, dct_s[name], n_cycles)
		dct_P_max[name] = P_max
		dct_Q_max[name] = Q_max
	return dct_P_max, dct_Q_max


def split_train_test(df: DF, r_split: int) -> DF_DF:
	"""Split data into train and test blocks.
	
	:param df: Dataframe.
	:type df: ``pandas.DataFrame``
	:param r_split: Data fraction to be train.
	:type r_split: ``float``
	:return: Results in tuple.
	
		* **df_train** (``pandas.DataFrame``) - Dataframe with train block.
		* **df_test** (``pandas.DataFrame``) - Dataframe with test block.
	:rtype: ``(pandas.DataFrame, pandas.DataFrame)``
	"""
	k = int(r_split * len(df))
	df_train = df.iloc[:k]
	df_test = df.iloc[k:]
	return df_train, df_test


def tune_sarima(df: DF, dct_s: HP, dct_d: HP, dct_p_max: HP, dct_q_max: HP, dct_P_max: HP, dct_Q_max: HP) -> MHP:
	"""Tune SARIMA hyper parameters for each time series.
	
	:param df: Dataframe.
	:type df: ``pandas.DataFrame``
	:param dct_s: Dict with each time series seasonal period.
	:type dct_s: ``dict`` from ``str`` to ``int``
	:param dct_d: Dict with each time series number of unit roots.
	:type dct_d: ``dict`` from ``str`` to ``int``
	:param dct_p_max: Dict with each time series maximum order for AR.
	:type dct_p_max: ``dict`` from ``str`` to ``int``
	:param dct_q_max: Dict with each time series maximum order for MA.
	:type dct_q_max: ``dict`` from ``str`` to ``int``
	:param dct_P_max: Dict with each time series maximum order for seasonal AR.
	:type dct_P_max: ``dict`` from ``str`` to ``int``
	:param dct_Q_max: Dict with each time series maximum order for seasonal MA.
	:type dct_Q_max: ``dict`` from ``str`` to ``int``
	:return: Dict with each time series SARIMA hyper parameters.
	:rtype: ``dict`` from ``str`` to ``dict`` from ``str`` to ``tuple`` of ``int``
	"""
	dct_kwargs = dict()
	for name, ts in df.items():
		p = dct_p_max[name]
		d = dct_d[name]
		q = dct_q_max[name]
		s = dct_s[name]
		P = dct_P_max[name]
		Q = dct_Q_max[name]
		pdq = (p, d, q)
		sPQ = (s, P, Q) if s else None
		kwargs = sarima_test(ts, pdq, sPQ)
		dct_kwargs[name] = kwargs
	return dct_kwargs
