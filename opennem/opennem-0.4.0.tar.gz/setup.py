# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opennem',
 'opennem.agent',
 'opennem.api',
 'opennem.commands',
 'opennem.datetimes',
 'opennem.db',
 'opennem.db.migrations',
 'opennem.db.models',
 'opennem.nem_derived',
 'opennem.pipelines',
 'opennem.scheduler',
 'opennem.schema',
 'opennem.settings',
 'opennem.spiders',
 'opennem.spiders.bom',
 'opennem.spiders.nem',
 'opennem.spiders.wem',
 'opennem.utils']

package_data = \
{'': ['*'], 'opennem.db': ['fixtures/*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'huey>=2.2.0,<3.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'scrapy>=2.1.0,<3.0.0',
 'sentry-sdk>=0.14.4,<0.15.0',
 'smart_open>=2.0.0,<3.0.0',
 'sqlalchemy>=1.3.17,<2.0.0']

entry_points = \
{'console_scripts': ['opennem = opennem.cli:main']}

setup_kwargs = {
    'name': 'opennem',
    'version': '0.4.0',
    'description': 'opennem engine agent',
    'long_description': '# OpenNEM Energy Market Data Access\n\nThe OpenNEM project aims to make the wealth of public National Electricity Market (NEM) data more accessible to a wider audience.\n\nThis toolkit enables downloading, mirroring and accessing energy data from various networks\n\nProject homepage at https://opennem.org.au\n\nAvailable on Docker at https://hub.docker.com/r/opennem/opennem\n\nCurrently supports:\n\n- Australian NEM: https://www.nemweb.com.au/\n- West Australia Energy Market: http://data.wa.aemo.com.au/\n\n\n## Install\n\nYou can install this project with python `pip`:\n\n```sh\n$ pip install opennem\n```\n\nOr alternatively with docker:\n\n```\n$ docker pull opennem/opennem\n```\n\nBundled with sqlite support. Other database drivers are optional and not installed by default. Install a supported database driver:\n\nPostgres:\n\n```sh\n$ pip install psycopg2\n```\n\n## Usage\n\nList the crawlers\n\n```sh\n$ scrapy list\n```\n\nCrawl\n\n```sh\n$ scrapy crawl au.nem.current.dispatch_scada\n```\n\n## Development\n\nSetting up a virtual environment and installing requiements using Poetry:\n\n```sh\n$ poetry install\n$ source .venv/bin/activate\n```\n\nSettings are read from environment variables. Environment variables can be read from a `.env` file in the root of the folder. Setup the environment by copying the `.env.sample` file to `.env`. The defaults in the sample file map to the settings in `docker-compose.yml`\n\nThere is a `docker-compose` file that will bring a local database:\n\n```sh\n$ docker-compose up -d\n```\n\nBring up the database migrations using alembic:\n\n```sh\n$ alembic upgrade head\n```\n\nRun scrapy in the root folder for options:\n\n```sh\n$ scrapy\n```\n\nThe `opennem` cli interface provides other options and settings:\n\n```sh\n$ opennem -h\n```\n\nSettings for Visual Studio Code are stored in `.vscode`. Code is kept formatted and linted using `pylint`, `black` and `isort` with settings defined in `pyproject.toml`\n\n## Architecture overview\n\nThis project uses [Scrapy](https://scrapy.org/) to obtain data from supported energy markets and [SQLAlchemy](https://www.sqlalchemy.org/) to store data, and [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations. Database storage has been tested with sqlite, postgres and mysql.\n\nOverview of scrapy architecture:\n\n![](https://docs.scrapy.org/en/latest/_images/scrapy_architecture_02.png)\n\n## Code Navigation\n\n* Spider definitions in `opennem/spiders`\n* Processing pipelines for crawls in `opennem/pipelines`\n* Database models for supported energy markets are stored in `opennem/db/models`\n',
    'author': 'Dylan McConnell',
    'author_email': 'dylan.mcconnell@unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://opennem.org.au',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
