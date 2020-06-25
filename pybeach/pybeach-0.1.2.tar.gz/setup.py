# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybeach', 'pybeach.support']

package_data = \
{'': ['*'],
 'pybeach': ['classifiers/barrier_island_clf.joblib',
             'classifiers/barrier_island_clf.joblib',
             'classifiers/barrier_island_clf.joblib',
             'classifiers/mixed_clf.joblib',
             'classifiers/mixed_clf.joblib',
             'classifiers/mixed_clf.joblib',
             'classifiers/wave_embayed_clf.joblib',
             'classifiers/wave_embayed_clf.joblib',
             'classifiers/wave_embayed_clf.joblib']}

install_requires = \
['joblib==0.13.2',
 'numpy==1.17.2',
 'pandas==0.25.1',
 'scikit-learn==0.21.2',
 'scipy==1.3.1']

setup_kwargs = {
    'name': 'pybeach',
    'version': '0.1.2',
    'description': 'A Python package for locating the dune toe on cross-shore beach profile transects.',
    'long_description': '[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Documentation Status](https://readthedocs.org/projects/pybeach/badge/?version=latest)](https://pybeach.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/TomasBeuzen/pybeach/branch/master/graph/badge.svg)](https://codecov.io/gh/TomasBeuzen/pybeach)\n[![status](https://joss.theoj.org/papers/8b211e45c6919ea8057946484e757c28/status.svg)](https://joss.theoj.org/papers/8b211e45c6919ea8057946484e757c28)\n[![PyPI version](https://badge.fury.io/py/pybeach.svg)](https://badge.fury.io/py/pybeach)\n\n# **pybeach**: A Python package for locating the dune toe on cross-shore beach profile transects.\n\n<div align="center">\n  <img src="https://raw.githubusercontent.com/TomasBeuzen/pybeach/master/docs/img/figure_1.png" alt="pybeach-example" width="700"/>\n</div>\n\n## Background\n**pybeach** is a Python package for identifying dune toes on 2D beach profile transects. It includes the following methods:\n  - Machine learning; \n  - Maximum curvature (Stockdon et al, 2007); \n  - Relative relief (Wernette et al, 2016); and,\n  - Perpendicular distance.\n  \nIn addition, **pybeach** contains methods for identifying the shoreline position and dune crest position on 2D beach profile transects. See the [*pybeach* paper](paper.md) for more details about **pybeach**.\n\n## Installation\n\n`pip install pybeach`\n\n## Usage\n```python\nfrom pybeach.beach import Profile\n\n# example data\nx = np.arange(0, 80, 0.5)\nz = np.concatenate((np.linspace(4, 5, 40),\n                    np.linspace(5, 2, 10),\n                    np.linspace(2, 0, 91)[1:],\n                    np.linspace(0, -1, 20)))\n\n# instantiate\np = Profile(x, z)\n\n# predict dune toe, dune crest, shoreline location\ntoe_ml, prob_ml = p.predict_dunetoe_ml(\'wave_embayed_clf\')  # predict toe using machine learning model\ntoe_mc = p.predict_dunetoe_mc()    # predict toe using maximum curvature method (Stockdon et al, 2007)\ntoe_rr = p.predict_dunetoe_rr()    # predict toe using relative relief method (Wernette et al, 2016)\ntoe_pd = p.predict_dunetoe_pd()    # predict toe using perpendicular distance method\ncrest = p.predict_dunecrest()      # predict dune crest\nshoreline = p.predict_shoreline()  # predict shoreline\n```\n\nSee the [example notebook](https://github.com/TomasBeuzen/pybeach/blob/master/example/example.ipynb) for more details.\n\n## Documentation\nRead the **pybeach** documentation [here](https://pybeach.readthedocs.io/en/latest/).\n\n## Dependencies\nA list of **pybeach** dependencies can be found in [pyproject.toml](https://github.com/TomasBeuzen/pybeach/blob/master/pyproject.toml). Currently, **pybeach** depends on the following:\n- python = "^3.7"\n- numpy = "1.17.2"\n- scipy = "1.3.1"\n- pandas = "0.25.1"\n- scikit-learn = "0.21.2"\n- joblib = "0.13.2"\n\n## Questions, Comments, Suggestions\nDo you have a question that needs answering? Have you found an issue with the code and need to get it fixed? Or perhaps you\'re looking to contribute to the code and have ideas for how it could be improved. In all cases, please see the [Issues](https://github.com/TomasBeuzen/pybeach/issues) page.\n\n## References\nStockdon, H. F., Sallenger Jr, A. H., Holman, R. A., & Howd, P. A. (2007). A simple model for the spatially-variable coastal response to hurricanes. Marine Geology, 238, 1-20. https://doi.org/10.1016/j.margeo.2006.11.004\n\nWernette, P., Houser, C., & Bishop, M. P. (2016). An automated approach for extracting Barrier Island morphology from digital elevation models. Geomorphology, 262, 1-7. https://doi.org/10.1016/j.geomorph.2016.02.024\n',
    'author': 'Tomas Beuzen',
    'author_email': 'tomas.beuzen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TomasBeuzen/pybeach',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
