# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kart']

package_data = \
{'': ['*']}

install_requires = \
['feedgen>=0.9,<0.10',
 'jinja2>=2.11,<3.0',
 'livereload>=2.6,<3.0',
 'paka.cmark>=2.2,<3.0',
 'python-frontmatter>=0.5,<0.6',
 'pyyaml>=5.1,<6.0']

setup_kwargs = {
    'name': 'kart',
    'version': '0.6.0',
    'description': 'A very flexible static site generator written in python',
    'long_description': '# Kart\nA very flexible static site generator written in python\n\n# Getting started\nInstall Kart with pip\n```bash\n$ pip install Kart\n```\n\nBuild the basic strcucture\n```bash\n$ python -m kart init\n```\n\nIn this configuration Kart will only build a basic blog with a paginated blog index and paginated tags. If you want to customize the urls of the blog you will have to modify main.py with custom python code\n\n\nYou can then build and serve your site with this command\n```bash\n$ python3 main.py serve\n```\n# Disclaimer\nKart is not yet ready to use in a real-world scenario because it is in its early stage of its life and its api can change abruptly each minor verision.\n\nI am currently writing the [documentation](https://giacomocaironi.github.io/Kart) of kart but it is by no mean complete. If you want to look at some examples you can look the docs folder, where the documentation is held, and the source code of [my personal site](https://giacomocaironi.github.io) which is generated using kart\n',
    'author': 'Giacomo Caironi',
    'author_email': 'giacomo.caironi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
