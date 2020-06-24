# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mixins', 'mixins.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'giant-mixins',
    'version': '0.1.1.3',
    'description': 'A mixins app that provides some standard mixins for Giant projects',
    'long_description': 'Giant Mixins\n===================\nA small, re-usable package which can be used in any project that requires mixins (which is 99% of them)\nThis will include the standard mixins such as TimestampMixin, PublishingMixin and YoutubeURLMixin\n\nInstallation\n===================\n\nTo install with the package manager simply run\n\n    $ poetry add giant-mixins\n\nYou should then add `"mixins"` to the `INSTALLED_APPS` in `base.py`. \n\n',
    'author': 'Will-Hoey',
    'author_email': 'will.hoey@giantmade.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-mixins',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
