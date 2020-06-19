# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dxfeed',
 'dxfeed.core',
 'dxfeed.core.listeners',
 'dxfeed.core.pxd_include',
 'dxfeed.core.utils',
 'dxfeed.wrappers']

package_data = \
{'': ['*'],
 'dxfeed': ['dxfeed-c-api/*',
            'dxfeed-c-api/include/*',
            'dxfeed-c-api/include/pthreads/*',
            'dxfeed-c-api/src/*']}

install_requires = \
['pandas>=0.25.1,<0.26.0']

extras_require = \
{'docs': ['toml>=0.10.0,<0.11.0', 'jupyter>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'dxfeed',
    'version': '0.4.0',
    'description': 'DXFeed Python API via C API',
    'long_description': "# dxfeed package\n\n[![PyPI](https://img.shields.io/pypi/v/dxfeed)](https://pypi.org/project/dxfeed/)\n[![Documentation Status](https://readthedocs.org/projects/dxfeed/badge/?version=latest)](https://dxfeed.readthedocs.io/en/latest/?badge=latest)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dxfeed)](https://pypi.org/project/dxfeed/)\n[![PyPI - Wheel](https://img.shields.io/pypi/wheel/dxfeed)](https://pypi.org/project/dxfeed/)\n[![PyPI - License](https://img.shields.io/pypi/l/dxfeed)](https://github.com/dxFeed/dxfeed-python-api/blob/master/LICENSE)\n[![Test workflow](https://github.com/dxFeed/dxfeed-python-api/workflows/Test%20package/badge.svg)](https://github.com/dxFeed/dxfeed-python-api/actions)\n\n\n\nThis package provides access to [dxFeed](https://www.dxfeed.com/) streaming data.\nThe library is build as a thin wrapper over [dxFeed C-API library](https://github.com/dxFeed/dxfeed-c-api).\nWe use [Cython](https://cython.org/) in this project as it combines flexibility, reliability and\nusability in writing C extensions.\n\nThe design of the dxfeed package allows users to write any logic related to events in python as well as \nextending lower level Cython functionality. Moreover, one may start working with the API using the default \nvalues like function arguments or a default event handler.\n\nDocumentation: [dxfeed.readthedocs.io](https://dxfeed.readthedocs.io/en/latest/)\n\nPackage distribution: [pypi.org/project/dxfeed](https://pypi.org/project/dxfeed/)\n\n## Installation\n\n**Requirements:** python >= 3.6, pandas\n\n```python\npip3 install pandas\n```\n\nInstall package via PyPI\n\n```python\npip3 install dxfeed\n``` \n\n## Basic usage\n\nFollowing steps should be performed:\n\n* Import\n* Create Endpoint\n* Create Subscription\n* Attach event handler\n* Add tickers\n* Finally close subscription and connection \n\n### Import package\n\n```python\nimport dxfeed as dx\nfrom datetime import datetime  # for timed subscription\n```\n\n### Configure and create connection with Endpoint class\nCreate instance of Endpoint class which will connect provided address. \n\n\n```python\nendpoint = dx.Endpoint('demo.dxfeed.com:7300')\n```\n\nEndpoint instance contains information about the connection, e.g. connection address or status\n\n\n```python\nprint(f'Connected address: {endpoint.address}')\nprint(f'Connection status: {endpoint.connection_status}')\n```\n\n```text\nConnected address: demo.dxfeed.com:7300\nConnection status: Connected and authorized\n```\n\n### Configure and create subscription\nYou should specify event type. For timed subscription (conflated stream) you should also provide time to start subscription from.\n\n\n```python\ntrade_sub = endpoint.create_subscription('Trade')\n```\n\n**Attach default or custom event handler** - class that process incoming events. For details about custom\nevent handler look into `CustomHandlerExample.ipynb` jupyter notebook in `exapmles` folder of this repository.\n\n\n```python\ntrade_handler = dx.DefaultHandler()\ntrade_sub = trade_sub.set_event_handler(trade_handler)\n```\n\n**Add tikers** you want to receive events for\n\n\n```python\ntrade_sub = trade_sub.add_symbols(['C', 'AAPL'])\n```\n\nFor timed subscription you may provide either datetime object or string. String might be incomplete, in \nthis case you will get warning with how your provided date parsed automatically. \n\n\n```python\ntns_sub = endpoint.create_subscription('TimeAndSale', date_time=datetime.now()) \\\n                  .add_symbols(['AMZN'])\n```\n\n\n```python\ncandle_sub = endpoint.create_subscription('Candle', date_time='2020-04-16 13:05')\ncandle_sub = candle_sub.add_symbols(['AAPL', 'MSFT'])\n```\n\nWe didn't provide subscriptions with event handlers. In such a case DefaultHandler is initiated automatically.\nOne may get it with `get_event_handler` method.\n\n```python\ntns_handler = tns_sub.get_event_handler()\ncandle_handler = candle_sub.get_event_handler()\n```\n\n#### Subscription instance properties\n\n\n```python\nprint(f'Subscription event type: {tns_sub.event_type}')\nprint(f'Subscription symbols: {candle_sub.symbols}')\n```\n\n```text\nSubscription event type: TimeAndSale\nSubscription symbols: ['AAPL', 'MSFT']\n```\n\n### Access data\nIn DefaultHandler the data is stored as deque. Its length may be configured, by default 100000 events.\n\n```python\ncandle_handler.get_list()\n```\n\n### Close connection\n\n\n```python\nendpoint.close_connection()\nprint(f'Connection status: {endpoint.connection_status}')\n```\n\n```text\nConnection status: Not connected\n```\n\n### Transform data to pandas DataFrame\n\nDefaultHandler has `get_dataframe` method, which allows you to get pandas.DataFrame object with events as rows.\n\n```python\ntrade_df = trade_handler.get_dataframe()\ntns_df = tns_handler.get_dataframe()\ncandle_df = candle_handler.get_dataframe()\n```\n",
    'author': 'Index Management Team',
    'author_email': 'im@dxfeed.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
