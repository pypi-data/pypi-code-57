# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arg', 'arg.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-args',
    'version': '1.0.0',
    'description': 'Python argument design patterns in a composable interface.',
    'long_description': 'python-args\n########################################################################\n\nDocumentation\n=============\n\n`View the python-args docs here\n<https://python-args.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall python-args with::\n\n    pip3 install python-args\n\n\nContributing Guide\n==================\n\nFor information on setting up python-args for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n',
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/python-args',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
