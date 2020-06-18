# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['enciphey']
install_requires = \
['cipheycore>=0.1.5-rc.4,<0.2.0',
 'cipheydists>=0.1.3,<0.2.0',
 'unicode>=2.7,<3.0']

setup_kwargs = {
    'name': 'enciphey',
    'version': '0.1.2rc1',
    'description': 'Randomly chooses an encryption',
    'long_description': None,
    'author': 'Brandon',
    'author_email': 'brandon@skerritt.blog',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
