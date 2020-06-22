# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

from kedro.pipeline import Pipeline
from take_forecast.fit.pipeline import create_pipeline


def test__create_pipeline():
	case = 'MUs'
	pipeline = create_pipeline(case=case)
	assert isinstance(pipeline, Pipeline)
	
	catalog_prefix = case
	parameter_prefix = 'params:{case}'.format(case=case)
	
	inputs = pipeline.all_inputs()
	for i in inputs:
		if i.startswith('params:'):
			assert i.startswith(parameter_prefix)
		else:
			assert i.startswith(catalog_prefix)
	
	outputs = pipeline.all_outputs()
	for o in outputs:
		assert o.startswith(catalog_prefix)
