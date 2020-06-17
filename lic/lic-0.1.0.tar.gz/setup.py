# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lic']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pytest-pylint>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'lic',
    'version': '0.1.0',
    'description': 'Line integral convolution for numpy arrays',
    'long_description': None,
    'author': 'Steffen Brinkmann',
    'author_email': 's-b@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
