# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desdeo']

package_data = \
{'': ['*']}

install_requires = \
['desdeo-mcdm>=0.1.3,<0.2.0',
 'desdeo-problem>=0.15.0,<0.16.0',
 'desdeo-tools>=0.2.6,<0.3.0']

setup_kwargs = {
    'name': 'desdeo',
    'version': '1.0',
    'description': 'Open source framework for interactive multiobjective optimization.',
    'long_description': None,
    'author': 'Giovanni Misitano',
    'author_email': 'giovanni.a.misitano@jyu.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
