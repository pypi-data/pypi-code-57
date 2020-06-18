# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antsibull',
 'antsibull.cli',
 'antsibull.cli.doc_commands',
 'antsibull.data',
 'antsibull.data.docsite',
 'antsibull.docs_parsing',
 'antsibull.jinja2',
 'antsibull.schemas',
 'antsibull.utils',
 'antsibull.vendored',
 'tests',
 'tests.functional.schema',
 'tests.units']

package_data = \
{'': ['*'],
 'antsibull.data': ['debian/*'],
 'tests.functional.schema': ['good_data/*']}

install_requires = \
['PyYAML',
 'aiofiles',
 'aiohttp',
 'antsibull-changelog',
 'asyncio-pool',
 'docutils',
 'jinja2',
 'packaging',
 'perky',
 'pydantic',
 'rstcheck>=3,<4',
 'semantic_version',
 'sh',
 'twiggy>=0.5.0']

entry_points = \
{'console_scripts': ['antsibull-build = antsibull.cli.antsibull_build:main',
                     'antsibull-docs = antsibull.cli.antsibull_docs:main',
                     'antsibull-lint = antsibull.cli.antsibull_lint:main']}

setup_kwargs = {
    'name': 'antsibull',
    'version': '0.9.0',
    'description': 'Tools for building the Ansible Distribution',
    'long_description': "# antsibull -- Ansible Build Scripts\nTooling for building various things related to Ansible\n\nScripts that are here:\n\n* antsibull-build - Builds Ansible-2.10+ from component collections ([docs](docs/build-ansible.rst))\n* antsibull-docs - Extracts documentation from ansible plugins\n* antsibull-lint - Right now only validates ``changelogs/changelog.yaml`` files ([docs](docs/changelog.yaml-format.md))\n\nA related project is [antsibull-changelog](https://pypi.org/project/antsibull-changelog/), which is in its [own repository](https://github.com/ansible-community/antsibull-changelog/).\n\nScripts are created by poetry at build time.  So if you want to run from\na checkout, you'll have to run them under poetry::\n\n    python3 -m pip install poetry\n    poetry install  # Installs dependencies into a virtualenv\n    poetry run antsibull-build --help\n\nIf you want to create a new release::\n\n    poetry build\n    poetry publish  # Uploads to pypi.  Be sure you really want to do this\n\n.. note:: When installing a package published by poetry, it is best to use\n    pip >= 19.0.  Installing with pip-18.1 and below could create scripts which\n    use pkg_resources which can slow down startup time (in some environments by\n    quite a large amount).\n\nUnless otherwise noted in the code, it is licensed under the terms of the GNU\nGeneral Public License v3 or, at your option, later.\n",
    'author': 'Toshio Kuratomi',
    'author_email': 'a.badger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ansible-community/antsibull',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
