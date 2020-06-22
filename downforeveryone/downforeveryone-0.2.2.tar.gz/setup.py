# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['downforeveryone']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['isup = downforeveryone.isup:main']}

setup_kwargs = {
    'name': 'downforeveryone',
    'version': '0.2.2',
    'description': 'checks if a website is really down via isup.me',
    'long_description': "downforeveryone\n======================\n|LANGUAGE| |VERSION| |STYLE| |LICENSE| |CIRCLECI| |COVERAGE| |MAINTAINABILITY| |MAINTAINED|\n\n.. |CIRCLECI| image:: https://img.shields.io/circleci/build/gh/rpdelaney/downforeveryone\n   :target: https://circleci.com/gh/rpdelaney/downforeveryone/tree/master\n.. |LICENSE| image:: https://img.shields.io/badge/license-Apache%202.0-informational\n   :target: https://www.apache.org/licenses/LICENSE-2.0.txt\n.. |MAINTAINED| image:: https://img.shields.io/maintenance/yes/2020?logoColor=informational\n.. |VERSION| image:: https://img.shields.io/pypi/v/downforeveryone\n   :target: https://pypi.org/project/downforeveryone\n.. |STYLE| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n.. |LANGUAGE| image:: https://img.shields.io/pypi/pyversions/downforeveryone\n.. |COVERAGE| image:: https://img.shields.io/codeclimate/coverage/rpdelaney/downforeveryone\n   :target: https://codeclimate.com/github/rpdelaney/downforeveryone\n.. |MAINTAINABILITY| image:: https://img.shields.io/codeclimate/maintainability-percentage/rpdelaney/downforeveryone\n   :target: https://codeclimate.com/github/rpdelaney/downforeveryone\n\nChecks if a website is down for everyone or just you, via isup.me.\n\nInstallation\n------------\n\n::\n\n    pip3 install downforeveryone\n\n============\nDevelopment\n============\n\nTo install development dependencies, you will need `poetry <https://docs.pipenv.org/en/latest/>`_\nand `pre-commit <https://pre-commit.com/>`_.\n\n::\n\n    poetry install\n    pre-commit install --install-hooks\n\nUsage\n-----\n\n::\n\n    $ isup -h\n    usage: isup [-h] url\n\n    checks if a site is down for everyone or just you\n\n    positional arguments:\n    url         url to test\n\n    optional arguments:\n    -h, --help  show this help message and exit\n    $ isup google.com ; echo $?\n    just you.\n    1\n    $ isup thingthatsdown.com ; echo $?\n    it's down.\n    0\n",
    'author': 'Ryan Delaney',
    'author_email': 'ryan.delaney@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/downforeveryone',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
