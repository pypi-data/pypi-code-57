# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['quantaq']

package_data = \
{'': ['*']}

install_requires = \
['getversion>=1.0.1,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'setuptools>=47.3.1,<48.0.0']

setup_kwargs = {
    'name': 'py-quantaq',
    'version': '0.4.0a2',
    'description': 'API wrapper and utils for QuantAQ, Inc.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/py-quantaq.svg)](https://badge.fury.io/py/py-quantaq)\n![run and build](https://github.com/quant-aq/py-quantaq/workflows/run%20and%20build/badge.svg)\n[![codecov](https://codecov.io/gh/quant-aq/py-quantaq/branch/master/graph/badge.svg)](https://codecov.io/gh/quant-aq/py-quantaq)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n# py-quantaq\nA python wrapper for the QuantAQ RESTful API\n\n## Installation\n\nInstall directly from PyPI:\n\n```sh\n$ pip install -U py-quantaq\n```\n\nOr, install the library directly from GitHub:\n\n```bash\n$ pip install git+https://github.com/quant-aq/py-quantaq.git\n```\n\n## Docs\n\nDocumentation is in progress, but can be found [here](https://quant-aq.github.io/py-quantaq).\n\n## Authentication\n\nTo use the API, you must first have an API key. You can obtain an API key from the [user dashboard][1]. Once you create a new API key, make sure to keep it secret! The easiest way to do this is to save your key as an environment variable. This process is unique to each OS, but many tutorials exist online. For Mac, do the following:\n\nUsing your editor of choice, open up your `.bash_profile`:\n```bash\n# open up your bash profile\n$ nano ~/.bash_profile\n```\n\nNext, save the API key as an environment variable:\n```bash\n# add a line with your API Key\nexport QUANTAQ_APIKEY=<your-api-key-goes-here>\n```\n\nFinally, source your `.bash_profile`:\n\n```sh\n$ source ~/.bash_profile\n```\n\nNow, you shouldn't ever have to touch this again or remember the key!\n\n## Tests\n\nTo run the unittests:\n\n```sh\n$ poetry run pytest tests\n```\n\nTests are automagically run via github actions on each build. Results and coverage are tracked via Code Coverage which can be viewed by clicking on the badge above.\n\n\n[1]: https://www.quant-aq.com/api-keys",
    'author': 'David H Hagan',
    'author_email': 'david.hagan@quant-aq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quant-aq/py-quantaq',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
