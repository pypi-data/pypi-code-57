# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgstats',
 'pgstats.management',
 'pgstats.management.commands',
 'pgstats.migrations',
 'pgstats.tests']

package_data = \
{'': ['*']}

install_requires = \
['django>=2']

setup_kwargs = {
    'name': 'django-pgstats',
    'version': '1.0.0',
    'description': 'Commands and models for tracking internal postgres stats.',
    'long_description': 'django-pgstats\n########################################################################\n\nDocumentation\n=============\n\n`View the django-pgstats docs here\n<https://django-pgstats.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall django-pgstats with::\n\n    pip3 install django-pgstats\n\nAfter this, add ``pgstats`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-pgstats for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n- @tomage (Tómas Árni Jónasson)\n',
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/django-pgstats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
