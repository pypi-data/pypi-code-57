# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['dqfuns', 'dqfuns.data', 'dqfuns.features', 'dqfuns.visualization']

package_data = \
{'': ['*'], 'dqfuns': ['notebooks/*']}

install_requires = \
['cognite-sdk-experimental>=0.11.1,<0.12.0',
 'cognite-sdk>=1.6.0,<2.0.0',
 'ipykernel>=5.2.1,<6.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numba==0.48.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'cognite-dqfuns',
    'version': '0.1.0',
    'description': 'Collection of python algorithms to evaluate data quality in CDF timeseries and assets',
    'long_description': None,
    'author': 'cognite',
    'author_email': 'support@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
