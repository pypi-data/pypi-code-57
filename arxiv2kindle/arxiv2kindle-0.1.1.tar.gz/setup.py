# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['arxiv2kindle']
install_requires = \
['lxml>=4.5.1', 'requests']

entry_points = \
{'console_scripts': ['arxiv2kindle = arxiv2kindle:run']}

setup_kwargs = {
    'name': 'arxiv2kindle',
    'version': '0.1.1',
    'description': 'A simple tool to recompile arxiv papers to kindle-like format.',
    'long_description': None,
    'author': 'Dmitriy Serdyuk',
    'author_email': 'dmitriy@serdyuk.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmitriy-serdyuk/arxiv2kindle',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
