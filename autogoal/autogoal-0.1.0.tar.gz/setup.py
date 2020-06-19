# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autogoal',
 'autogoal.contrib',
 'autogoal.contrib.gensim',
 'autogoal.contrib.keras',
 'autogoal.contrib.nltk',
 'autogoal.contrib.re',
 'autogoal.contrib.sklearn',
 'autogoal.contrib.spacy',
 'autogoal.contrib.streamlit',
 'autogoal.contrib.telegram',
 'autogoal.contrib.torch',
 'autogoal.contrib.wikipedia',
 'autogoal.datasets',
 'autogoal.datasets.ehealthkd20',
 'autogoal.grammar',
 'autogoal.kb',
 'autogoal.ml',
 'autogoal.sampling',
 'autogoal.search',
 'autogoal.utils']

package_data = \
{'': ['*'], 'autogoal.datasets': ['data/.gitignore']}

install_requires = \
['black>=19.10b0,<20.0',
 'enlighten>=1.4.0,<2.0.0',
 'fire>=0.2.1,<0.3.0',
 'networkx>=2.4,<3.0',
 'nx_altair>=0.1.4,<0.2.0',
 'psutil>=5.6.7,<6.0.0',
 'pydot>=1.4.1,<2.0.0',
 'pyyaml>=5.2,<6.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'autogoal',
    'version': '0.1.0',
    'description': 'Automatic Generation Optimization And Learning',
    'long_description': '# AutoGOAL\n\n> Automatic Generation, Optimization And Learning\n\n## What is this?\n\nAutoGOAL is a Python library for automatically finding the best way to solve a given task.\nIt has been designed mainly for Automatic Machine Learning (aka [AutoML](https://www.automl.org))\nbut it can be used in any scenario where you have several possible ways (i.e., programs) to solve a given task.\n\n## Installation\n\nInstallation is very simple:\n\n    pip install autogoal\n\nHowever, `autogoal` comes with a bunch of optional dependencies. You can install them all with:\n\n    pip install autogoal[all]\n\nTo fine-pick which dependencies you want, read the [dependencies section](/dependencies/).\n\n## Documentation\n\n### User Guide\n\nThe step-by-step [User Guide](/guide/quickstart) will show you everything you need to know to use AuoGOAL.\n\n### Examples\n\nLooking at the [examples](/examples/) is the best way to learn how to use AutoGOAL:\n\n- [Finding the best scikit-learn pipeline for classifying movie reviews](/examples/sklearn_simple_grammar/)\n- [Finding the best neural network for a dataset](/examples/keras_text_classifier/)\n\n### API\n\nThe [API documentation](/api) details the public API for AutoGOAL.\n\nIn its core, AutoGOAL is an evolutionary program synthesis framework. It consists\nof two main components:\n\n1. The [grammar](autogoal/grammar) module contains tools to design context-free and graph grammars that describe the space of all possible solutions to a specific problem.\n2. The [search](autogoal/search) module contains tools for automatically exploring this vast space efficiently.\n\n## Contribution\n\nCode is licensed under MIT. Read the details in the [collaboration section](/contributing).\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
