# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.7.0'

from kedro.pipeline import Pipeline, node
from .nodes import decompose_seasonal
from .nodes import transform_to_stationary
from .nodes import analyse_autocorrelation
from .nodes import analyse_seasonal_autocorrelation
from .nodes import split_train_test
from .nodes import tune_sarima


def create_pipeline(**kwargs) -> Pipeline:
	"""Create a pipeline to tune hyper parameters for SARIMA model.
	
	This pipeline execute following nodes:
	
	- Decompose seasonal component with Jung Box test
	- Transform to stationary series with ADF test
	- Analyse autocorrelation at stationary series
	- Analyse seasonal autocorrelation at series
	- Split data into train and test blocks
	- Tune hyper parameters on train data with AIC
	
	:keyword ``str`` case: Case name. Same used on preprocess pipeline.
	:return: Pipeline to tune SARIMA hyper parameters.
	:rtype: ``kedro.pipeline.Pipeline``
	"""
	case = kwargs['case']
	c = (lambda name: '{case}_{name}'.format(case=case, name=name))
	p = (lambda name: 'params:{case}_{name}'.format(case=case, name=name))
	return Pipeline(
		[
			node(
				transform_to_stationary,
				[c('new_users'), p('adf_threshold'), p('adf_n_diff')],
				[c('stationary'), c('d')],
				name='transform_to_stationary'
			),
			node(
				decompose_seasonal,
				[c('stationary'), p('seasonal_threshold'), p('s_start'), p('s_stop')],
				[c('seasonal'), c('not_seasonal'), c('s')],
				name='decompose_seasonal'
			),
			node(
				analyse_autocorrelation,
				[c('stationary'), c('s')],
				[c('p_max'), c('q_max')],
				name='analyse_autocorrelation'
			),
			node(
				analyse_seasonal_autocorrelation,
				[c('new_users'), c('s'), p('seasonal_acf_n_cycles')],
				[c('sP_max'), c('sQ_max')],
				name='analyse_seasonal_autocorrelation'
			),
			node(
				split_train_test,
				[c('new_users'), p('r_split')],
				[c('train'), c('test')],
				name='split_train_test'
			),
			node(
				tune_sarima,
				[c('train'), c('s'), c('d'), c('p_max'), c('q_max'), c('sP_max'), c('sQ_max')],
				c('hyper_parameters'),
				name='tune_sarima'
			)
		]
	)
