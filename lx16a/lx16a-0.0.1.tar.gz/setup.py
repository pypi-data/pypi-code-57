# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lx16a']

package_data = \
{'': ['*']}

install_requires = \
['construct>=2.10.56,<3.0.0', 'loguru>=0.5.0,<0.6.0', 'pyserial>=3.4,<4.0']

setup_kwargs = {
    'name': 'lx16a',
    'version': '0.0.1',
    'description': 'Python library to control the Hiwonder LX-16a digital serial servo motor.',
    'long_description': '# lx16a\n\n> THIS IS WIP!\n\nPython library to control the Hiwonder LX-16a digital serial servo motor.',
    'author': 'Phil Winder',
    'author_email': 'phil@WinderResearch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://winderresearch.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
