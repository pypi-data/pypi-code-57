# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['errorpages']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'giant-errorpages',
    'version': '0.1.0',
    'description': 'A small package to trigger specific non-200 HTTP responses in a Django application.',
    'long_description': '# Giant Error Pages\n\nA small package to trigger specific non-200 HTTP responses. This is useful for previewing your error pages while DEBUG=True. Once enabled, you will be able to access three new routes:\n\n- /errors/404/, which will return a 404 response and error page.\n- /errors/403/, which will return a 403 response and error page.\n- /errors/500/, which will return a 500 response and error page.\n\n## Installation\n\nTo install with Poetry, run:\n\n    $ poetry add giant-errorpages\n\nYou should then add `"errorpages"` to the `INSTALLED_APPS` in your settings file. Finally, update your root `urlpatterns` to include:\n\n    path("errors/", include("errorpages.urls"), name="errorpages"),\n\n## Preparing for release\n \nIn order to prepare the package for a new release on TestPyPi and PyPi, you need to update the version number in the `pyproject.toml`. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.\n \n## Publishing\n \nOnce the version number has been updated, run:\n \n   $ `poetry build` \n\nThis will package the project ready for publication:\n\n   $ `poetry publish`\n\n...will then publish the package to PyPi. You will need to enter the username and password for the account which can be found in the company password manager.',
    'author': 'Jon Atkinson',
    'author_email': 'jon@giantmade.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-errorpages',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
