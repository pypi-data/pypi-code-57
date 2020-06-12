# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_whirlwind']

package_data = \
{'': ['*']}

install_requires = \
['tornado>=6.0.4,<7.0.0']

entry_points = \
{'console_scripts': ['pytest-whirlwind = pytest-whirlwind.__main__:main']}

setup_kwargs = {
    'name': 'pytest-whirlwind',
    'version': '0.1.0',
    'description': 'Testing Tornado.',
    'long_description': 'pytest-whirlwind\n################\n\n.. image:: https://travis-ci.org/supakeen/pytest-whirlwind.svg?branch=master\n    :target: https://travis-ci.org/supakeen/pytest-whirlwind\n\n.. image:: https://readthedocs.org/projects/pytest-whirlwind/badge/?version=latest\n    :target: https://pytest-whirlwind.readthedocs.io/en/latest/\n\n.. image:: https://pytest-whirlwind.readthedocs.io/en/latest/_static/license.svg\n    :target: https://github.com/supakeen/pytest-whirlwind/blob/master/LICENSE\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://img.shields.io/pypi/v/pytest-whirlwind\n    :target: https://pypi.org/project/pytest-whirlwind\n\n.. image:: https://codecov.io/gh/supakeen/pytest-whirlwind/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/supakeen/pytest-whirlwind\n',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supakeen/pytest-whirlwind',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
