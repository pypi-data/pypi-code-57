# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypyp']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0.1,<5.0.0',
 'autoreject>=0.2.1,<0.3.0',
 'joblib>=0.14.1,<0.15.0',
 'matplotlib>=3.2.1,<4.0.0',
 'meshio>=4.0.13,<5.0.0',
 'mne>=0.20.0,<0.21.0',
 'numpy>=1.18.3,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'tqdm>=4.46.0,<5.0.0']

setup_kwargs = {
    'name': 'hypyp',
    'version': '0.2.0a1',
    'description': 'The Hyperscanning Python Pipeline.',
    'long_description': '# HyPyP 🐍〰️🐍\n\nThe **Hy**perscanning **Py**thon **P**ipeline\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/hypyp.svg)](https://pypi.org/project/HyPyP/) <a href="https://travis-ci.org/GHFC/HyPyP"><img src="https://travis-ci.org/GHFC/HyPyP.svg?branch=master"></a> [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![Gitter](https://badges.gitter.im/GHFC/HyPyP.svg)](https://gitter.im/GHFC/HyPyP)\n\n## Contributors\nFlorence BRUN, Anaël AYROLLES, Phoebe CHEN, Amir DJALOVSKI, Yann BEAUXIS, Suzanne DIKKER, Guillaume DUMAS\n\n## Installation\n\n```\npip install HyPyP\n```\n\n## Documentation\n\nHyPyP documentation of all the API functions is available online at [hypyp.readthedocs.io](https://hypyp.readthedocs.io/)\n\nFor getting started with HyPyP, we have designed a little walkthrough: [getting_started.ipynb](https://github.com/GHFC/HyPyP/blob/master/tutorial/getting_started.ipynb)\n\n## API\n\n🛠 [io.py](https://github.com/GHFC/HyPyP/blob/master/hypyp/io.py) — Loaders (Florence, Anaël, Guillaume)\n\n\U0001f9f0 [utils.py](https://github.com/GHFC/HyPyP/blob/master/hypyp/utils.py) — Basic tools (Amir, Florence, Guilaume)\n\n⚙️ [prep.py](https://github.com/GHFC/HyPyP/blob/master/hypyp/prep.py) — Preprocessing (ICA & AutoReject) (Anaël, Florence, Guillaume)\n\n🔠 [analyses.py](https://github.com/GHFC/HyPyP/blob/master/hypyp/analyses.py) — Power spectral density and wide choice of connectivity measures (Phoebe, Suzanne, Florence, Guillaume)\n\n📈 [stats.py](https://github.com/GHFC/HyPyP/blob/master/hypyp/stats.py) — Statistics (permutations & cluster statistics) (Florence, Guillaume)\n\n\U0001f9e0 [viz.py](https://github.com/GHFC/HyPyP/blob/master/hypyp/viz.py) — Inter-brain visualization (Anaël, Amir, Florence, Guillaume)\n\n🎓 [Tutorials](https://github.com/GHFC/HyPyP/tree/master/tutorial) - Examples & documentation (Anaël, Florence, Yann, Guillaume)\n\n## Roadmap\n\n:warning: This is an alpha version and thus should be used with caution. While we have done our best to test all the functionalities, there is no guarantee that the pipeline is entirely bug-free. See Roadmap below for functionalities that will be implemented in the futur.\n\n### Alpha [Spring 2020]\n\nFirst public version with a basic demonstration of the pipeline.\n\nAvailabel functionalities:\n\n[TABLE]\n\n### Beta [Summer 2020]\n\nUpdated version with those functionalities:\n\n[TABLE]\n\n### Release [Fall/Winter 2020]\n\nFull stable version, including functionalities:\n\n[TABLE]\n',
    'author': 'Anaël AYROLLLES',
    'author_email': 'anael.ayrollles@pasteur.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GHFC/HyPyP',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
