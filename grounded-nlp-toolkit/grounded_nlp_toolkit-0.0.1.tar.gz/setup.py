# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grounded_nlp_toolkit']

package_data = \
{'': ['*']}

install_requires = \
['nltk>=3.5,<4.0', 'spacy>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'grounded-nlp-toolkit',
    'version': '0.0.1',
    'description': 'This is the alpha version of a library for NLP, especially Image Captioning, Information Retrieval and Text Analysis.',
    'long_description': None,
    'author': 'Robin',
    'author_email': 'rojowiec@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
