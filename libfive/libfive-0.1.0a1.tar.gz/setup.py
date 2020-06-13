# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libfive']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libfive',
    'version': '0.1.0a1',
    'description': 'libfive bindings for Python',
    'long_description': '# libfive-python\n\nThis is a work in progress Python library for using [libfive](https://libfive.com/) from Python.\n',
    'author': 'Sem Mulder',
    'author_email': 'sem@mulderke.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SemMulder/libfive-python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
