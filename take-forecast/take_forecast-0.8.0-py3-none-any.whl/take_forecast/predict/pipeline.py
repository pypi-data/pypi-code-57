# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

from kedro.pipeline import Pipeline, node
from .nodes import predict_series


def create_pipeline(**kwargs) -> Pipeline:
	"""Create a pipeline to predict series from SARIMA models.
	
	This pipeline execute following nodes:
	
	- Get prediction with confidence interval.
	
	:keyword ``str`` case: Case name. Same used on preprocess pipeline.
	:return: Pipeline to predict series.
	:rtype: ``kedro.pipeline.Pipeline``
	"""
	case = kwargs['case']
	c = (lambda name: '{case}_{name}'.format(case=case, name=name))
	p = (lambda name: 'params:{case}_{name}'.format(case=case, name=name))
	return Pipeline(
		[
			node(
				predict_series,
				[c('sarima'), p('horizon')],
				c('forecast'),
				name='predict_series'
			)
		]
	)
