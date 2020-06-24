from injectark import StrategyBuilder
from .altair import altair
from .base import base
from .check import check
from .json import json
from .rst import rst



strategy_builder = StrategyBuilder({
    'base': base,
    'altair': altair,
    'check': check,
    'json': json,
    'rst': rst
})
