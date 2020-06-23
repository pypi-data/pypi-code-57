# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pullframe', 'pullframe.coordinator', 'pullframe.persist']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.5.0,<0.6.0',
 'fastapi>=0.58.0,<0.59.0',
 'kazoo>=2.7.0,<3.0.0',
 'pandas>=1.0.0,<2.0.0',
 'tables>=3.6.1,<4.0.0']

setup_kwargs = {
    'name': 'pullframe',
    'version': '0.1.0',
    'description': 'pull based pandas dataframe syncing',
    'long_description': '# pullframe\n[![pypi](https://img.shields.io/pypi/v/pullframe.svg)](https://pypi.python.org/pypi/pullframe)\n[![Build Status](https://travis-ci.com/ghsang/pullframe.svg?branch=master)](https://travis-ci.com/ghsang/pullframe)\n[![codecov](https://codecov.io/gh/ghsang/pullframe/branch/master/graph/badge.svg)](https://codecov.io/gh/ghsang/pullframe)\n\n## pull based pandas dataframe syncing\n-----\nTo reduce network consumption, it syncs dataframe from the other nodes only on demand.\nWhen your task is divide and conquer style, you should consider [dask][1] instead.\n\n### Features\n* Once the cache has been synced, it will not call remotes. So cache\'s locality is 1.\n* Ideal situations is that you need to read some dataframe multiple times on serveral nodes and the data frame should be updated frequently.\n* Only unique str name is required configuration when you add a new dataframe on the system.\n* No configuration, no operation is needed when a new node is added and a node is crashed and restored.\n* No configuration, no operation makes it be easy to scale up in the cloud.\n\n\n### Communications\n* Coordination via zookeeper\n* Synchronize files via http POST\n\n\n#### Start Service\n```\n$ uvicorn pullframe.sender:app\n```\n\n### Example\n\n#### Load / Save\n```\nfrom pullframe import pullframe\n\nwith pullframe(hosts, directory, sync_timeo 60.0) as pf:\n    # set start as None if you want to load from the very beginning\n    # set end as None if you want to load from the very ending\n    df = pf.load(name, start: Optional[datetime], end: Optional[datetime])\n\n    pf.save(name, df)\n\n```\n\n### TODO\n* Check cache discrepency/corruption between nodes.\n* Stable backup using Amazon S3 / Google cloud storage.\n* Replace zookeeper client to zake (fake kazoo client) during tests.\n\n### Requirements\n* zookeeper\n* the dataframe\'s index should be datetime\n* linux\n* python>=3.7\n* python = "^3.7"\n* pandas = "^1.0.0"\n* tables = "^3.6.1"\n* fastapi = "^0.58.0"\n* aiofiles = "^0.5.0"\n* kazoo = "^2.7.0"\n\n### Free software: MIT License\n\n### Credits\n\n* This package was created with [Cookiecutter][2]\n* Also was copied and modified from the [audreyr/cookiecutter-pypackage][3] project template.\n\n[1]: https://dask.org\n[2]: https://github.com/cookiecutter/cookiecutter\n[3]: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Hyuksang Gwon',
    'author_email': 'gwonhyuksang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ghsang/pullframe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
