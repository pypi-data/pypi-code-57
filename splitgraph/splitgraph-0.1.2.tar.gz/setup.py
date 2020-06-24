# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitgraph',
 'splitgraph.cloud',
 'splitgraph.commandline',
 'splitgraph.config',
 'splitgraph.core',
 'splitgraph.core.indexing',
 'splitgraph.core.sql',
 'splitgraph.engine',
 'splitgraph.engine.postgres',
 'splitgraph.hooks',
 'splitgraph.ingestion',
 'splitgraph.ingestion.socrata',
 'splitgraph.splitfile']

package_data = \
{'': ['*'],
 'splitgraph': ['.pyre/*', 'resources/splitgraph_meta/*', 'resources/static/*']}

install_requires = \
['asciitree>=0.3.3,<0.4.0',
 'click>=7,<8',
 'click_log>=0.3.2,<0.4.0',
 'docker>=4.0',
 'minio>=4',
 'packaging>=20.1,<21.0',
 'parsimonious>=0.8,<0.9',
 'psycopg2-binary>=2,<3',
 'pyyaml>=5.1',
 'requests>=2.22',
 'sodapy>=2.1',
 'tabulate>=0.8.7,<0.9.0',
 'tqdm>=4.46.0,<5.0.0']

extras_require = \
{':sys_platform != "win32"': ['pglast>=1.6'],
 'pandas': ['pandas[ingestion]>=0.24', 'sqlalchemy[ingestion]>=1.3,<2.0']}

entry_points = \
{'console_scripts': ['sgr = splitgraph.commandline:cli']}

setup_kwargs = {
    'name': 'splitgraph',
    'version': '0.1.2',
    'description': 'Command line library and Python client for Splitgraph, a version control system for data',
    'long_description': '![](https://www.mildbyte.xyz/asciicast/splitfiles.gif)\n\n# Splitgraph\n![Build status](https://github.com/splitgraph/splitgraph/workflows/build_all/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/splitgraph/splitgraph/badge.svg?branch=master)](https://coveralls.io/github/splitgraph/splitgraph?branch=master)\n[![PyPI version](https://badge.fury.io/py/splitgraph.svg)](https://badge.fury.io/py/splitgraph)\n[![Discord chat room](https://img.shields.io/discord/718534846472912936.svg)](https://discord.gg/4Qe2fYA)\n[![Follow](https://img.shields.io/badge/twitter-@Splitgraph-blue.svg)](https://twitter.com/Splitgraph)\n\n[Splitgraph](https://www.splitgraph.com) is a tool for building, versioning, querying and sharing datasets that works on top of [PostgreSQL](https://postgresql.org) and [integrates](https://www.splitgraph.com/product/splitgraph/integrations) seamlessly with anything that uses PostgreSQL.\n\nThis repository contains most of the core code for the Splitgraph library, \nthe [`sgr` command line client](https://www.splitgraph.com/docs/architecture/sgr-client) and the [Splitgraph Engine](engine/README.md). \n\nSee https://www.splitgraph.com/docs/getting-started/introduction for the full docs.\n\n## Installation\n\nYou will need access to [Docker](https://docs.docker.com/install/) as Splitgraph uses it to run\nthe Splitgraph Engine.\n\nFor Linux and OSX, there\'s a single script:\n\n```\n$ bash -c "$(curl -sL https://github.com/splitgraph/splitgraph/releases/latest/download/install.sh)"\n```\n\nThis script downloads the `sgr` binary and sets up the Splitgraph Engine Docker container.\n\nAlternatively, you can get the `sgr` single binary from [the releases page](https://github.com/splitgraph/splitgraph/releases) and run [`sgr engine add`](https://www.splitgraph.com/docs/sgr/engine-management/engine-add) to create an engine.\n\nSee the [installation guide](https://www.splitgraph.com/docs/getting-started/installation) for more installation methods.\n\n## Quick start guide\n\nYou can follow the [quick start guide](https://www.splitgraph.com/docs/getting-started/five-minute-demo) that will guide you through the basics of using Splitgraph with public and private data.\n\nAlternatively, Splitgraph comes with plenty of [examples](examples) to get you started.\n\nIf you\'re stuck or have any questions, check out the [documentation](https://www.splitgraph.com/docs/) or join our [Discord channel](https://discord.gg/4Qe2fYA)!\n\n## Setting up a development environment\n\n  * Splitgraph requires Python 3.6 or later.\n  * Install [Poetry](https://github.com/python-poetry/poetry): `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python` to manage dependencies\n  * Install pre-commit hooks (we use [Black](https://github.com/psf/black) to format code)\n  * `git clone https://github.com/splitgraph/splitgraph.git`\n  * `poetry install` \n  * To build the [engine](https://www.splitgraph.com/docs/architecture/splitgraph-engine) Docker image: `cd engine && make`\n\n### Running tests\n\nThe test suite requires [docker-compose](https://github.com/docker/compose). You will also\nneed to add these lines to your `/etc/hosts` or equivalent:\n\n```\n127.0.0.1       local_engine\n127.0.0.1       remote_engine\n127.0.0.1       objectstorage\n```\n\nTo run the core test suite, do\n\n```\ndocker-compose -f test/architecture/docker-compose.core.yml up -d\npoetry run pytest -m "not mounting and not example"\n```\n\nTo run the test suite related to "mounting" and importing data from  other databases\n(PostgreSQL, MySQL, Mongo), do\n\n```\ndocker-compose -f test/architecture/docker-compose.core.yml -f test/architecture/docker-compose.core.yml up -d  \npoetry run pytest -m mounting\n```\n\nFinally, to test the [example projects](https://github.com/splitgraph/splitgraph/tree/master/examples), do\n\n```\n# Example projects spin up their own engines\ndocker-compose -f test/architecture/docker-compose.core.yml -f test/architecture/docker-compose.core.yml down -v\npoetry run pytest -m example\n```\n\nAll of these tests run in [CI](https://github.com/splitgraph/splitgraph/actions).\n',
    'author': 'Splitgraph Limited',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.splitgraph.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
