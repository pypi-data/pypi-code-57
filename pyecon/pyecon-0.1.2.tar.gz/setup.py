# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyecon']

package_data = \
{'': ['*']}

install_requires = \
['pyfan>=0.1.37,<0.2.0']

setup_kwargs = {
    'name': 'pyecon',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Fan Wang',
    'author_email': 'wangfanbsg75@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
