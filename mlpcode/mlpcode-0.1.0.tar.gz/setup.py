# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlpcode']

package_data = \
{'': ['*'],
 'mlpcode': ['data/*',
             'data/affnist/readme.txt',
             'data/cifar-10/readme.txt',
             'data/fashion-mnist/readme.txt',
             'data/mnist-c/*',
             'data/mnist/readme.txt']}

install_requires = \
['cupy-cuda102>=7.3.0,<8.0.0',
 'h5py>=2.10.0,<3.0.0',
 'numpy>=1.18.2,<2.0.0',
 'typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['mlp = mlpcode.cli:main']}

setup_kwargs = {
    'name': 'mlpcode',
    'version': '0.1.0',
    'description': 'MLP cli for semester project',
    'long_description': None,
    'author': 'Arslan',
    'author_email': 'rslnkrmt2552@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
