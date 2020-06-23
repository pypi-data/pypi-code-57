# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ortoolpy', 'ortoolpy.optimization']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.2.0,<9.0.0', 'pandas>=1.0.3,<2.0.0', 'pulp>=2.1,<3.0']

setup_kwargs = {
    'name': 'ortoolpy',
    'version': '0.2.35',
    'description': '`ortoolpy` is a package for Operations Research.',
    'long_description': "`ortoolpy` is a package for Operations Research.\nIt is user's responsibility for the use of `ortoolpy`.\n\n::\n\n   from ortoolpy import knapsack\n   size = [21, 11, 15, 9, 34, 25, 41, 52]\n   weight = [22, 12, 16, 10, 35, 26, 42, 53]\n   capacity = 100\n   knapsack(size, weight, capacity)\n\nRequirements\n------------\n* Python 3, numpy, pandas, matplotlib, networkx, pulp, more-itertools, ortools\n\nFeatures\n--------\n* This is a sample. So it may not be efficient.\n* `ortools_vrp` using Google OR-Tools ( https://developers.google.com/optimization/ ).\n\nSetup\n-----\n::\n\n   $ pip install ortoolpy\n\nHistory\n-------\n0.0.1 (2015-6-26)\n~~~~~~~~~~~~~~~~~~\n* first release\n",
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/ortoolpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
