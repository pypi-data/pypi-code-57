# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp

registered = dict()


def register(name: str) -> tp.Callable:
	"""Register a posprocess pipeline creator.
	
	Use it as decorator for ``create_pipeline`` function.
	
	Example:
	::
	>>> from kedro.pipeline import Pipeline, node
	>>> @register('name')
	>>> def create_pipeline(**_) -> Pipeline:
	>>>     return Pipeline([node(sum, ['df'], ['total'])])
	
	:param name: Case name.
	:type name: ``str``
	:return: Decorator for posprocess pipeline creator.
	:rtype: ``function``
	"""
	def decorator(creator):
		registered[name] = creator
		return creator
	return decorator
