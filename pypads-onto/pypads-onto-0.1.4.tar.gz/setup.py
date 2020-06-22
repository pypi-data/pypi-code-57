# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypads_onto',
 'pypads_onto.app',
 'pypads_onto.bindings',
 'pypads_onto.bindings.resources',
 'pypads_onto.bindings.resources.mapping',
 'pypads_onto.concepts',
 'pypads_onto.injections',
 'pypads_onto.injections.analysis',
 'pypads_onto.injections.loggers']

package_data = \
{'': ['*']}

install_requires = \
['pypads-padre>=0.2.3,<0.3.0', 'pypads>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'pypads-onto',
    'version': '0.1.4',
    'description': 'PyPads_Onto is an extension introducing ontology information. It will be used for semantic harmonization.',
    'long_description': '\n# PyPaDS-Onto\n\n[![Documentation Status](https://readthedocs.org/projects/pypads-onto/badge/?version=latest)](https://pypads.readthedocs.io/projects/pypads-onto/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/pypads-onto.svg)](https://badge.fury.io/py/pypads-onto)\n![Build status](https://gitlab.padim.fim.uni-passau.de/RP-17-PaDReP/padre-onto/badges/master/pipeline.svg)\n\nThis is the Ontology extension to pypads framework. It will be used for semantic harmonization.',
    'author': 'Thomas Weißgerber',
    'author_email': 'thomas.weissgerber@uni-passau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.padre-lab.eu/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
