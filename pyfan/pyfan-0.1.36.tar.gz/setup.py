# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfan',
 'pyfan.gen',
 'pyfan.gen.rand',
 'pyfan.util',
 'pyfan.util.path',
 'pyfan.util.pdf',
 'pyfan.util.rmd']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'pyyaml>=5.3.1,<6.0.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'pyfan',
    'version': '0.1.36',
    'description': '',
    'long_description': None,
    'author': 'Fan Wang',
    'author_email': 'wangfanbsg75@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
