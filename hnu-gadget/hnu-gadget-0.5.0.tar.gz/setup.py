# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hnu_gadget']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['hnu-gadget = hnu_gadget.__main__:main']}

setup_kwargs = {
    'name': 'hnu-gadget',
    'version': '0.5.0',
    'description': '',
    'long_description': '',
    'author': 'renantamashiro',
    'author_email': 'tamashirorenan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/renantamashiro/hnu-gadget',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
