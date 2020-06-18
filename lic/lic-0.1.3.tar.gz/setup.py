# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lic']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'numpy>=1.18.5,<2.0.0']

entry_points = \
{'console_scripts': ['lic = lic.lic:py']}

setup_kwargs = {
    'name': 'lic',
    'version': '0.1.3',
    'description': 'Line integral convolution for numpy arrays',
    'long_description': '.. image:: https://img.shields.io/pypi/v/lic?style=flat-square   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/l/lic?style=flat-square   :alt: PyPI - License\n\n.. image:: https://img.shields.io/pypi/pyversions/lic?style=flat-square   :alt: PyPI - Python Version\n\n.. image:: https://img.shields.io/gitlab/pipeline/szs/lic?style=flat-square   :alt: Gitlab pipeline status\n\n.. image:: https://gitlab.com/szs/lic/badges/master/coverage.svg?style=flat-square   :alt: Coverage\n\nLine Integral Convolution for numpy Arrays\n==========================================\n\nThis package provides line integral convolution (lic) algorithms to Python.\n\nThere are functions which can be imported and are highly configurable for the power user.\nMoreover, there is a command line tool to generate lic images without having to code a single line.\n\nReferences\n==========\n\n* http://www.zhanpingliu.org/Research/FlowVis/FlowVis.htm\n',
    'author': 'Steffen Brinkmann',
    'author_email': 's-b@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/szs/lic/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
