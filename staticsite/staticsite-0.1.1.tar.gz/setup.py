# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['staticsite']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'htmlmin>=0.1.12,<0.2.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'staticsite',
    'version': '0.1.1',
    'description': 'Super simple Jinja2 based staticsite generator.',
    'long_description': '# StaticSite\n\nSuper simple static site builder.\n\n1. Create a folder called `src` (or spcify `--src` on CLI)\n2. Put your files there.\n3. `python -m staticsite`\n4. Find your built site in `docs` (or specify `--target` on CLI)\n',
    'author': 'arjoonn sharma',
    'author_email': 'arjoonn.94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://thesage21.github.io/staticsite/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
