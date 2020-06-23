# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markovgram']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'markovify>=0.7.2,<0.8.0']

entry_points = \
{'console_scripts': ['markovgram = markovgram.__main__:main',
                     'markovgram-merge = markovgram.merge:run',
                     'markovgram-preview = markovgram.preview:run']}

setup_kwargs = {
    'name': 'markovgram',
    'version': '0.3.5',
    'description': 'Parse GDPR-exported Telegram data and create markovify Texts',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
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
