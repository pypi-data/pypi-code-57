# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp
import pytest
from kedro.pipeline import Pipeline
from kedro.pipeline.node import Node
from take_forecast.utils.build_pipeline import build_node, build_pipeline


def test__build_node__empty_input():
	node_setting = {
		'func': 'time.time',
		'inputs': [],
		'outputs': ['now']
	}
	node = build_node(node_setting)
	assert isinstance(node, Node)
	assert len(node.inputs) == 0
	assert len(node.outputs) == 1
	assert node.outputs[0] == 'now'
	assert node.name == 'time'


def test__build_node__empty_output():
	node_setting = {
		'func': 'time.sleep',
		'inputs': ['seconds'],
		'outputs': []
	}
	node = build_node(node_setting)
	assert isinstance(node, Node)
	assert len(node.inputs) == 1
	assert node.inputs[0] == 'seconds'
	assert len(node.outputs) == 0
	assert node.name == 'sleep'


@pytest.mark.parametrize('func_name', [('operator.add', 'add'), ('builtins.pow', 'pow')])
@pytest.mark.parametrize('inputs', [['a', 'b'], ['a', 'params:p'], ['params:q', 'b']])
@pytest.mark.parametrize('outputs', [['result'], ['y']])
def test__build_node__no_variable(func_name: tp.Tuple[str, str], inputs: tp.List[str], outputs: tp.List[str]):
	func, name = func_name
	node_setting = {
		'func': func,
		'inputs': inputs,
		'outputs': outputs
	}
	node = build_node(node_setting)
	assert isinstance(node, Node)
	assert all(i1 == i2 for i1, i2 in zip(node.inputs, inputs))
	assert all(o1 == o2 for o1, o2 in zip(node.outputs, outputs))
	assert node.name == name


@pytest.mark.parametrize('func_name', [('operator.add', 'add'), ('builtins.pow', 'pow')])
@pytest.mark.parametrize('inputs', [['VARIABLE_a', 'b'], ['VARIABLE_a', 'params:p'], ['params:q', 'VARIABLE_b']])
@pytest.mark.parametrize('outputs', [['VARIABLE_result'], ['VARIABLE']])
@pytest.mark.parametrize('variable', ['x', 'y', 'number'])
def test__build_node(func_name: tp.Tuple[str, str], inputs: tp.List[str], outputs: tp.List[str], variable: str):
	func, name = func_name
	node_setting = {
		'func': func,
		'inputs': inputs,
		'outputs': outputs
	}
	node = build_node(node_setting, variable)
	assert isinstance(node, Node)
	assert all(i1 == i2.replace('VARIABLE', variable) for i1, i2 in zip(node.inputs, inputs))
	assert all(o1 == o2.replace('VARIABLE', variable) for o1, o2 in zip(node.outputs, outputs))
	assert node.name == '{variable}_{name}'.format(variable=variable, name=name)


def test__build_pipeline__no_variable():
	pipeline_setting = [
		{
			'func': 'operator.sub',
			'inputs': ['y_true', 'y_pred'],
			'outputs': ['e']
		},
		{
			'func': 'builtins.pow',
			'inputs': ['e', 'params:exp'],
			'outputs': ['se']
		},
		{
			'func': 'numpy.mean',
			'inputs': ['se'],
			'outputs': ['mse']
		}
	]
	pipeline = build_pipeline(pipeline_setting)
	assert isinstance(pipeline, Pipeline)
	assert len(pipeline.nodes) == 3


@pytest.mark.parametrize('variable', ['x', 'y', 'number'])
def test__build_pipeline__(variable: str):
	pipeline_setting = [
		{
			'func': 'operator.sub',
			'inputs': ['VARIABLE_true', 'VARIABLE_pred'],
			'outputs': ['VARIABLE_e']
		},
		{
			'func': 'builtins.pow',
			'inputs': ['VARIABLE_e', 'params:exp'],
			'outputs': ['VARIABLE_se']
		},
		{
			'func': 'numpy.mean',
			'inputs': ['VARIABLE_se'],
			'outputs': ['VARIABLE_mse']
		}
	]
	pipeline = build_pipeline(pipeline_setting, variable)
	assert isinstance(pipeline, Pipeline)
	assert len(pipeline.nodes) == 3
