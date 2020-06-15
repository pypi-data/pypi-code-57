# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quantaq_cli', 'quantaq_cli.console', 'quantaq_cli.console.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pandas>=1.0.4,<2.0.0',
 'pyarrow>=0.17.1,<0.18.0',
 'terminaltables>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['quantaq-cli = quantaq_cli.console:main']}

setup_kwargs = {
    'name': 'quantaq-cli',
    'version': '0.1.3',
    'description': 'The QuantAQ CLI',
    'long_description': '# QuantAQ Command Line Interface (CLI)\n\n[![PyPI version](https://badge.fury.io/py/quantaq-cli.svg)](https://badge.fury.io/py/quantaq-cli)\n[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/quant-aq/cli/blob/master/LICENSE)\n![run and build](https://github.com/quant-aq/cli/workflows/run%20and%20build/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/quant-aq/cli/branch/master/graph/badge.svg)](https://codecov.io/gh/quant-aq/cli)\n\nThis package provides easy-to-use tools to munge data associated with QuantAQ air quality sensors. \n\n## Documentation\n\nFull documentation can be found [here](https://quant-aq.github.io/cli/).\n\n## Dependencies\n\nThis tool is built for Python 3.6.1+ and has the following key dependencies\n\n```\npython = "^3.6.1"\npandas = "^1.0.4"\nclick = "^7.1.2"\npyarrow = "^0.17.1"\n```\n\nMore details can be found in the `pyproject.toml` file at the base of this repository.\n\n## Installation\n\nInstall from PyPI\n\n```sh\n$ pip install quantaq-cli\n```\n\nIt can also be added as a dependency using Poetry\n\n```sh\n$ poetry add quantaq-cli\n```\n\n\nIf you would like to install locally, you can clone the repository and install directly with Poetry\n\n```sh\n$ poetry install\n```\n\n## Testing\n\nAll tests are automagically run via GitHub actions and reports are uploaded directly to codecov. For results to these runs, click on the badges at the top of this file. In addition, you can run tests locally\n\n\n```sh\n$ poetry run coverage run -m unittest discover\n```\n\n## Development\n\nDevelopment takes place on GitHub. Issues and bugs can be submitted and tracked via the [GitHub Issue Tracker](https://github.com/quant-aq/cli/issues) for this repository.\n\n\n## License\n\nCopyright 2020 QuantAQ, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at\n\n```\nhttp://www.apache.org/licenses/LICENSE-2.0\n```\n\nUnless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.',
    'author': 'David H Hagan',
    'author_email': 'david.hagan@quant-aq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quant-aq/cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
