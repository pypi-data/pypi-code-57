# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['bartdatasets',
 'bartdatasets.extract',
 'bartdatasets.recommendations',
 'bartdatasets.utils']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client==1.9.1',
 'pandas>=1.0.4,<2.0.0',
 'pyarrow>=0.17.1,<0.18.0',
 's3fs>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'bart-datasets',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Cesar Augusto',
    'author_email': 'cesarabruschetta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<3.7',
}


setup(**setup_kwargs)
