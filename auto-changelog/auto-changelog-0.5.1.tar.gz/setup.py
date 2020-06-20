# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_changelog']

package_data = \
{'': ['*'], 'auto_changelog': ['templates/*']}

install_requires = \
['Click>=7.0,<8.0',
 'docopt>=0.6.2,<0.7.0',
 'gitpython>=2.1',
 'jinja2>=2.10,<3.0']

entry_points = \
{'console_scripts': ['auto-changelog = auto_changelog.__main__:main']}

setup_kwargs = {
    'name': 'auto-changelog',
    'version': '0.5.1',
    'description': 'Simple tool to generate nice, formatted changelogs from vcs',
    'long_description': 'Auto Changelog\n==============\n\n|ci| |pypi| |version| |licence| |black|\n\n.. |ci| image:: https://gitlab.com/KeNaCo/auto-changelog-ci-test/badges/master/pipeline.svg\n   :target: https://gitlab.com/KeNaCo/auto-changelog-ci-test/commits/master\n   :alt: CI Pipeline\n.. |pypi| image:: https://img.shields.io/pypi/v/auto-changelog\n   :target: https://pypi.org/project/auto-changelog/\n   :alt: PyPI\n.. |version| image:: https://img.shields.io/pypi/pyversions/auto-changelog\n   :alt: PyPI - Python Version\n.. |licence| image:: https://img.shields.io/pypi/l/auto-changelog\n   :alt: PyPI - License\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :alt: Code style - Black\n\nA quick script that will generate a changelog for any git repository using `conventional style`_ commit messages.\n\nInstallation\n------------\n\nInstall and update using `pip`_:\n\n.. code-block:: text\n\n    pip install auto-changelog\n\nor directly from source(via poetry):\n\n.. code-block:: text\n\n    poetry install\n    poetry build\n    pip install dist/*.whl\n\nA simple example\n----------------\n\n.. image:: example-usage.gif\n   :alt: Example usage of auto-changelog\n\nContributing\n------------\n\nTo setup development environment, you may use `Poetry`_:\n\n.. code-block:: text\n\n    poetry install\n\nTo activate virtualenv:\n\n.. code-block:: text\n\n    poetry shell\n\nTo run tests:\n\n.. code-block:: text\n\n    pytest\n\nFor consistent formatting, you may use `Black`_:\n\n.. code-block:: text\n\n    black .\n\n.. note::\n\n    Instead of manual run of black tool, you can consider using `Pre-commit`_.\n\n.. _Black: https://black.readthedocs.io/en/stable/\n.. _conventional style: https://www.conventionalcommits.org/en\n.. _pip: https://pip.pypa.io/en/stable/quickstart/\n.. _Poetry: https://poetry.eustace.io/\n.. _Pre-commit: https://pre-commit.com/\n',
    'author': 'Michael F Bryan',
    'author_email': 'michaelfbryan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Michael-F-Bryan/auto-changelog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
