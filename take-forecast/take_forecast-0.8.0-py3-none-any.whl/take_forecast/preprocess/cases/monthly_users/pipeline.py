# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.3.0'

from kedro.pipeline import Pipeline, node
from ..register import register
from .nodes import filter_by_client
from .nodes import format_dataframe
from .nodes import limit_by_time
from .nodes import transform_to_daily_new_users


@register('MUs')
def create_pipeline(**_) -> Pipeline:
	"""Create a pipeline to preprocess monthly users.
	
	This pipeline execute following nodes:
	
	- Filter data by client
	- Format data by datetime
	- Limit data by initial datetime
	- Transform cumulative users at month to new diary users at month.
	
	:return: Pipeline to preprocess monthly users.
	:rtype: ``kedro.pipeline.Pipeline``
	"""
	case = 'MUs'
	c = (lambda name: '{case}_{name}'.format(case=case, name=name))
	p = (lambda name: 'params:{case}_{name}'.format(case=case, name=name))
	return Pipeline([
		node(
			filter_by_client,
			[c('raw_data'), p('client')],
			c('filtered'),
			name='filter_by_client'
		),
		node(
			format_dataframe,
			c('filtered'),
			c('formatted'),
			name='format_dataframe'
		),
		node(
			limit_by_time,
			[c('formatted'), p('t_init')],
			c('limited'),
			name='limit_by_time'
		),
		node(
			transform_to_daily_new_users,
			c('limited'),
			c('new_users'),
			name='transform_to_daily_new_users'
		)
	])
