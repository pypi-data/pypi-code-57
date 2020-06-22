# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toggl_python']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.13.3,<0.14.0', 'pydantic[email]>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'toggl-python',
    'version': '0.1.0',
    'description': 'Python wraper for Toggl API.',
    'long_description': None,
    'author': 'Ivlev Denis',
    'author_email': 'me@dierz.pro',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
