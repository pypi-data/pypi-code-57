# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['clitw']
install_requires = \
['fire>=0.3.1,<0.4.0', 'tweepy>=3.8.0,<4.0.0']

entry_points = \
{'console_scripts': ['clitw = clitw:main']}

setup_kwargs = {
    'name': 'clitw',
    'version': '0.0.7',
    'description': 'CUI Twitter Client on Python',
    'long_description': 'tamatebako\n==========\n\n::\n\n   pip install tamatebako\n   tw\n',
    'author': 'Daisuke Oku',
    'author_email': 'w.40141@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/w40141',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
