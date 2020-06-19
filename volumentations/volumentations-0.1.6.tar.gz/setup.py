# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volumentations', 'volumentations.augmentations', 'volumentations.core']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.6.0,<2.0.0',
 'numpy>=1.18.3,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'volumentations',
    'version': '0.1.6',
    'description': 'Point augmentations library as hard-fork of albu-team/albumentations',
    'long_description': '[![Tests](https://github.com/kumuji/volumentations/workflows/Tests/badge.svg)](https://github.com/kumuji/volumentations/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/kumuji/volumentations/branch/master/graph/badge.svg)](https://codecov.io/gh/kumuji/volumentations)\n[![PyPI](https://img.shields.io/pypi/v/volumentations.svg)](https://pypi.org/project/volumentations/)\n[![Documentation Status](https://readthedocs.org/projects/volumentations/badge/?version=latest)](https://volumentations.readthedocs.io/en/latest/?badge=latest)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)\n[![Downloads](https://pepy.tech/badge/volumentations)](https://pepy.tech/project/volumentations)\n[![CodeFactor](https://www.codefactor.io/repository/github/kumuji/volumentations/badge)](https://www.codefactor.io/repository/github/kumuji/volumentations)\n[![Maintainability](https://api.codeclimate.com/v1/badges/a3dc1e079290f508bf6f/maintainability)](https://codeclimate.com/github/kumuji/volumentations/maintainability)\n\n\n# ![logo](./docs/logo.png "logo") Volumentations\n\n![augmented_teapot](./docs/augmented_teapot.png "teapot")\n\n\nPython library for 3d data augmentaiton. Hard fork from [alumentations](https://github.com/albumentations-team/albumentations).\n\nFor more information on available augmentations check [documentation](https://volumentations.readthedocs.io/en/latest/index.html).\n\nOr, check simple example in colab:\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1CT9nIGME_M4kIDc3BfEF4pCb_8JdFLpH)\n\n# Setup\n\n`pip install volumentations`\n\n# Usage example\n\n```python\nimport volumentations as V\nimport numpy as np\n\naugmentation = V.Compose(\n    [\n        V.Scale3d(scale_limit=(0.2, 0.2, 0.1), p=0.75),\n        V.OneOrOther(\n            V.Compose(\n                [\n                    V.RotateAroundAxis3d(\n                        rotation_limit=np.pi, axis=(0, 0, 1), always_apply=True\n                    ),\n                    V.RotateAroundAxis3d(\n                        rotation_limit=np.pi / 3, axis=(0, 1, 0), always_apply=True\n                    ),\n                    V.RotateAroundAxis3d(\n                        rotation_limit=np.pi / 3, axis=(1, 0, 0), always_apply=True\n                    ),\n                ],\n                p=1,\n            ),\n            V.Flip3d(axis=(0, 0, 1)),\n        ),\n        V.OneOf(\n            [\n                V.RandomDropout3d(dropout_ratio=0.2, p=0.75),\n                V.RandomDropout3d(dropout_ratio=0.3, p=0.5),\n            ]\n        ),\n    ]\n)\n\naugmented_teapot = augmentation(points=teapot.copy())["points"]\nshow_augmentation(teapot, augmented_teapot)\n```\n',
    'author': 'kumuji',
    'author_email': 'alexey@nekrasov.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kumuji/volumentations',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
