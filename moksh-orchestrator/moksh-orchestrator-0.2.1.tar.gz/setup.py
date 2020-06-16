# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moksh_orchestrator',
 'moksh_orchestrator.framework',
 'moksh_orchestrator.framework.apis',
 'moksh_orchestrator.framework.config',
 'moksh_orchestrator.framework.config.validators',
 'moksh_orchestrator.framework.impl',
 'moksh_orchestrator.framework.parallel',
 'moksh_orchestrator.framework.utils',
 'moksh_orchestrator.logging']

package_data = \
{'': ['*']}

install_requires = \
['Zope>=4.4.3,<5.0.0',
 'dask-kubernetes>=0.10.1,<0.11.0',
 'dask>=2.18.1,<3.0.0',
 'dpath>=2.0.1,<3.0.0',
 'mypy>=0.780,<0.781',
 'pinject>=0.14.1,<0.15.0',
 'python-interface>=1.6.0,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'yamale>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'moksh-orchestrator',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'gmalho',
    'author_email': 'gaurav.malhotra@nike.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
