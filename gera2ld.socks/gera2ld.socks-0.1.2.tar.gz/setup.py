# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gera2ld',
 'gera2ld.socks',
 'gera2ld.socks.client',
 'gera2ld.socks.server',
 'gera2ld.socks.utils']

package_data = \
{'': ['*']}

install_requires = \
['async_dns>=1.0.10,<2.0.0', 'gera2ld-pyserve>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'gera2ld.socks',
    'version': '0.1.2',
    'description': 'SOCKS client and server based on asyncio',
    'long_description': None,
    'author': 'Gerald',
    'author_email': 'gera2ld@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/pysocks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
