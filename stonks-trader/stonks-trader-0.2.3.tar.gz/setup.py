# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stonks_trader',
 'stonks_trader.cli',
 'stonks_trader.helpers',
 'stonks_trader.trade_strategies']

package_data = \
{'': ['*']}

install_requires = \
['click-spinner==0.1.10',
 'matplotlib',
 'numpy',
 'pandas',
 'pandas-ta==0.1.39b',
 'pytse_client',
 'requests',
 'ta',
 'typer']

entry_points = \
{'console_scripts': ['stonks-trader = stonks_trader.cli.cli_app:app']}

setup_kwargs = {
    'name': 'stonks-trader',
    'version': '0.2.3',
    'description': '',
    'long_description': None,
    'author': 'glyphack',
    'author_email': 'sh.hooshyari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
