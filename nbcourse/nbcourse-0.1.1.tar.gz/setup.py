# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbcourse']

package_data = \
{'': ['*']}

install_requires = \
['IPython>=7.15.0,<8.0.0',
 'bookbook>=0.2,<0.3',
 'bs4>=0.0.1,<0.0.2',
 'doit>=0.32.0',
 'jinja2>=2.11.2,<3.0.0',
 'jupyter_contrib_nbextensions>=0.5.1,<0.6.0',
 'latex>=0.7.0,<0.8.0',
 'markdown>=3.2.2,<4.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'pyyaml>=5.3.1,<6.0.0',
 'rise>=5.6.1,<6.0.0']

entry_points = \
{'console_scripts': ['nbcourse = nbcourse:main']}

setup_kwargs = {
    'name': 'nbcourse',
    'version': '0.1.1',
    'description': 'Create a minisite to publish a course based on Jupyter notebooks',
    'long_description': None,
    'author': 'Matthieu Boileau',
    'author_email': 'matthieu.boileau@math.unistra.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.math.unistra.fr/boileau/nbcourse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
