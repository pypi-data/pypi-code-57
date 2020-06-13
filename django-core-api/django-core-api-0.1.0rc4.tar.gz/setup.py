# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_core_api', 'django_core_api.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3,<4',
 'dj-database-url>=0,<1',
 'django-autoslug-iplweb>=1,<2',
 'django-filter>=2,<3',
 'django-model-utils>=4,<5',
 'django-ordered-model>=3,<4',
 'django-redis>=4,<5',
 'django-storages>=1,<2',
 'djangorestframework>=3,<4',
 'drf-extensions>=0,<1',
 'envparse>=0,<1',
 'psycopg2-binary>=2,<3',
 'python-dateutil',
 'whitenoise>=5,<6']

setup_kwargs = {
    'name': 'django-core-api',
    'version': '0.1.0rc4',
    'description': '',
    'long_description': None,
    'author': 'João Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
