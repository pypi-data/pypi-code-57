# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfgaws',
 'pyfgaws.batch',
 'pyfgaws.batch.tests',
 'pyfgaws.core',
 'pyfgaws.logs',
 'pyfgaws.logs.tests',
 'pyfgaws.tests']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'boto3-stubs[batch,logs]>=1.13.19,<2.0.0',
 'boto3>=1.13.18,<2.0.0',
 'botocore>=1.13.18,<2.0.0',
 'defopt>=6.0,<7.0',
 'namegenerator>=1.0.6,<2.0.0']

entry_points = \
{'console_scripts': ['fgaws-tools = pyfgaws.__main__:main']}

setup_kwargs = {
    'name': 'pyfgaws',
    'version': '0.1.3',
    'description': 'Tools and python libraries for working with AWS.',
    'long_description': '\n[![Language][language-badge]][language-link]\n[![Code Style][code-style-badge]][code-style-link]\n[![Type Checked][type-checking-badge]][type-checking-link]\n[![PEP8][pep-8-badge]][pep-8-link]\n[![Code Coverage][code-coverage-badge]][code-coverage-link]\n[![License][license-badge]][license-link]\n\n---\n\n[![Python package][python-package-badge]][python-package-link]\n[![PyPI version][pypi-badge]][pypi-link]\n[![PyPI download total][pypi-downloads-badge]][pypi-downloads-link]\n\n---\n\n[language-badge]:       http://img.shields.io/badge/language-python-brightgreen.svg\n[language-link]:        http://www.python.org/\n[code-style-badge]:     https://img.shields.io/badge/code%20style-black-000000.svg\n[code-style-link]:      https://black.readthedocs.io/en/stable/ \n[type-checking-badge]:  http://www.mypy-lang.org/static/mypy_badge.svg\n[type-checking-link]:   http://mypy-lang.org/\n[pep-8-badge]:          https://img.shields.io/badge/code%20style-pep8-brightgreen.svg\n[pep-8-link]:           https://www.python.org/dev/peps/pep-0008/\n[code-coverage-badge]:  https://codecov.io/gh/fulcrumgenomics/pyfgaws/branch/master/graph/badge.svg\n[code-coverage-link]:   https://codecov.io/gh/fulcrumgenomics/pyfgaws\n[license-badge]:        http://img.shields.io/badge/license-MIT-blue.svg\n[license-link]:         https://github.com/fulcrumgenomics/pyfgaws/blob/master/LICENSE\n[python-package-badge]: https://github.com/fulcrumgenomics/pyfgaws/workflows/Python%20package/badge.svg\n[python-package-link]:  https://github.com/fulcrumgenomics/pyfgaws/actions?query=workflow%3A%22Python+package%22\n[pypi-badge]:           https://badge.fury.io/py/pyfgaws.svg\n[pypi-link]:            https://pypi.python.org/pypi/pyfgaws\n[pypi-downloads-badge]: https://img.shields.io/pypi/dm/pyfgaws\n[pypi-downloads-link]:  https://pypi.python.org/pypi/pyfgaws\n\n# pyfgaws\n\n`pip install pyfgaws`\n\n**Requires python 3.8**\n\n# Getting Setup\n\nConda is used to install a specific version of python and [poetry](https://github.com/python\n-poetry/poetry) which is then used to manage the python development environment.  If not already\n installed, install [miniconda from the latest platform-appropriate installer](miniconda-link\n ). Then run:\n\n```\nconda create -n pyfgaws -c conda-forge -c bioconda --file conda-requirements.txt\n```\n\nThen activate the new environment and install the toolkit:\n\n```\nconda activate pyfgaws\npoetry install\n```\n\n[miniconda-link]: https://docs.conda.io/en/latest/miniconda.html\n',
    'author': 'Nils Homer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fulcrumgenomics/pyfgaws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
