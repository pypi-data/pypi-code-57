# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['arxiv2kindle']
install_requires = \
['arxiv>=0.5.3,<0.6.0', 'requests']

entry_points = \
{'console_scripts': ['arxiv2kindle = arxiv2kindle:run']}

setup_kwargs = {
    'name': 'arxiv2kindle',
    'version': '0.1.3',
    'description': 'A simple tool to recompile arxiv papers to kindle-like format.',
    'long_description': '# arxiv2kindle\n\nA simple script to recompile arxiv papers to kindle-like format.\n\n## How does it work?\n\nThis script downloads the LaTeX source from arxiv \nand re-compiles it trying to fit a smaller size.\nWe also apply some simple transforms such as:\n- downsize images;\n- add automatic line breaks in formulas;\n- allow formulas be placed on the next line;\n- try to convert two-sided documents to one-sided format.\n\nAll these transformations are automatic, so the success is not guaranteed.\nThis approach will also not work for papers without the source.\nNevertheless, in most cases the result is readable \n(tested on an old 6.5in x 4.5in Kindle).\n\n\n## Usage\n\nWith your paper of choice run:\n```\narxiv2kindle --width 4 --height 6 --margin 0.2 1802.08395 - > out.pdf\n```\nor \n```\narxiv2kindle --width 6 --height 4 --margin 0.2 --landscape "Towards end-to-end spoken language understanding" ./\n```\n\n## Installation\n\n`arxiv2kindle` requires `pip` version 10.0 or greater. \n\nTo install the package, run\n```\npip install arxiv2kindle\n```\n\n## Acknowledgements\n\nThis script is based on this amazing [notebook](https://gist.github.com/bshillingford/6259986edca707ca58dd).\n\n## Related projects\n\n- https://github.com/cerisara/arxiv2kindle\n- https://knanagnostopoulos.blogspot.com/2013/03/from-arxiv-directly-to-my-kindle_15.html\n- https://dlmf.nist.gov/LaTeXML/',
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
