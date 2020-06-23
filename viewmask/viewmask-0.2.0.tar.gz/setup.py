# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viewmask']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.2,<8.0.0',
 'click>=7.1.2,<8.0.0',
 'dask-image>=0.3.0,<0.4.0',
 'napari[pyside2]>=0.3.4,<0.4.0',
 'numpy>=1.18.4,<2.0.0',
 'opencv-python-headless>=4.2.0,<5.0.0',
 'openslide-python>=1.1.1,<2.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'toolz>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['viewmask = viewmask.cli:cli']}

setup_kwargs = {
    'name': 'viewmask',
    'version': '0.2.0',
    'description': 'A Python package and CLI to view XML annotations and NumPy masks.',
    'long_description': 'viewmask\n========\nA Python package and CLI to view XML annotations and NumPy masks.\n\n|PyPI version fury.io|\n|PyPI downloads|\n|HitCount|\n|Documentation Status|\n|Travis build|\n|PyPI license|\n\n.. |PyPI version fury.io| image:: https://badge.fury.io/py/viewmask.svg\n   :target: https://pypi.python.org/pypi/viewmask/\n\n.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/viewmask\n   :target: https://pypistats.org/packages/viewmask\n\n.. |HitCount| image:: https://hits.dwyl.com/sumanthratna/viewmask.svg\n   :target: https://hits.dwyl.com/sumanthratna/viewmask\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/viewmask/badge/?version=latest\n   :target: https://viewmask.readthedocs.io/?badge=latest\n\n.. |Travis build| image:: https://travis-ci.com/sumanthratna/viewmask.svg?branch=master\n   :target: https://travis-ci.com/sumanthratna/viewmask\n\n.. |PyPI license| image:: https://img.shields.io/pypi/l/viewmask.svg\n   :target: https://pypi.python.org/pypi/viewmask/\n\nInstallation\n============\n\npip\n------------\n::\n\n python3 -m pip install --upgrade pip\n python3 -m pip install viewmask\n\nor:\n::\n\n python3 -m pip install --upgrade pip\n python3 -m pip install git+git://github.com/sumanthratna/viewmask.git#egg=viewmask\n\nPoetry\n------------\n::\n\n poetry run python -m pip install --upgrade pip\n poetry add viewmask\n\nor:\n::\n\n poetry run python -m pip install --upgrade pip\n poetry add git+https://github.com/sumanthratna/viewmask.git\n',
    'author': 'sumanthratna',
    'author_email': 'sumanthratna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumanthratna/viewmask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
