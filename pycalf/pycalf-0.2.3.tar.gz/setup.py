# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycalf']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'pycalf',
    'version': '0.2.3',
    'description': '',
    'long_description': None,
    'author': 'konumaru',
    'author_email': 'konumaru1022@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
