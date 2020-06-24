# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formaldict', 'formaldict.tests']

package_data = \
{'': ['*']}

install_requires = \
['kmatch>=0.3.0,<0.4.0',
 'prompt-toolkit>=3.0.2,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'formaldict',
    'version': '0.2.1',
    'description': 'Formal structured dictionaries parsed from a schema',
    'long_description': 'formaldict\n########################################################################\n\nDocumentation\n=============\n\n`View the formaldict docs here\n<https://formaldict.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall formaldict with::\n\n    pip3 install formaldict\n\n\nContributing Guide\n==================\n\nFor information on setting up formaldict for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n',
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/formaldict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
