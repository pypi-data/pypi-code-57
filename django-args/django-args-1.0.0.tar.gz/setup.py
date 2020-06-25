# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djarg', 'djarg.tests']

package_data = \
{'': ['*'], 'djarg.tests': ['templates/tests/*']}

install_requires = \
['django-formtools>=2.2,<3.0', 'django>=2', 'python-args>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'django-args',
    'version': '1.0.0',
    'description': 'Django wrappers for python-args functions.',
    'long_description': 'django-args\n########################################################################\n\nDocumentation\n=============\n\n`View the django-args docs here\n<https://django-args.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall django-args with::\n\n    pip3 install django-args\n\nAfter this, add ``djarg`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-args for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n',
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/django-args',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
