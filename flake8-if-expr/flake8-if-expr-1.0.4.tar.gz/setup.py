# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_if_expr']

package_data = \
{'': ['*']}

install_requires = \
['flake8-plugin-utils>=1.0,<2.0']

entry_points = \
{'flake8.extension': ['IF100 = flake8_if_expr:IfExprPlugin']}

setup_kwargs = {
    'name': 'flake8-if-expr',
    'version': '1.0.4',
    'description': 'The plugin checks `if expressions` (ternary operator)',
    'long_description': '# flake8-if-expr\n\n[![pypi](https://badge.fury.io/py/flake8-if-expr.svg)](https://pypi.org/project/flake8-if-expr)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-if-expr)\n[![Downloads](https://img.shields.io/pypi/dm/flake8-if-expr.svg)](https://pypistats.org/packages/flake8-if-expr)\n![CI Status](https://github.com/afonasev/flake8-if-expr/workflows/ci/badge.svg?branch=master)\n[![Code coverage](https://codecov.io/gh/afonasev/flake8-if-expr/branch/master/graph/badge.svg)](https://codecov.io/gh/afonasev/flake8-if-expr)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n## Description\n\nThe plugin forbids `if expressions` (ternary operator).\n\n## Installation\n\n```bash\npip install flake8-if-expr\n```\n\n## Examples\n\n```python\n# code.py\nx = 1 if 2 else 3\n```\n\n```bash\n$ flake8 code.py\n./code.py:1:5: KEK100 don`t use "[on_true] if [expression] else [on_false]" syntax\nx = 1 if 2 else 3\n    ^\n```\n',
    'author': 'Afonasev Evgeniy',
    'author_email': 'ea.afonasev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/flake8-if-expr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
