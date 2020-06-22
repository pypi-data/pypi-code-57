# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['squashblame']
install_requires = \
['click>=7.0,<8.0', 'gitpython>=3.0.3,<4.0.0']

entry_points = \
{'console_scripts': ['git-squash-blame = squashblame:squash_blame']}

setup_kwargs = {
    'name': 'git-squash-blame',
    'version': '0.1.0',
    'description': 'Squash git history while preserving blame',
    'long_description': 'Squash git history while preserving blame',
    'author': 'Evan Grim',
    'author_email': 'evan@mirgnave.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/egrim/git-squash-blame',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
