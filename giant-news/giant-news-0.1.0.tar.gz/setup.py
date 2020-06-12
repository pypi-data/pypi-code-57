# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['news', 'news.migrations', 'news.tests']

package_data = \
{'': ['*'], 'news': ['templates/news/*']}

install_requires = \
['django-filer>=1.7.1,<2.0.0', 'giant-mixins>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'giant-news',
    'version': '0.1.0',
    'description': 'A small reusable package that adds a News app to a project',
    'long_description': '# Giant Newsletter\n\nA re-usable package which can be used in any project that requires a generic `News` app. \n\nThis will include the basic formatting and functionality such as model creation via the admin.\n\n## Installation\n\nTo install with the package manager, run:\n\n    $ poetry add giant-news\n\nYou should then add `"news", "easy_thumbnails" and "filer"` to the `INSTALLED_APPS` in `base.py`.  \n\n',
    'author': 'Will-Hoey',
    'author_email': 'will.hoey@giantmade.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-news',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
