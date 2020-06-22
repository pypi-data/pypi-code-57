# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

from pytest_mock.plugin import MockFixture
from kedro.pipeline import Pipeline
from take_forecast.preprocess.pipeline import create_pipeline
from take_forecast.preprocess.cases import register


def test__create_pipeline(mocker: MockFixture):
	case = 'case'
	mocked = mocker.Mock(side_effect=(lambda **kwargs: Pipeline([])))
	kwargs = {'case': case, 'key': 'value'}
	
	register(case)(mocked)
	pipeline = create_pipeline(**kwargs)
	
	assert isinstance(pipeline, Pipeline)
	mocked.assert_called_once_with()
