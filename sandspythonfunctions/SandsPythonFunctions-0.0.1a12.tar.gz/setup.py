# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['SandsPythonFunctions']

package_data = \
{'': ['*'], 'SandsPythonFunctions': ['extracted_phrases/*']}

install_requires = \
['altair>=4.1.0,<5.0.0',
 'altair_saver>=0.5.0,<0.6.0',
 'gensim>=3.8.3,<4.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'nltk>=3.5,<4.0',
 'notebook>=6.0.3,<7.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyarrow>=0.16.0,<0.17.0',
 'pyemd>=0.5.1,<0.6.0',
 'wmd>=1.3.2,<2.0.0',
 'zstandard>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'sandspythonfunctions',
    'version': '0.0.1a12',
    'description': 'Functions I use regularly with my python projects',
    'long_description': "# Sands Python Functions\n\nSome functions I find useful regularly and I put them all into one package for easy access\n\nI created this using [Poetry](https://python-poetry.org/).\n\n## Instructions\n\n- To build this you must first install poetry see instructions [here](https://python-poetry.org/docs/#installation)\n- However to make it easy to access this is all of the code you'll need on linux to make this run (note that I use zsh not bash for my shell)\n    - First you must navigate to the folder containing these files `CHANGELOG.md   LICENSE  'README reference.md'   README.md   dist   poetry.lock   pyproject.toml   src`\n    - You then to make sure that you have the python environment that you want activated\n    - You can then enter the code below\n\n```sh\npoetry build\npoetry install\n```\n\n## Basic Usage Example\n\nTODO:\n\n## Included Packages\n\n### Functions from EmailFunctions\n\n- \n\n### Functions from MultiprocessingFunctions\n\n- \n\n### Functions from ParquetFunctions\n\n- \n\n### Functions from PrintFunctions\n\n- \n\n### Functions from TimerFunctions\n\n- \n\n## Testing\n\nPytest runs in whatever directory you're located in at the time you run pytest so if you're not in the directory of the test scripts pytest will not see the files it needs to and will then fail.\n\nFollow the code below to test the functions\n\n```sh\ncd src/tests\npytest /src/tests/EmailFunctions_test.py\npytest /src/tests/MultiprocessingFunctions_test.py\npytest /src/tests/ParquetFunctions_test.py\n```\n\n## CI/CD\n\nSee [this repo](https://github.com/speg03/shishakai/blob/971261e6f73ee8b9dcc83837b6c1a5f809c985f8/.github/workflows/upload-python-package.yml) for an example of someone using poetry with they're python project to upload to PyPI on push to master.\n",
    'author': 'ldsands',
    'author_email': 'ldsands@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ldsands/SandsPythonFunctions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
