# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_awesome']

package_data = \
{'': ['*']}

install_requires = \
['flake8',
 'flake8-annotations-complexity',
 'flake8-bandit',
 'flake8-breakpoint',
 'flake8-bugbear',
 'flake8-builtins',
 'flake8-comprehensions',
 'flake8-eradicate',
 'flake8-expression-complexity',
 'flake8-if-expr',
 'flake8-isort',
 'flake8-logging-format',
 'flake8-print',
 'flake8-pytest',
 'flake8-pytest-style',
 'flake8-requirements',
 'flake8-return',
 'pep8-naming']

setup_kwargs = {
    'name': 'flake8-awesome',
    'version': '1.3.0',
    'description': 'Flake8 awesome plugins pack',
    'long_description': "# flake8-awesome\n\n[![pypi](https://badge.fury.io/py/flake8-awesome.svg)](https://pypi.org/project/flake8-awesome)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-awesome)\n[![Downloads](https://img.shields.io/pypi/dm/flake8-awesome.svg)](https://pypistats.org/packages/flake8-awesome)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n\nFlake8 awesome plugins pack.\n\n## Installation\n\n```bash\npip install flake8-awesome\n```\n\nvs\n\n```bash\npip install flake8 flake8-builtins flake8-comprehensions flake8-eradicate # etc.\n```\n\n## Example of Flake8 config\n\n```ini\n[flake8]\nenable-extensions = G\nexclude = .git, .venv\nignore =\n    A003 ; 'id' is a python builtin, consider renaming the class attribute\n    W503 ; line break before binary operator\n    S101 ; use of assert detected (useless with pytest)\nmax-complexity = 8\nmax-annotations-complexity = 3\nmax-expression-complexity = 7\nmax-line-length = 120\nshow-source = true\n```\n\n## List of plugins\n\n* flake8-annotations-complexity\n* flake8-bandit\n* flake8-breakpoint\n* flake8-bugbear\n* flake8-builtins\n* flake8-comprehensions\n* flake8-eradicate\n* flake8-expression-complexity\n* flake8-if-expr\n* flake8-isort\n* flake8-logging-format\n* flake8-print\n* flake8-pytest\n* flake8-pytest-style\n* flake8-requirements\n* flake8-return\n* pep8-naming\n",
    'author': 'Afonasev Evgeniy',
    'author_email': 'ea.afonasev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/flake8-awesome',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
