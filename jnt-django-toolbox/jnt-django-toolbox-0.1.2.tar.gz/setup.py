# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jnt_django_toolbox',
 'jnt_django_toolbox.admin',
 'jnt_django_toolbox.admin.decorators',
 'jnt_django_toolbox.admin.fields',
 'jnt_django_toolbox.admin.filters',
 'jnt_django_toolbox.admin.helpers',
 'jnt_django_toolbox.admin.widgets',
 'jnt_django_toolbox.helpers',
 'jnt_django_toolbox.models',
 'jnt_django_toolbox.models.fields',
 'jnt_django_toolbox.models.fields.bit']

package_data = \
{'': ['*']}

install_requires = \
['django>=3']

setup_kwargs = {
    'name': 'jnt-django-toolbox',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Junte',
    'author_email': 'tech@junte.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
