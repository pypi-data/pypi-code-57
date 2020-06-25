# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gtag']

package_data = \
{'': ['*']}

install_requires = \
['guy>=0.7.2,<0.8.0']

setup_kwargs = {
    'name': 'gtag',
    'version': '0.0.27',
    'description': 'GUI toolkit for building beautiful applications for mobile, web, and desktop from a single python3 codebase',
    'long_description': '# gtag\n\n**GTag** is a GUI toolkit for building beautiful applications for mobile, web, and desktop from a single python3 codebase.\n\n[Official docs](https://gtag-docs.glitch.me/)\n',
    'author': 'manatlan',
    'author_email': 'manatlan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manatlan/guy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
