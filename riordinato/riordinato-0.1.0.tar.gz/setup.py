# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['riordinato']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'riordinato',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Organize your files automatically just by using prefixes\n\n### example video\n\n[![asciicast](https://asciinema.org/a/ROPMams9fQwUBU5Ajo90X5ki4.svg)](https://asciinema.org/a/ROPMams9fQwUBU5Ajo90X5ki4)\n\n## install\n\n`pip3 install riordinator`\n',
    'author': 'Dan-',
    'author_email': 'misternutel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
