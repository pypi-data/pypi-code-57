# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blc', 'blc.handlers']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'pendulum>=2.1.0,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'rich>=1.3.1,<2.0.0',
 'tinydb>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'blc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dimitrios Strantsalis',
    'author_email': 'dstrants@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
