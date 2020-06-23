# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newsletter', 'newsletter.migrations', 'newsletter.tests']

package_data = \
{'': ['*'], 'newsletter': ['templates/*']}

install_requires = \
['giant-mixins>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'giant-newsletter',
    'version': '0.2.0',
    'description': 'A small reusable package that adds a Newsletter app to a project',
    'long_description': '# Giant Newsletter\n\nA re-usable package which can be used in any project that requires a generic `Newletter` app. \n\nThis will include the basic formatting and functionality such as model creation via the admin and email sending.\n\n## Installation\n\nTo install with the package manager, run:\n\n    $ poetry add giant-newsletter\n\nYou should then add `"newsletter"` to the `INSTALLED_APPS` in `base.py` and to the `Makefile`.  \n\nIn `base.py` there should also be a `DEFAULT_FROM_EMAIL` and a `DEFAULT_TO_EMAIL`. This is used by the email sending method.\n\n',
    'author': 'Will-Hoey',
    'author_email': 'will.hoey@giantmade.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-newsletter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
