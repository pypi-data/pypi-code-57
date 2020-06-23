# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interrofont']

package_data = \
{'': ['*']}

install_requires = \
['fonttools']

entry_points = \
{'console_scripts': ['interrofont = entry:main']}

setup_kwargs = {
    'name': 'interrofont',
    'version': '0.1.1',
    'description': 'Interrogate a font file',
    'long_description': None,
    'author': 'Simon Cozens',
    'author_email': 'simon@simon-cozens.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
