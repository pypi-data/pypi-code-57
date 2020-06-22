# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia', 'graia.protocol.core']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'graia-protocol-core',
    'version': '0.0.1',
    'description': 'Abstract implementation of "Protocol" in "Graia Framework"',
    'long_description': None,
    'author': 'Chenwe-i-lin',
    'author_email': '1846913566@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
