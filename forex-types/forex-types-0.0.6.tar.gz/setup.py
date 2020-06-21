# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forex_types']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'forex-types',
    'version': '0.0.6',
    'description': 'Basic Forex Classes',
    'long_description': '# python_forex_types\nClass models for Eight major Forex Currency Pairs.\n\n\n\n### Summary of Classes provided\nclass | init example | description\n --- | --- | ---\n Calc | -- | Has class methods for doing calculations with other types.\n Cash | Cash("102.231", Currency.JPY) | Cash represented by decimal number and currency.\n Currency | Currency("EUR") | EUR, GBP, AUD, NZD, USD, CAD, CHF or JPY\n FracPips | FracPips(112345) | Integer subclass for fractional pips.\n LotSize | LotSize(20000) | Integer subclass for number of units in trade.\n Pair | Pair("AUD_USD") | one of 28 forex pairs from the 8 currencies\n Price | Price("1.2342") | Decimal based representation of forex price.\n \n### Quick Example\n```python\nfrom forex_types import Pair, Currency, Price, LotSize, Calc, Direction\n\n# Details of trade:\npair = Pair.EUR_USD\nlot_size = LotSize(20000)\ndirection = Direction.LONG\nentry_price = Price("1.2223")\nexit_price = Price("1.2244")\n\n# Figuring out the profit (or loss)\nprofit = Calc.get_trade_cash(lot_size, pair.quote, direction, entry_price, exit_price)\n\nprint(f"Trade Result: {profit.nearest_cent()}")\n```\n\n### Quick note about Price class\nAlthough the `Price` class represents price, it does not know its quote\ncurrency. When constructed it determines if the price is in a Japanese Yen\nkind of range, and if so a subclass called `NinjaPrice` is returned, otherwise\nif it is in a reasonable range for other currencies a `Price` object is returned.\nIf the price is out of what is considered a reasonable range, an exception is raised.\nNote that an important difference between Japanese Yen based currencies is that\nthere are 100 pips to a Yen, but for our other currencies there are 10,000\npips per unit.\n\n\n### Disclaimers:\n1. Only the eight major currencies are supported with the resulting 28 currency\npairs. This might be expanded to include other currencies that are reasonably stable and\nwhose central banks establish a record of responsibly managing them (the CHF is\nsupported with a reluctant eye to that business with the Euro peg in 2015--but\nwith the trust they have learned their lesson).\n1. There is no plan to ever support any crypto currency. Nor is there any chain\nsaw juggling support for similar reasons.\n1. no API to any data or broker in this package. However, there is a\nseparate [oanda-candles API](https://pypi.org/project/oanda-candles/)\nthat is built on this package.\n1. The `Calc` class needs some more functionality. In particular, a function\nthat converts one currency into another given the relevant forex price.\n1. There are parts that are not covered by unit tests and are a bit rough and\nlikely to be changed in future updates.\n\n\n\n',
    'author': 'Andrew Allaire',
    'author_email': 'andrew.allaire@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aallaire/python_forex_types',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
