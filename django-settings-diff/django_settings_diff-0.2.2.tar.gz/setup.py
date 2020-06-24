# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_settings_diff']

package_data = \
{'': ['*']}

install_requires = \
['deepdiff>=3.3.0,<4.0.0']

entry_points = \
{'console_scripts': ['diffsettings = django_settings_diff.cli:main']}

setup_kwargs = {
    'name': 'django-settings-diff',
    'version': '0.2.2',
    'description': 'Tool to help diff two Django settings modules',
    'long_description': '``django-settings-diff``\n========================\n\nA very simple tool to help diff two Django settings modules.\n\nMotivation\n----------\n\nLet\'s say that you have done some significant refactoring to your settings module. For example, you have gone from a single settings file to a modular approach, where there is no longer a single ``settings.py``. You want to make sure that your settings are effectively *exactly* the same as before, though! Of course you can\'t rely on simple file diffing, since there is no longer a single ``settings.py``.\n\nThere are some non-intuitive things to account for, which ``django-settings-diff`` handles for you:\n\n1. Even with a single ``settings.py``, there is a (potentially) significant difference between simply importing the file and the "final" settings that are used by Django (see https://docs.djangoproject.com/en/2.1/topics/settings/#using-settings-in-python-code). That is, we want to compare the *actual settings at runtime*!\n2. The ``settings`` object cannot be naively treated as a ``dict`` -- it is similar, but different enough to prevent easy diffing (the native settings object thwarts both ``pprint`` and ``deepdiff``).\n\nSo, it isn\'t doing anything crazy, but it removes some overhead.\n\nInstallation\n------------\n\nInstall from pip (recommended):\n\n::\n\n    $ pip install django-settings-diff\n\nOr, install straight from the repo:\n\n::\n\n    $ git clone https://github.com/GreenBankObservatory/django-settings-diff\n    $ pip install django-settings-diff\n\nNote that this will install a wrapper script for you: ``diffsettings``\n\nEntry Points\n------------\n\nUse the wrapper script (recommended):\n\n::\n\n    $ diffsettings -h\n\nCall the module:\n\n::\n\n    $ python -m django_settings_diff -h\n\nImport as library:\n\n::\n\n    $ python\n    >>> from django_settings_diff import diffsettings\n    >>> help(diffsettings)\n\nUsage\n-----\n\nThere are two standard usage patterns.\n\nYou should first ensure that you have saved two versions of your settings. For this example we will use ``myapp/settings_old.py`` and ``myapp/settings_new.py``.\n\nAlternatively, you could use the same ``DJANGO_SETTINGS_MODULE`` for both dumps, but swap the settings file itself in between. This is useful in repositories that rely on the settings file being a specific name, for example.\n\n#1: Compare Python objects directly\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nThis uses ``deepdiff`` internally to perform the diff.\n\nDump Settings\n^^^^^^^^^^^^^\n\nPickle the settings modules to disk:\n\n::\n\n    $ DJANGO_SETTINGS_MODULE=myapp.settings_old diffsettings --dump old_settings.pkl\n    $ DJANGO_SETTINGS_MODULE=myapp.settings_new diffsettings --dump new_settings.pkl\n\nDiff Settings\n^^^^^^^^^^^^^\n\nNow we can diff the two settings objects:\n\n::\n\n    $ diffsettings old_settings.pkl new_settings.pkl \n\nSee the documentation for `deepdiff <https://github.com/seperman/deepdiff>`_ for help deciphering the output.\n\n#2: Compare via external diff tool\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nIn this method the settings are dumped as text files and then compared using a standard diff tool.\n\nDump Settings\n^^^^^^^^^^^^^\n\nDump the settings modules to disk (internally this uses ``pprint`` to print the settings object):\n\n::\n\n    $ DJANGO_SETTINGS_MODULE=myapp.settings_old diffsettings --dump old_settings.txt\n    $ DJANGO_SETTINGS_MODULE=myapp.settings_new diffsettings --dump new_settings.txt\n\nDiff Settings\n^^^^^^^^^^^^^\n\nThen, use your favorite diff tool to compare these. This should work quite well, since the object hierarchy has been broken up line by line.\n\nFor example:\n\n::\n\n    $ tkdiff {old,new}_settings.txt\n',
    'author': 'Thomas Chamberlin',
    'author_email': 'tchamber@nrao.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/GreenBankObservatory/django-settings-diff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
