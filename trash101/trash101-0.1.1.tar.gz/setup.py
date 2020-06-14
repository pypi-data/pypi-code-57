# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trash101']

package_data = \
{'': ['*']}

install_requires = \
['xattr>=0.9.7,<0.10.0']

entry_points = \
{'console_scripts': ['putback = trash101.putback:main',
                     'trash = trash101.trash:main']}

setup_kwargs = {
    'name': 'trash101',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
