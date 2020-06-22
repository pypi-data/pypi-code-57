# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.7.0'

import typing as tp
import operator as op
import functools as ft
from pathlib import Path
from kedro.context import load_context
from kedro.pipeline import Pipeline
from take_forecast import preprocess, tune, fit


def create_pipelines(**_) -> tp.Dict[str, Pipeline]:
	"""Create pipelines for project and users.
	
	:return: All pipelines in a dict.
	:rtype: ``dict`` from ``str`` to ``kedro.pipeline.Pipeline``
	"""
	
	pipelines = dict()
	
	context = load_context(Path.cwd())
	loader = context.config_loader
	cases = loader.get('cases.yml')['cases']
	for case in cases:
		pl_preprocess = preprocess.create_pipeline(case=case)
		pl_tune = tune.create_pipeline(case=case)
		pl_fit = fit.create_pipeline(case=case)
		pipelines['{case}_preprocess'.format(case=case)] = pl_preprocess
		pipelines['{case}_tune'.format(case=case)] = pl_tune
		pipelines['{case}_fit'.format(case=case)] = pl_fit
	
	pipelines['__default__'] = ft.reduce(op.add, pipelines.values())
	return pipelines
