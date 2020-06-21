# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fs', 'fs.googledrivefs']

package_data = \
{'': ['*']}

install_requires = \
['fs>=2.4.10', 'google-api-python-client>=1.6.3', 'google-auth>=1.5.1']

entry_points = \
{'fs.opener': ['googledrive = fs.googledrivefs.opener:GoogleDriveFSOpener']}

setup_kwargs = {
    'name': 'fs.googledrivefs',
    'version': '1.5.0',
    'description': 'Pyfilesystem2 implementation for Google Drive',
    'long_description': '# fs.googledrivefs\n\n[![Builds](https://travis-ci.org/rkhwaja/fs.googledrivefs.svg?branch=master "CI status")](https://travis-ci.org/rkhwaja/fs.googledrivefs) [![Coverage report](https://coveralls.io/repos/github/rkhwaja/fs.googledrivefs/badge.svg?branch=master "Coverage summary")](https://coveralls.io/github/rkhwaja/fs.googledrivefs?branch=master) [![PyPI version](https://badge.fury.io/py/fs.googledrivefs.svg)](https://badge.fury.io/py/fs.googledrivefs)\n\nImplementation of [pyfilesystem2](https://docs.pyfilesystem.org/) file system for Google Drive\n\n# Usage\n\n```python\n  fs = GoogleDriveFS(credentials=<google-auth credentials>)\n\n  # fs is now a standard pyfilesystem2 file system\n\n  fs2 = open_fs("googledrive:///?access_token=<oauth2 access token>&refresh_token=<oauth2 refresh token>&client_id=<oauth2 client id>&client_secret=<oauth2 client secret>")\n\n  # fs2 is now a standard pyfilesystem2 file system\n```\n\n# Running tests\n\nTo run the tests, set the following environment variables:\n\n- GOOGLEDRIVEFS_TEST_CREDENTIALS_PATH - path to a json file which will contain the credentials\n- GOOGLEDRIVEFS_TEST_CLIENT_ID - your client id (see Google Developer Console)\n- GOOGLEDRIVEFS_TEST_CLIENT_SECRET - your client secret (see Google Developer Console)\n\nThen generate the credentials json file by running\n\n```bash\n  python generate-credentials.py\n```\n\nThen run the tests by executing\n\n```bash\n  pytest\n```\n\nin the root directory. The tests may take an hour or two to complete. They create and destroy many, many files and directories mostly under the /test-googledrivefs directory in the user\'s Google Drive and a few in the root directory\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rkhwaja/fs.googledrivefs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
