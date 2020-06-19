# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bananopy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'bananopy',
    'version': '0.3.1',
    'description': 'Python library for interaction with Banano',
    'long_description': '===============================\n🍌\U0001f967: Banano Python Library\n===============================\n\n.. image:: https://img.shields.io/pypi/l/bananopy.svg\n    :target: https://github.com/milkyklim/bananopy/blob/master/LICENSE\n    :alt: License\n\n.. image:: https://github.com/milkyklim/bananopy/workflows/CI/badge.svg\n    :target: https://github.com/milkyklim/bananopy/actions\n    :alt: Build Status\n\n.. image:: https://readthedocs.org/projects/bananopy/badge/?version=latest\n    :target: http://bananopy.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/pyversions/bananopy.svg\n    :target: https://pypi.python.org/pypi/\n    :alt: Supported Python Versions\n\n.. image:: https://img.shields.io/pypi/v/bananopy.svg\n    :target: https://pypi.python.org/pypi/bananopy\n    :alt: Package Version\n\n.. image:: https://img.shields.io/badge/Banano%20Node-v20.0-yellow\n    :alt: Banano Node Version\n\n🍌\U0001f967 is a python wrapper for Banano node communication.\nIt takes care of RPC responses (type conversions) and exposes a pythonic API for making RPC calls.\n\nFull list of RPC calls is coming from `docs <https://docs.nano.org/commands/rpc-protocol/>`_.\n',
    'author': 'milkyklim',
    'author_email': '10698619+milkyklim@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/milkyklim/bananopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
