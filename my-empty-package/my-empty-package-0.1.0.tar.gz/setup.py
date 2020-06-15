# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['my_empty_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'my-empty-package',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Orlando Diaz',
    'author_email': 'orlandodiaz.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
