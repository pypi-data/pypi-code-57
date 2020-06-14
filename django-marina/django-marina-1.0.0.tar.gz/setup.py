# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_marina', 'django_marina.db', 'django_marina.test']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8.0,<5.0.0', 'django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-marina',
    'version': '1.0.0',
    'description': 'Django extensions by Zostera',
    'long_description': '# django-marina\n\n[![image](https://travis-ci.org/zostera/django-marina.svg?branch=master)](https://travis-ci.org/zostera/django-marina)\n[![image](https://coveralls.io/repos/github/zostera/django-marina/badge.svg?branch=develop)](https://coveralls.io/github/zostera/django-marina?branch=develop)\n[![Latest PyPI version](https://img.shields.io/pypi/v/django-marina.svg)](https://pypi.python.org/pypi/django-marina)\n[![Any color you like](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nDjango extensions by Zostera. Use at your own leisure and peril.\n\nDocumentation is available at <https://django-marina.readthedocs.io/>.\n',
    'author': 'Dylan Verheul',
    'author_email': 'dylan@zostera.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zostera/django-marina',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
