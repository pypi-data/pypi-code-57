# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bootstrap3', 'bootstrap3.templatetags']

package_data = \
{'': ['*'], 'bootstrap3': ['templates/bootstrap3/*']}

install_requires = \
['django>=2.2,<4.0']

extras_require = \
{'docs': ['sphinx>=2.4,<3.0',
          'sphinx_rtd_theme>=0.4.3,<0.5.0',
          'm2r>=0.2.1,<0.3.0']}

setup_kwargs = {
    'name': 'django-bootstrap3',
    'version': '14.0.0',
    'description': 'Bootstrap 3 support for Django projects',
    'long_description': '# django-bootstrap3\n\n[![Build](https://travis-ci.org/zostera/django-bootstrap3.svg?branch=main)](https://travis-ci.org/zostera/django-bootstrap3)\n[![Coverage Status](https://coveralls.io/repos/github/zostera/django-bootstrap3/badge.svg?branch=main)](https://coveralls.io/github/zostera/django-bootstrap3?branch=main)\n[![Latest PyPI version](https://img.shields.io/pypi/v/django-bootstrap3.svg)](https://pypi.python.org/pypi/django-bootstrap3)\n[![Any color you like](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nBootstrap 3 integration for Django.\n\n## Goal\n\nThe goal of this project is to seamlessly blend Django and Bootstrap 3.\n\nWant to use Bootstrap 4 in Django? See https://github.com/zostera/django-bootstrap4.\n\n## Requirements\n\nDjango 2.2 or 3.0 with Python 3.6 or higher.\n\n## Documentation\n\nThe full documentation is at https://django-bootstrap3.readthedocs.io/\n\n## Installation\n\n1. Install using pip:\n\n    ```shell script\n    pip install django-bootstrap3\n    ```\n   \n   Alternatively, you can install download or clone this repo and call ``pip install -e .``.\n\n2. Add to `INSTALLED_APPS` in your `settings.py`:\n\n   ```python\n   INSTALLED_APPS = (\n       # ...\n       "bootstrap3",\n       # ...\n   )\n   ````\n\n3. In your templates, load the `bootstrap3` library and use the `bootstrap_*` tags:\n\n## Example template\n\n```djangotemplate\n{% load bootstrap3 %}\n\n{# Display a form #}\n\n<form action="/url/to/submit/" method="post" class="form">\n    {% csrf_token %}\n    {% bootstrap_form form %}\n    {% buttons %}\n        <button type="submit" class="btn btn-primary">Submit</button>\n    {% endbuttons %}\n</form>\n```\n\nDemo\n----\n\nA demo app is provided in `demo`. You can run it from your virtualenv with `python manage.py runserver`.\n\n\nBugs and suggestions\n--------------------\n\nIf you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.\n\nhttps://github.com/zostera/django-bootstrap3/issues\n\n\nLicense\n-------\n\nYou can use this under BSD-3-Clause. See [LICENSE](LICENSE) file for details.\n\n\nAuthor\n------\n\nDeveloped and maintained by [Zostera](https://zostera.nl).\n\nOriginal author: [Dylan Verheul](https://github.com/dyve).\n\nThanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.\n\nPlease see [AUTHORS.md](AUTHORS.md) for a list of contributors.\n',
    'author': 'Dylan Verheul',
    'author_email': 'dylan@zostera.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zostera/django-bootstrap3',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
