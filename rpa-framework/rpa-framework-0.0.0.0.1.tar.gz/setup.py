# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpa_framework']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rpa-framework',
    'version': '0.0.0.0.1',
    'description': 'Deprecated project. Current project is rpaframework.',
    'long_description': 'Introduction\n------------\n\n**DEPRECATED**\n\nCurrent project at https://pypi.org/project/rpaframework/',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
