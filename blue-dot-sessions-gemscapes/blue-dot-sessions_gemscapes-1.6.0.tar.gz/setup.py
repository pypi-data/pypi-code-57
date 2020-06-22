# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gemscapes',
 'gemscapes.audio',
 'gemscapes.color',
 'gemscapes.conversion',
 'gemscapes.image',
 'gemscapes.metadata',
 'gemscapes.pipeline',
 'gemscapes.plotting',
 'gemscapes.svg_tools']

package_data = \
{'': ['*']}

install_requires = \
['colour>=0.1.5,<0.2.0',
 'cython>=0.29.19,<0.30.0',
 'eyeD3>=0.9.5,<0.10.0',
 'numpy>=1.16,<2.0',
 'pillow==6.2.2',
 'pyclipper>=1.1.0,<2.0.0',
 'pysndfile>=1.4.3,<2.0.0',
 'scikit-image>=0.16.2,<0.17.0',
 'toml>=0.10.0,<0.11.0',
 'tqdm>=4.45.0,<5.0.0']

setup_kwargs = {
    'name': 'blue-dot-sessions-gemscapes',
    'version': '1.6.0',
    'description': 'Blue Dot Sessions Gemscape Generation',
    'long_description': None,
    'author': 'Dean Shaff',
    'author_email': 'dean.shaff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
