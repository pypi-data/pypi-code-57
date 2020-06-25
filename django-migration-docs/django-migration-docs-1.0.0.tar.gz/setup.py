# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['migration_docs',
 'migration_docs.management',
 'migration_docs.management.commands',
 'migration_docs.tests',
 'migration_docs.tests.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2',
 'formaldict>=1.0.0,<2.0.0',
 'jinja2>=2.10.3,<3.0.0',
 'pyyaml>=5.3,<6.0']

setup_kwargs = {
    'name': 'django-migration-docs',
    'version': '1.0.0',
    'description': 'Sync and validate additional information about your Django migrations.',
    'long_description': 'django-migration-docs\n########################################################################\n\nDocumentation\n=============\n\n`View the django-migration-docs docs here\n<https://django-migration-docs.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall django-migration-docs with::\n\n    pip3 install django-migration-docs\n\nAfter this, add ``migration_docs`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-migration-docs for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\n\nPrimary Authors\n===============\n\n- @juemura (Juliana de Heer)\n- @wesleykendall (Wes Kendall)\n- @tomage (Tómas Árni Jónasson)\n',
    'author': 'Juliana de Heer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/django-migration-docs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
