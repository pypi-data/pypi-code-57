# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.9.0'

import typing as tp
import operator as op
import functools as ft
from pathlib import Path
from kedro.config import ConfigLoader
from kedro.context import load_context
from kedro.pipeline import Pipeline
from take_forecast.utils import build_pipeline


def load_pipeline(loader: ConfigLoader, filename: str) -> tp.Dict[str, Pipeline]:
	"""Load pipeline from config.
	
	:param loader: Config loader.
	:type loader: ``kedro.config.config.ConfigLoader``
	:param filename: Filename to load config.
	:type filename: ``str``
	:return: Pipeline in dict.
	:rtype: ``dict`` from ``str`` to ``kedro.pipeline.Pipeline``
	"""
	pipelines = dict()
	dct_pipeline_setting = loader.get(filename)
	for key, pipeline_setting in dct_pipeline_setting.items():
		pipelines[key] = build_pipeline(pipeline_setting)
	return pipelines


def load_pipelines(loader: ConfigLoader, filename: str, variables: tp.List[str]) -> tp.Dict[str, Pipeline]:
	"""Load pipelines from config.
	
	:param loader: Config loader.
	:type loader: ``kedro.config.config.ConfigLoader``
	:param filename: Filename to load config.
	:type filename: ``str``
	:param variables: Variables for template.
	:type variables: ``list`` of ``str``
	:return: Pipelines in dict.
	:rtype: ``dict`` from ``str`` to ``kedro.pipeline.Pipeline``
	"""
	pipelines = dict()
	dct_pipeline_setting = loader.get(filename)
	for template_key, pipeline_setting in dct_pipeline_setting.items():
		for variable in variables:
			key = template_key.replace('VARIABLE', variable)
			pipelines[key] = build_pipeline(pipeline_setting, variable)
	return pipelines


def create_pipelines(**_) -> tp.Dict[str, Pipeline]:
	"""Create pipelines for project and users.
	
	:return: All pipelines in a dict.
	:rtype: ``dict`` from ``str`` to ``kedro.pipeline.Pipeline``
	"""
	pipelines = dict()
	context = load_context(Path.cwd())
	loader = context.config_loader
	variables = context.params['variables']
	yml = (lambda step: 'pipelines/{step}.yml'.format(step=step))
	
	pipelines.update(load_pipeline(loader, yml('preprocess')))
	for variable in variables:
		filename = 'pipelines/preprocess/{variable}.yml'.format(variable=variable)
		pipelines.update(load_pipelines(loader, filename, [variable]))
	pipelines.update(load_pipelines(loader, yml('tune'), variables))
	pipelines.update(load_pipelines(loader, yml('fit'), variables))
	pipelines.update(load_pipelines(loader, yml('predict'), variables))
	for variable in variables:
		filename = 'pipelines/posprocess/{variable}.yml'.format(variable=variable)
		pipelines.update(load_pipelines(loader, filename, [variable]))
	pipelines.update(load_pipeline(loader, yml('posprocess')))
	
	steps = ['preprocess', 'tune', 'fit', 'predict', 'posprocess']
	for variable in variables:
		pipelines[variable] =\
			pipelines['preprocess'] +\
			ft.reduce(op.add, [
				pipelines['{variable}_{step}'.format(variable=variable, step=step)]
				for step in steps
			]) +\
			pipelines['posprocess']
	
	pipelines['__default__'] = ft.reduce(op.add, pipelines.values())
	return pipelines
