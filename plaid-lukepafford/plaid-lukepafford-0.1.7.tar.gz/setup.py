# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plaid_lukepafford']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.5,<2.0.0',
 'plaid-python>=4.1.0,<5.0.0',
 'pytest>=5.4.3,<6.0.0',
 'typer>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['chase-plaid = plaid_lukepafford.main:app']}

setup_kwargs = {
    'name': 'plaid-lukepafford',
    'version': '0.1.7',
    'description': '',
    'long_description': "# plaid_lukepafford\n\nUses Plaid to instantiate a Chase connection and save transaction data\nlocally.\n\nGraphs and summaries will be built that I find interesting.\n\nMain object is at `plaid_lukepafford.transactions.ChaseTransactions`\n\n# Install\n\n### Install package\n`pip install plaid_lukepafford`\n\n### Fetch transactions from Plaid API. (This will fail if you don't provide correct environment variables)\n`chase-plaid fetch-latest-transactions`\n\n### Display a table summarizing results\n`chase-plaid money-spent-on-food`\n```\n",
    'author': 'Luke Pafford',
    'author_email': 'lukepafford@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
