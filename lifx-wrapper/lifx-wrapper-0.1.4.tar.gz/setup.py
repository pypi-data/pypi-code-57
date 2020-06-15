# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': '.'}

packages = \
['lifx']

package_data = \
{'': ['*']}

install_requires = \
['black>=18.3-alpha.0,<19.0',
 'mypy>=0.770,<0.771',
 'pydantic>=1.5.1,<2.0.0',
 'pytest>=5.4,<6.0',
 'requests>=2.23.0,<3.0.0',
 'responses>=0.10.14,<0.11.0',
 'sphinx>=3.0,<4.0',
 'sphinx_autodoc_typehints>=1.10,<2.0',
 'typing_extensions>=3.7,<4.0']

setup_kwargs = {
    'name': 'lifx-wrapper',
    'version': '0.1.4',
    'description': 'A python wrapper for the Lifx REST API',
    'long_description': None,
    'author': 'Harry Cooper',
    'author_email': 'harry.coop99@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
