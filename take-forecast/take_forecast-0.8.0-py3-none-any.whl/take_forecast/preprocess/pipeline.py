# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.3.0'

from kedro.pipeline import Pipeline
from .cases import registered


def create_pipeline(**kwargs) -> Pipeline:
	"""Create a pipeline to preprocess a given case.
	
	:keyword ``str`` case: Case name. Can be MUs.
	:return: Pipeline to preprocess a given case.
	:rtype: ``kedro.pipeline.Pipeline``
	"""
	case = kwargs['case']
	creator = registered[case]
	return creator()
