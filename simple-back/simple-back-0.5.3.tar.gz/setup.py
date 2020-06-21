# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_back']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'diskcache>=4.1.0,<5.0.0',
 'memoization>=0.3.1,<0.4.0',
 'numpy>=1.18.4,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pandas_market_calendars>=1.3.5,<2.0.0',
 'pandoc>=1.0.2,<2.0.0',
 'pytz>=2020.1,<2021.0',
 'requests_html>=0.10.0,<0.11.0',
 'tabulate>=0.8.7,<0.9.0',
 'yahoo_fin>=0.8.5,<0.9.0']

setup_kwargs = {
    'name': 'simple-back',
    'version': '0.5.3',
    'description': 'A backtester with minimal setup and sensible defaults.',
    'long_description': None,
    'author': 'Christoph Minixhofer',
    'author_email': 'christoph.minixhofer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
