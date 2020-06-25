# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dok8s', 'dok8s.cli.commands', 'dok8s.lib.analyses']

package_data = \
{'': ['*'], 'dok8s': ['cli/*', 'lib/*', 'lib/helpers/*']}

install_requires = \
['kubernetes>=11.0,<12.0', 'pyyaml>=5.3,<6.0', 'tabulate>=0.8,<0.9']

entry_points = \
{'console_scripts': ['dok8s = dok8s.cli.__main__:main']}

setup_kwargs = {
    'name': 'dok8s',
    'version': '0.0.3',
    'description': 'Output notes for a Kubernetes deployment',
    'long_description': "[![github latest release](https://badgen.net/github/release/nichelia/dok8s?icon=github)](https://github.com/nichelia/dok8s/releases/latest/)\n[![pypi latest package](https://badgen.net/pypi/v/dok8s?label=pypi%20pacakge)](https://pypi.org/project/dok8s/)\n[![docker latest image](https://img.shields.io/docker/v/nichelia/dok8s?label=image&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/nichelia/dok8s)\n[![project license](https://badgen.net/github/license/nichelia/dok8s?color=purple)](https://github.com/nichelia/dok8s/blob/master/LICENSE)\n\n![dok8s CI](https://github.com/nichelia/dok8s/workflows/dok8s%20CI/badge.svg)\n![dok8s CD](https://github.com/nichelia/dok8s/workflows/dok8s%20CD/badge.svg)\n[![security scan](https://badgen.net/dependabot/nichelia/dok8s/?label=security%20scan)](https://github.com/nichelia/dok8s/labels/security%20patch)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://github.com/pre-commit/pre-commit)\n\n\n[![code coverage](https://badgen.net/codecov/c/github/nichelia/dok8s?label=code%20coverage)](https://codecov.io/gh/nichelia/dok8s)\n[![code alerts](https://badgen.net/lgtm/alerts/g/nichelia/dok8s?label=code%20alerts)](https://lgtm.com/projects/g/nichelia/dok8s/alerts/)\n[![code quality](https://badgen.net/lgtm/grade/g/nichelia/dok8s?label=code%20quality)](https://lgtm.com/projects/g/nichelia/dok8s/context:python)\n[![code style](https://badgen.net/badge/code%20style/black/color=black)](https://github.com/ambv/black)\n\n# dok8s\ndok8s: Output notes for a Kubernetes deployment.\n\n\n## Contents\n1. [Use Case](#use-case)\n2. [Configuration](#configuration)\n3. [Development](#development)\n4. [Testing](#testing)\n5. [Versioning](#versioning)\n6. [Deployment](#deployment)\n7. [Production](#production)\n\n## Use Case\n\nA collection of output notes for Kubernetes deployments.  \nInput: [TODO].  \nOutput: [TODO].\n\n### Requirements\n\n* [TODO]\n\n### Assumptions\n\n* [TODO]\n\n### Design\n\n[TODO]\n\n## Configuration\n\nBehaviour of the application can be configured via Environment Variables.\n\n| Environment Variable | Description | Type | Default Value |\n| -------------- | -------------- | -------------- | -------------- |\n| `DOK8S_LOG_LEVEL` | Level of logging - overrides verbose/quiet flag | string | - |\n| `DOK8S_LOG_DIR` | Directory to save logs | string | - |\n| `DOK8S_BIN_DIR` | Directory to save any output (bin) | string | bin |\n\n## Development\n\n### Configure for local development\n\n* Clone [repo](https://github.com/nichelia/dok8s) on your local machine\n* Install [`conda`](https://www.anaconda.com) or [`miniconda`](https://docs.conda.io/en/latest/miniconda.html)\n* Create your local project environment (based on [`conda`](https://www.anaconda.com), [`poetry`](https://python-poetry.org), [`pre-commit`](https://pre-commit.com)):  \n`$ make env`\n* (Optional) Update existing local project environment:  \n`$ make env-update`\n\n### Run locally\n\nOn a terminal, run the following (execute on project's root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* Run the CLI using `poetry`:  \n`$ poetry run dok8s`\n\n### Contribute\n\n[ Not Available ]\n\n## Testing\n(part of CI/CD)\n\n[ Work in progress... ]\n\nTo run the tests, open a terminal and run the following (execute on project's root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To run pytest:  \n`$ make test`\n* To check test coverage:  \n`$ make test-coverage`\n\n## Versioning\n\nIncrement the version number:  \n`$ poetry version {bump rule}`  \nwhere valid bump rules are:\n\n1. patch\n2. minor\n3. major\n4. prepatch\n5. preminor\n6. premajor\n7. prerelease\n\n### Changelog\n\nUse `CHANGELOG.md` to track the evolution of this package.  \nThe `[UNRELEASED]` tag at the top of the file should always be there to log the work until a release occurs.  \n\nWork should be logged under one of the following subtitles:\n* Added\n* Changed\n* Fixed\n* Removed\n\nOn a release, a version of the following format should be added to all the current unreleased changes in the file.  \n`## [major.minor.patch] - YYYY-MM-DD`\n\n## Deployment\n\n### Pip package\n\nOn a terminal, run the following (execute on project's root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To build pip package:  \n`$ make build-package`\n* To publish pip package (requires credentials to PyPi):  \n`$ make publish-package`\n\n### Docker image\n\nOn a terminal, run the following (execute on project's root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To build docker image:  \n`$ make build-docker`\n\n## Production\n\nFor production, a Docker image is used.\nThis image is published publicly on [docker hub](https://hub.docker.com/repository/docker/nichelia/dok8s).\n\n* First pull image from docker hub:  \n`$ docker pull nichelia/dok8s:[version]`\n* First pull image from docker hub:  \n`$ docker run --rm -it -v ~/dok8s_bin:/usr/src/bin nichelia/dok8s:[version]`  \nThis command mounts the application's bin (outcome) to user's root directory under dok8s_bin folder.\n\nwhere version is the published application version (e.g. 0.1.0)\n",
    'author': 'Nicholas Elia',
    'author_email': 'me@nichelia.com',
    'maintainer': 'Nicholas Elia',
    'maintainer_email': 'me@nichelia.com',
    'url': 'https://github.com/nichelia/dok8s',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
