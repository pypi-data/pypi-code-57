# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['arxiv2kindle']
install_requires = \
['lxml>=4.5.1,<5.0.0', 'requests']

entry_points = \
{'console_scripts': ['arxiv2kindle = arxiv2kindle:run']}

setup_kwargs = {
    'name': 'arxiv2kindle',
    'version': '0.1.2',
    'description': 'A simple tool to recompile arxiv papers to kindle-like format.',
    'long_description': '# arxiv2kindle\n\nA simple script to recompile arxiv papers to kindle-like format.\n\n## Usage\n\nWith your paper of choice run:\n```\narxiv2kindle --width 4 --height 6 --margin 0.2 https://arxiv.org/abs/1802.08395 > out.pdf\n```\nor \n```\narxiv2kindle --width 6 --height 4 --margin 0.2 --landscape --dest-dir ./ https://arxiv.org/abs/1802.08395\n```\n\n## Installation\n\n`arxiv2kindle` requires `pip` version 10.0 or greater. \n\n## Acknowledgements\n\nThis script is based on this amazing [notebook](https://gist.github.com/bshillingford/6259986edca707ca58dd).',
    'author': 'Dmitriy Serdyuk',
    'author_email': 'dmitriy@serdyuk.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmitriy-serdyuk/arxiv2kindle',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
