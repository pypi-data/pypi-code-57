# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['estimark',
 'estimark.application',
 'estimark.application.domain',
 'estimark.application.domain.common',
 'estimark.application.domain.models',
 'estimark.application.domain.repositories',
 'estimark.application.domain.services',
 'estimark.application.informers',
 'estimark.application.managers',
 'estimark.core',
 'estimark.core.common',
 'estimark.core.data',
 'estimark.core.data.json',
 'estimark.core.plot',
 'estimark.factories',
 'estimark.factories.strategies',
 'estimark.presenters',
 'estimark.presenters.shell']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.1.0,<5.0.0', 'docutils>=0.16,<0.17', 'injectark>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['estimark = estimark.__main__:main']}

setup_kwargs = {
    'name': 'estimark',
    'version': '0.3.0',
    'description': 'Frictionless Estimation',
    'long_description': None,
    'author': 'Esteban Echeverry',
    'author_email': 'eecheverry@knowark.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
