# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymonad', 'pymonad.operators']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'boxx-pymonad',
    'version': '0.2.0',
    'description': 'My Implementation of pymonad package.',
    'long_description': '============\nboxx-pymonad\n============\n\n\n.. image:: https://img.shields.io/pypi/v/boxx_pymonad.svg\n        :target: https://pypi.python.org/pypi/boxx_pymonad\n\n.. image:: https://img.shields.io/travis/wboxx1/boxx-pymonad.svg\n        :target: https://travis-ci.org/wboxx1/boxx-pymonad\n\n.. image:: https://ci.appveyor.com/api/projects/status/wboxx1/branch/master?svg=true\n    :target: https://ci.appveyor.com/project/wboxx1/boxx-pymonad/branch/master\n    :alt: Build status on Appveyor\n\n.. image:: https://readthedocs.org/projects/boxx-pymonad/badge/?version=latest\n        :target: https://boxx-pymonad.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nMy Implementation of pymonad package.\n\n\n* Free software: MIT license\n\n* Documentation: https://wboxx1.github.io/boxx-pymonad\n\n\n\nInstallation:\n-------------\n\n.. code-block:: console\n\n    $ pip install boxx-pymonad\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage-poetry`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`wboxx1/cookiecutter-pypackage-poetry`: https://github.com/wboxx1/cookiecutter-pypackage-poetry\n',
    'author': 'Will Boxx',
    'author_email': 'wboxx1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wboxx1.github.io/boxx-pymonad',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
