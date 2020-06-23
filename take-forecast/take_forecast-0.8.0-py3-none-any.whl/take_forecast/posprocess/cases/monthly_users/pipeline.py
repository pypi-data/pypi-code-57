# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

from kedro.pipeline import Pipeline, node
from ..register import register
from .nodes import transform_to_cumulative_users


@register('MUs')
def create_pipeline(**_) -> Pipeline:
	"""Create a pipeline to posprocess monthly users.
	
	This pipeline execute following nodes:
	
	- Filter data by client
	- Format data by datetime
	- Limit data by initial datetime
	- Transform new diary users at month to cumulative users at month.
	
	:return: Pipeline to posprocess monthly users.
	:rtype: ``kedro.pipeline.Pipeline``
	"""
	case = 'MUs'
	c = (lambda name: '{case}_{name}'.format(case=case, name=name))
	return Pipeline([
		node(
			transform_to_cumulative_users,
			[c('forecast'), c('limited')],
			c('output'),
			name='transform_to_cumulative_users'
		)
	])
