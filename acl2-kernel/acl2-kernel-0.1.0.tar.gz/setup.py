# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acl2_kernel']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=5.3.0,<6.0.0',
 'ipython>=7.15.0,<8.0.0',
 'jupyter_client>=6.1.3,<7.0.0',
 'pexpect>=4.8.0,<5.0.0']

setup_kwargs = {
    'name': 'acl2-kernel',
    'version': '0.1.0',
    'description': 'Jupyter Kernel for ACL2',
    'long_description': None,
    'author': 'TANIGUCHI Masaya',
    'author_email': 'mew@cat.ovh',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
