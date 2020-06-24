# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chime_frb_constants']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chime-frb-constants',
    'version': '2020.6.1',
    'description': 'CHIME/FRB Constants',
    'long_description': '# CHIME/FRB Constants\n\nConstants is a is pure-python, light-weight and a dependency-less package to access the commonly used variables in the CHIME/FRB software projects.\n\n## Installation\n```\npip install chime-frb-constants\n```\n\n## Usage\n```python\nimport chime_frb_constants as constants\n\nprint constants.K_DM\n```\n\n',
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CHIMEFRB/frb-constants',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
