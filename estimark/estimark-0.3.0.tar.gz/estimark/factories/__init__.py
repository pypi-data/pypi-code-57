from injectark import FactoryBuilder
from .base_factory import BaseFactory
from .altair_factory import AltairFactory
from .check_factory import CheckFactory
from .rst_factory import RstFactory
from .json_factory import JsonFactory
from .strategies import strategy_builder


factory_builder = FactoryBuilder([
    BaseFactory, CheckFactory, AltairFactory, JsonFactory, RstFactory])

__all__ = [
    'strategy_builder',
    'factory_builder'
]
