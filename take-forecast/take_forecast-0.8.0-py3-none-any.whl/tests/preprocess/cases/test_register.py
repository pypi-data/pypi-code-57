# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

from take_forecast.preprocess.cases import register, registered


def test__create_pipeline():
	case = 'case'
	expected_value = object()
	
	decorator = register(case)
	assert callable(decorator)
	
	value = decorator(expected_value)
	assert case in registered
	assert registered[case] is value
	assert value is expected_value
