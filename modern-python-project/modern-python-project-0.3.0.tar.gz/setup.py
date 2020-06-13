# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modern_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.6.0,<4.0.0',
 'requests>=2.23.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<2.0.0']}

entry_points = \
{'console_scripts': ['modern-python = modern_python.console:main']}

setup_kwargs = {
    'name': 'modern-python-project',
    'version': '0.3.0',
    'description': 'Testing modern python tools',
    'long_description': '# modern-python-project\n[![Tests](https://github.com/LuckyDams/modern-python-project/workflows/Tests/badge.svg)](https://github.com/LuckyDams/modern-python-project/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/LuckyDams/modern-python-project/branch/master/graph/badge.svg)](https://codecov.io/gh/LuckyDams/modern-python-project)\n[![PyPI](https://img.shields.io/pypi/v/modern-python-project.svg)](https://pypi.org/project/modern-python-project)\n[![Documentation](https://readthedocs.org/projects/modern-python-project/badge/?version=latest)](https://modern-python-project.readthedocs.io)\n\nTesting modern python tools\n(Based on this [article](https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769))\n',
    'author': 'LuckyDams',
    'author_email': 'luckydams@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LuckyDams/modern-python-project.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
