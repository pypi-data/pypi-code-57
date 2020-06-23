# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['measurement',
 'measurement.plugins',
 'measurement.plugins.download_speed',
 'measurement.plugins.download_speed.tests',
 'measurement.plugins.latency',
 'measurement.plugins.latency.tests',
 'measurement.plugins.netflix_fast',
 'measurement.plugins.netflix_fast.tests',
 'measurement.plugins.speedtestdotnet',
 'measurement.plugins.speedtestdotnet.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0',
 'six>=1.12,<2.0',
 'speedtest-cli>=2.1,<3.0',
 'statistics>=1.0.3,<2.0.0',
 'validators>=0.13.0,<0.14.0']

extras_require = \
{':python_version >= "3.6.0" and python_version < "4.0.0"': ['dataclasses>=0.6.0,<0.7.0']}

setup_kwargs = {
    'name': 'honestybox-measurement',
    'version': '1.0.6',
    'description': 'A framework for measuring things and producing structured results.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/honestybox-measurement.svg)](https://badge.fury.io/py/honestybox-measurement)\n[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/honestybox-measurement.svg)](https://pypi.python.org/pypi/honestybox-measurement/)\n[![GitHub license](https://img.shields.io/github/license/honesty-box/honestybox-measurement)](https://github.com/honesty-box/honestybox-measurement/blob/master/LICENSE)\n[![GitHub Actions (Tests)](https://github.com/honesty-box/honestybox-measurement/workflows/Tests/badge.svg)](https://github.com/honesty-box/honestybox-measurement)\n[![GitHub Actions (Quality)](https://github.com/honesty-box/honestybox-measurement/workflows/Quality/badge.svg)](https://github.com/honesty-box/honestybox-measurement)\n[![Honesty Box Twitter](https://img.shields.io/twitter/follow/honestybox?style=social)](https://twitter.com/honestybox)\n\n# honestybox-measurement\n\nA framework for measuring things and producing structured results.\n\n## Requirements\n\n`honestybox-measurement` supports Python 3.5 to Python 3.8 inclusively.\n\n## Development\n\n### Git hooks\n\n[pre-commit](https://pre-commit.com/) hooks are included to ensure code quality\non `commit` and `push`. Install these hooks like so:\n\n```shell script\n$ pre-commit install && pre-commit install -t pre-push\nasd\n```\n\n## Releases\n\nTo ensure releases are always built on the latest codebase, *changes are only ever merged to `release` from `master`*.\n\n### Creating a release\n1. Ensure that master is up to date:\n\n    ```shell script\n    $ git checkout master\n    $ git pull origin\n    ```\n\n2. Switch to release and ensure it is up to date:\n\n    ```shell script\n    $ git checkout release\n    $ git pull origin\n    ```\n\n3. Merge from master:\n\n    ```shell script\n    $ git merge master\n    ```\n\n4. Add a new release to `CHANGELOG.md` and include all changes in `[Unreleased]`.\n\n5. Update version number in `pyproject.toml`\n\n6. Commit the changes to the `release` branch with comment `Release <version number>`\n\n    ```shell script\n    $ git add CHANGELOG.md pyproject.toml\n    $ git commit -m 'Release x.y.z`\n    ```\n\n7. Tag the commit with the release number:\n\n    ```shell script\n    $ git tag x.y.z\n    ```\n\n8. Push the commit and tags upstream:\n\n    ```shell script\n    $ git push && git push --tags\n    ```\n\n9. Merge changes into master and push upstream:\n\n    ```shell script\n    $ git checkout master\n    $ git merge release\n    $ git push\n    ```\n\n\n### Publishing a release\n\n1. Install [poetry](https://poetry.eustace.io)\n\n2. Checkout the release:\n\n    ```shell script\n    $ git checkout x.y.z\n    ```\n\n3. Publish the release:\n\n    ```shell script\n    $ poetry publish --build\n    ```\n",
    'author': 'James Stewart',
    'author_email': 'james@amorphitec.io',
    'maintainer': 'Honesty Box',
    'maintainer_email': 'engineering@honestybox.com.au',
    'url': 'https://github.com/honesty-box/honestybox-measurement/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
