# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glosario']

package_data = \
{'': ['*'], 'glosario': ['.github/workflows/*', 'data/*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0', 'textdistance>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'glosario',
    'version': '0.1',
    'description': 'Python package to define technical terms',
    'long_description': "## glosario\n\n[![Documentation Status](https://readthedocs.org/projects/glossary/badge/?version=latest)](https://glossary.readthedocs.io/en/latest/?badge=latest)\n\nPackage to define technical terms\n\n### Installation:\n\n```\npip install glosario\n```\n\n### Usage\n\n```\n>>> from glosario import glosario\n>>> glosario.set_language('en')\n>>> glosario.define('data frame')\n```\n\n### Features\n\n- Defines technical terms in multiple languages\n- Allows for setting multiple languages in one script (sequentially)\n- Implements cosine similarity for matching words to closest slug\n\n### Dependencies\n\n- `PyYaml`\n- `textdistance`\n\n### Documentation\n\nThe official documentation is hosted on Read the Docs: <https://glosario.readthedocs.io/en/latest/>\n\n### Credits\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n",
    'author': 'Ian Flores Siaca',
    'author_email': 'iflores.siaca@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
