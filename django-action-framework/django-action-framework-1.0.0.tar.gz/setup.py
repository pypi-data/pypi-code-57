# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daf',
 'daf.migrations',
 'daf.tests',
 'daf.tests.actions',
 'daf.tests.migrations']

package_data = \
{'': ['*'],
 'daf': ['templates/daf/admin/*'],
 'daf.tests': ['templates/tests/*']}

install_requires = \
['django-args>=1.0.0,<2.0.0',
 'django>=2',
 'djangorestframework>=3.0.0,<4.0.0',
 'python-args>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'django-action-framework',
    'version': '1.0.0',
    'description': 'Easily create actions and various interfaces around them.',
    'long_description': 'django-action-framework\n########################################################################\n\nDocumentation\n=============\n\n`View the django-action-framework docs here\n<https://django-action-framework.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall django-action-framework with::\n\n    pip3 install django-action-framework\n\nAfter this, add ``daf`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-action-framework for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n- @romansul (Roman Sul)\n- @chang-brian (Brian Chang)\n',
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/django-action-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
