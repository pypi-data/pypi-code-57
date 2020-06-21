# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nio',
 'nio.client',
 'nio.crypto',
 'nio.event_builders',
 'nio.events',
 'nio.store']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.4.0,<0.5.0',
 'aiohttp>=3.6.2,<4.0.0',
 'future>=0.18.2,<0.19.0',
 'h11>=0.9.0,<0.10.0',
 'h2>=3.2.0,<4.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'logbook>=1.5.3,<2.0.0',
 'pycryptodome>=3.9.7,<4.0.0',
 'unpaddedbase64>=1.1.0,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'e2e': ['python-olm>=3.1.3,<4.0.0',
         'peewee>=3.13.2,<4.0.0',
         'cachetools>=4.0.0,<5.0.0',
         'atomicwrites>=1.3.0,<2.0.0']}

setup_kwargs = {
    'name': 'matrix-nio',
    'version': '0.14.0',
    'description': 'A Python Matrix client library, designed according to sans I/O principles.',
    'long_description': None,
    'author': 'Damir Jelić',
    'author_email': 'poljar@termina.org.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
