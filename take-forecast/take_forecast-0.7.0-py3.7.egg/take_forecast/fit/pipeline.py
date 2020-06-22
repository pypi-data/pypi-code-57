# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

from kedro.pipeline import Pipeline, node
from .nodes import fit_sarima


def create_pipeline(**kwargs) -> Pipeline:
	"""Create a pipeline to fit SARIMA model.
	
	This pipeline execute following nodes:
	
	- Create and fit a ``statsmodels.api.tsa.SARIMAX``
	
	:keyword ``str`` case: Case name. Same used on preprocess pipeline.
	:return: Pipeline to fit SARIMA model.
	:rtype: ``kedro.pipeline.Pipeline``
	"""
	case = kwargs['case']
	c = (lambda name: '{case}_{name}'.format(case=case, name=name))
	return Pipeline(
		[
			node(
				fit_sarima,
				[c('new_users'), c('hyper_parameters')],
				c('sarima'),
				name='fit_sarima'
			)
		]
	)
