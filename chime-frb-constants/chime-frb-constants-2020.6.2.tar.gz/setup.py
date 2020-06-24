# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chime_frb_constants']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chime-frb-constants',
    'version': '2020.6.2',
    'description': 'CHIME/FRB Constants',
    'long_description': '# CHIME/FRB Constants\n\nConstants is a is pure-python, lightweight and zero dependency package to access variables used in the CHIME/FRB software projects.\n\n## Installation\n```\npip install chime-frb-constants\n```\n\n## Usage\n```python\nimport chime_frb_constants as constants\nprint (constants.K_DM)\n```\n\n## Changelog\n### 2020.06.2\n  - `FREQ` and `FREQ_FREQ` availaible once again, but with type changes\n    ```python\n    FREQ: np.array -> FREQ: List[float]\n    FPGA_FREQ: np.array -> FPGA_FREQ: List[float]\n    ```\n### 2020.06\n  - Initial release on [PYPI](https://pypi.org/project/chime-frb-constants/)\n  - All constants are now uppercase\n  - All physical constants from `scipy` are not availaible anymore under constants. If you still need them, import them directly from\n    ```python\n    from scipy import constants as phys_const\n    ```\n  - `FREQ` and `FREQ_FREQ` currently unavailaible.\n\n\n\n',
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CHIMEFRB/frb-constants',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
