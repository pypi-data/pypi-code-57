# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stoltzmaniac',
 'stoltzmaniac.data_handler',
 'stoltzmaniac.models',
 'stoltzmaniac.models.supervised',
 'stoltzmaniac.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.4,<2.0.0', 'pandas>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'stoltzmaniac',
    'version': '0.2.0',
    'description': 'A lightweight library for basic machine learning tasks.',
    'long_description': "# stoltzmaniac  \n\nA Python package to solve simple data science problems. \n\nThis is a rudimentary library for machine learning with 3 concepts in mind. This library should be:\n  - easy-to-use\n  - easy-to-read\n  - easy-to-interpret\n\nOptimization for efficiency of compute, latency, and memory will not be a priority.\n\nThe only external package we will use for modeling will be `numpy`. Others required are simply to get data into `numpy.ndarray` format.\n\nThis is my first package, so help out and don't hold back on putting in PR's. Thank you!\n\nInstalling:\n```bash\npip install stoltzmaniac\n```\n\n----\n\nRun tests  \n`pytest`\n\nAdd packages (example with requests):\n\nFor development:\n`poetry add -D requests`\n\nFor production:\n`poetry add requests`\n\nBuild:\n`poetry build`\n\nPublish:\n`poetry publish`",
    'author': 'stoltzmaniac',
    'author_email': 'scott@stoltzmaniac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stoltzmaniac/stoltzmaniac',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
