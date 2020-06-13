# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdfl', 'mdfl.parser']

package_data = \
{'': ['*'],
 'mdfl': ['templates/function/*',
          'templates/function/{{ cookiecutter.name }}.function/*',
          'templates/pack/*',
          'templates/pack/{{ cookiecutter.name }}/*']}

install_requires = \
['cookiecutter>=1.7.2,<2.0.0',
 'docopt>=0.6.2,<0.7.0',
 'lark-parser>=0.8.6,<0.9.0']

entry_points = \
{'console_scripts': ['mdfl = mdfl:main']}

setup_kwargs = {
    'name': 'mdfl',
    'version': '0.1.3',
    'description': 'A prototype command-line tool for creating datapacks.',
    'long_description': None,
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
