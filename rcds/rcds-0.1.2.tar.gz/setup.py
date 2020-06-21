# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rcds',
 'rcds.backend',
 'rcds.backends',
 'rcds.backends.k8s',
 'rcds.backends.rctf',
 'rcds.challenge',
 'rcds.cli',
 'rcds.project',
 'rcds.util']

package_data = \
{'': ['*'], 'rcds.backends.k8s': ['templates/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'docker>=4.2.1,<5.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'kubernetes>=11.0.0,<12.0.0',
 'pathspec>=0.8.0,<0.9.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.23.0,<3.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['rcds = rcds.cli:cli']}

setup_kwargs = {
    'name': 'rcds',
    'version': '0.1.2',
    'description': 'An automated CTF challenge deployment tool',
    'long_description': "#######\nrCDS\n#######\n\n.. image:: https://github.com/redpwn/rCDS/workflows/CI/badge.svg\n    :target: https://github.com/redpwn/rCDS/actions?query=workflow%3ACI+branch%3Amaster\n    :alt: CI Status\n\n.. image:: https://img.shields.io/codecov/c/gh/redpwn/rcds\n    :target: https://codecov.io/gh/redpwn/rCDS\n    :alt: Coverage\n\nrCDS is RedpwnCTF's automated challenge management and deployment tool. It is\ndeveloped and maintained by the `redpwn <https://redpwn.net>`_ CTF team.\n",
    'author': 'redpwn',
    'author_email': 'contact@redpwn.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rcds.redpwn.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
