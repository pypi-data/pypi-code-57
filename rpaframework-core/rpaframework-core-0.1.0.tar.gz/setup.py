# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['RPA', 'RPA.core']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141.0,<4.0.0']

extras_require = \
{':python_version < "3.7.6" and sys_platform == "win32" or python_version > "3.7.6" and python_version < "3.8.1" and sys_platform == "win32" or python_version > "3.8.1" and sys_platform == "win32"': ['pywin32>=227,<228']}

setup_kwargs = {
    'name': 'rpaframework-core',
    'version': '0.1.0',
    'description': 'Core utilities used by rpaframework',
    'long_description': 'rpaframework-core\n=================\n\nThis package is a set of core functionality and utilities used\nby `RPA Framework`_. It is not intended to be installed directly, but\nas a dependency to other projects.\n\n.. _RPA Framework: https://rpaframework.org\n',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rpaframework.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
