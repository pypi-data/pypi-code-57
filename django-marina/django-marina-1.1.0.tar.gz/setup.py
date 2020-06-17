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

extras_require = \
{'docs': ['sphinx>=2.4,<3.0', 'm2r>=0.2.1,<0.3.0']}

setup_kwargs = {
    'name': 'django-marina',
    'version': '1.1.0',
    'description': 'Django extensions by Zostera',
    'long_description': '# django-marina\n\n[![image](https://travis-ci.org/zostera/django-marina.svg?branch=main)](https://travis-ci.org/zostera/django-marina)\n[![image](https://coveralls.io/repos/github/zostera/django-marina/badge.svg?branch=main)](https://coveralls.io/github/zostera/django-marina?branch=main)\n[![Latest PyPI version](https://img.shields.io/pypi/v/django-marina.svg)](https://pypi.python.org/pypi/django-marina)\n[![Any color you like](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nDjango extensions by Zostera.\n\nDocumentation is available at <https://django-marina.readthedocs.io/>.\n',
    'author': 'Dylan Verheul',
    'author_email': 'dylan@zostera.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zostera/django-marina',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
