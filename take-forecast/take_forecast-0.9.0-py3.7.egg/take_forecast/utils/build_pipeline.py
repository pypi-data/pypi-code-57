# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp
from kedro.pipeline import Pipeline
from kedro.pipeline.node import Node
from kedro.utils import load_obj


NODE = tp.Dict[str, tp.Union[str, tp.List[str]]]
PIPELINE = tp.List[NODE]


def build_node(node_setting: NODE, variable: tp.Optional[str]=None) -> Node:
	"""Build a node from settings using standard for a variable.
	
	In this node, all catalog data, parameters and nodes are prefixes by variable, except base parameters.
	Node setting is like:
	::
	>>> node_setting = {'function': 'numpy.sum', 'input': ['x', 'y'], 'output': ['z']}
	>>> node = build_node(node_setting)
	
	:param node_setting: Node settings.
	:type node_setting: ``dict`` from ``str`` to (``str`` or ``list`` of ``str``)
	:param variable: Variable name.
	:type variable: ``str``
	:return: Node.
	:rtype: ``kedro.pipeline.node.Node``
	"""
	func = load_obj(node_setting['func'])
	if variable is None:
		inputs = node_setting['inputs']
		outputs = node_setting['outputs']
		name = func.__name__
	else:
		inputs = [i.replace('VARIABLE', variable) for i in node_setting['inputs']]
		outputs = [o.replace('VARIABLE', variable) for o in node_setting['outputs']]
		name = '{variable}_{func}'.format(variable=variable, func=func.__name__)
	if len(inputs) == 0:
		inputs = None
	elif len(inputs) == 1:
		inputs = inputs[0]
	if len(outputs) == 0:
		outputs = None
	elif len(outputs) == 1:
		outputs = outputs[0]
	return Node(func, inputs, outputs, name=name)


def build_pipeline(pipeline_setting: PIPELINE, variable: tp.Optional[str]=None) -> Pipeline:
	"""Build a pipeline from settings using standard for a variable.
	
	In this pipeline, all catalog data, parameters and nodes are prefixes by variable, except base parameters.
	Pipeline setting is like:
	::
	>>> pipeline_setting = [
	>>>     {'function': 'numpy.sum', 'input': ['x', 'y'], 'output': ['z']},
	>>>     {'function': 'numpy.power', 'input': ['z'], 'params': ['p'], 'output': ['q']},
	>>> ]
	>>> pipeline = build_pipeline(pipeline_setting, 'myVariable')
	
	:param pipeline_setting: Pipeline settings.
	:type pipeline_setting: ``list`` of ``dict`` from ``str`` to (``str`` or ``list`` of ``str``)
	:param variable: Variable name.
	:type variable: ``str``
	:return: Pipeline.
	:rtype: ``kedro.pipeline.Pipeline``
	"""
	return Pipeline([build_node(ns, variable) for ns in pipeline_setting])
