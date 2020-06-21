# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glovo_api_python', 'glovo_api_python.constants', 'glovo_api_python.resources']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'glovo-api-python',
    'version': '2.0.0',
    'description': '',
    'long_description': None,
    'author': 'SoftButterfly Development Team',
    'author_email': 'dev@softbutterfly.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
