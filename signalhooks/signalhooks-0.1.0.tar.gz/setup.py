# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['signalhooks']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2', 'boto3>=1.14', 'requests>=2.23']

setup_kwargs = {
    'name': 'signalhooks',
    'version': '0.1.0',
    'description': 'Set of useful hooks that you can attach to your Django Signals to notify other services when a Signal is triggered',
    'long_description': None,
    'author': 'Martin Zugnoni',
    'author_email': 'martin.zugnoni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
