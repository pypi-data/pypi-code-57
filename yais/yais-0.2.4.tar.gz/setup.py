# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['yais']
install_requires = \
['beautifulsoup4>=4.8.1,<5.0.0',
 'imagesize>=1.1.0,<2.0.0',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['yais = yais:cli']}

setup_kwargs = {
    'name': 'yais',
    'version': '0.2.4',
    'description': 'Yet Another Image Scraper',
    'long_description': '# yais\n\nYet Another Image Scraper\n\n## Changelog\n\n### v0.2.4\n\n- Fix support for Twitter\n\n### v0.2.3\n\n- Improve support for moebooru\n\n### v0.2.2\n\n- Fix suppport for konachan site with http\n\n### v0.2.1\n\n- Fix support for pixiv urls startswith `https://pixiv.net/`\n\n### v0.2.0\n\n- Add support for tweet with multiple images. ( e.g. https://twitter.com/hunwaritoast/status/1188048064948293632 )\n- Add support for zerochan.net\n',
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtsky/yais',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
