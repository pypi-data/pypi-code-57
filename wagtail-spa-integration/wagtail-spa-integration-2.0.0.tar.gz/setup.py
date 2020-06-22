# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_spa_integration', 'wagtail_spa_integration.templatetags']

package_data = \
{'': ['*'], 'wagtail_spa_integration': ['templates/wagtailadmin/pages/*']}

install_requires = \
['Django>=2.2.0', 'wagtail>=2.8.0']

setup_kwargs = {
    'name': 'wagtail-spa-integration',
    'version': '2.0.0',
    'description': 'Tools for using Wagtail API with JavaScript single page apps',
    'long_description': None,
    'author': 'David Burke',
    'author_email': 'david@burkesoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
