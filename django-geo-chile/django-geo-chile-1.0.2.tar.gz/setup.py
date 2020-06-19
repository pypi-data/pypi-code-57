# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geo_chile',
 'geo_chile.management',
 'geo_chile.management.commands',
 'geo_chile.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'django-geo-chile',
    'version': '1.0.2',
    'description': "Models and management command to load Chile's Administrative Geographical data from official source.",
    'long_description': '# Django Geo Chile 🇨🇱\n\nModels and management command to load Chile\'s Administrative Geographical data from official source.\n\n## Getting Started \n\n### 1) Download package\n\nUsing poetry\n\n    poetry add django_geo_chile\n\nUsing pipenv\n\n    pipenv install django_geo_chile\n\nUsing pip\n    \n    pip install django_geo_chile\n\n\n### 2) Add to settings\n\nIn `settings.py` add `geo_chile` to `INSTALLED_APPS`\n\n\n    INSTALLED_APPS = [\n        ...\n        "geo_chile",\n    ]\n\n### 3) Create database tables\n\nIn terminal run:\n\n    python manage.py migrate\n\n\n\n### 4) Load data\n\nIn terminal run:\n\n    python manage.py load_geo_chile_data\n\n\n### 5) Drink Wine 🍷 \n',
    'author': 'Francisco Ceruti',
    'author_email': 'hello@fceruti.com',
    'maintainer': 'Francisco Ceruti',
    'maintainer_email': 'hello@fceruti.com',
    'url': 'https://github.com/fceruti/django-geo-chile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
