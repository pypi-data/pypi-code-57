# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adit',
 'adit.checkpoint',
 'adit.config',
 'adit.dfs',
 'adit.ingest',
 'adit.ingest.crawler',
 'adit.ingest.receiver']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'dask[complete]>=2.17.2,<3.0.0',
 'distributed>=2.18.0,<3.0.0',
 'faust>=1.10.4,<2.0.0',
 'fxcmpy>=1.2.6,<2.0.0',
 'minio>=5.0.10,<6.0.0',
 'oandapyV20>=0.6.3,<0.7.0',
 'pandas>=1.0.4,<2.0.0',
 'python-socketio>=4.6.0,<5.0.0',
 'tensorflow>=2.2.0,<3.0.0',
 'tiledb>=0.6.3,<0.7.0',
 'v20>=3.0.25,<4.0.0']

setup_kwargs = {
    'name': 'adit',
    'version': '0.1.0',
    'description': 'Adit is a toolbox that helps people collaborating on machine learning prototype easier.',
    'long_description': None,
    'author': 'Trinh Tran',
    'author_email': 'trinhtran2151995@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
