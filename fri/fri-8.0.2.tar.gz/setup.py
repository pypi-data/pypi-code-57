# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fri', 'fri.model', 'fri.tests']

package_data = \
{'': ['*']}

install_requires = \
['arfs-gen>=1,<2',
 'cvxpy>=1.0,<1.2',
 'ecos>=2.0.7,<3.0.0',
 'joblib>=0.14,<0.16',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.17,<2.0',
 'scikit-learn>=0.23,<0.24',
 'scipy>=1.0,<2.0']

setup_kwargs = {
    'name': 'fri',
    'version': '8.0.2',
    'description': 'Implementation of Feature Relevance Bounds method to perform Feature Selection and further analysis.',
    'long_description': '# Feature Relevance Intervals - FRI\n\n![Feature Relevance Intervals - FRI](docs/relevancebars.png)\n\n\n![Travis (.org)](https://img.shields.io/travis/lpfann/fri)\n![Coveralls github](https://img.shields.io/coveralls/github/lpfann/fri)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1188749.svg)](https://doi.org/10.5281/zenodo.1188749)\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lpfann/fri/blob/master/doc/source/notebooks/Guide.ipynb)\n![PyPI](https://img.shields.io/pypi/v/fri)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fri)\n![GitHub](https://img.shields.io/github/license/lpfann/fri)\n\n__FRI__ is a Python 3 package for analytical feature selection\npurposes. It allows superior feature selection in the sense that all\nimportant features are conserved. At the moment we support multiple\nlinear models for solving Classification, Regression and Ordinal\nRegression Problems. We also support LUPI paradigm where at learning\ntime, privileged information is available.\n\n# Usage\nPlease refer to the [documentation](https://lpfann.github.io/fri/) for advice.\nFor a quick start we provide a simple guide which leads through the main functions.\n\n## Installation\n`FRI` requires __Python 3.6+__. \n\nFor a __stable__ version from `PyPI` use\n```shell\n$ pip install fri\n```\nor with new versions of `pip` (>=19?) you can clone the repository and run\n```shell\n$ pip install .\n```\nin the folder on the `master` or `dev` branch.\n## Documentation\nCheck out our online documentation [here](https://lpfann.github.io/fri/).\nThere you can find a quick start guide and more background information.\n\nYou can also run the guide directly online without setup [here](https://colab.research.google.com/github/lpfann/fri/blob/master/doc/source/notebooks/Guide.ipynb).\n\n\n\n\n# Development\nFor dependency management we use the newly released [poetry](https://python-poetry.org/) tool.\n\nIf you have `poetry` installed, use\n```shell\n$ poetry install\n```  \ninside the project folder to create a new `venv` and to install all dependencies.\nTo enter the newly created `venv` use \n```shell \n$ poetry env\n```\nto open a new shell inside.\nOr alternatively run commands inside the `venv` with `poetry run ...`.\n\n#### Docs\nThe [documentation](https://lpfann.github.io/fri/) is compiled using [portray](https://github.com/timothycrosley/portray/).\nIf the dependencies are installed with `poetry install` you should be able to run \n```shell\n$ poetry run portray in_browser\n```\nto compile the files into html and launch a browser to preview changes.\n\n(Be sure not to mix up `poetry` != `portray`.)\n\nThe documentation files are generated from `Python` docstrings inside the source files\n and from Markdown located in the `docs` folder.\n \n\n## References  \n\n[1] Göpfert C, Pfannschmidt L, Hammer B. Feature Relevance Bounds for Linear Classification. In: Proceedings of the ESANN. 25th European Symposium on Artificial Neural Networks, Computational Intelligence and Machine Learning;\n<https://pub.uni-bielefeld.de/publication/2908201>\n\n[2] Göpfert C, Pfannschmidt L, Göpfert JP, Hammer B. Interpretation of Linear Classifiers by Means of Feature Relevance Bounds. Neurocomputing.\n<https://pub.uni-bielefeld.de/publication/2915273>\n\n[3] Lukas Pfannschmidt, Jonathan Jakob, Michael Biehl, Peter Tino, Barbara Hammer: Feature Relevance Bounds for Ordinal Regression. Proceedings of the ESANN. 27th European Symposium on Artificial Neural Networks, Computational Intelligence and Machine Learning; Accepted.\n<https://pub.uni-bielefeld.de/record/2933893>\n\n[4] Pfannschmidt L, Göpfert C, Neumann U, Heider D, Hammer B: FRI - Feature Relevance Intervals for Interpretable and Interactive Data Exploration. Presented at the 16th IEEE International Conference on Computational Intelligence in Bioinformatics and Computational Biology, Certosa di Pontignano, Siena - Tuscany, Italy. <https://ieeexplore.ieee.org/document/8791489>\n',
    'author': 'Lukas Pfannschmidt',
    'author_email': 'lukas@lpfann.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fri.lpfann.me',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
