# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysm3',
 'pysm3.data',
 'pysm3.extern',
 'pysm3.models',
 'pysm3.tests',
 'pysm3.utils',
 'pysm3.utils.tests']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0.1,<5.0.0',
 'healpy>=1.13.0,<2.0.0',
 'numba>=0.49.1,<0.50.0',
 'numpy>=1.17,<2.0',
 'toml>=0.10.1,<0.11.0']

extras_require = \
{':python_version == "3.6"': ['importlib_resources>=2.0.1,<3.0.0'],
 'docs': ['sphinx>=3.0.4,<4.0.0',
          'sphinx-astropy>=1.3,<2.0',
          'nbsphinx>=0.7.0,<0.8.0',
          'sphinx-math-dollar>=1.1.1,<2.0.0',
          'pandoc>=1.0.2,<2.0.0',
          'ipykernel>=5.3.0,<6.0.0'],
 'test': ['pytest>=5.4.3,<6.0.0',
          'pytest-astropy>=0.8.0,<0.9.0',
          'mpi4py>=3.0.3,<4.0.0',
          'tox>=3.15.1,<4.0.0']}

setup_kwargs = {
    'name': 'pysm3',
    'version': '3.2.2',
    'description': 'PySM generates full-sky simulations of Galactic emissions in intensity and polarization relevant to CMB experiments',
    'long_description': '|Build Status| |Documentation Status| |PyPI| |Conda| |Astropy|\n\nPySM 3\n======\n\nPySM generates full-sky simulations of Galactic emissions in intensity\nand polarization relevant to CMB experiments. It is a large refactor of\n`PySM 2 <https://github.com/bthorne93/PySM_public>`__ focused on\nreducing memory usage, improving performance and run in parallel with\nMPI.\n\nSee the documentation at https://pysm3.readthedocs.io\n\n* Install with `pip install .` or use `poetry`\n* Check code style with ``tox -e codestyle``\n* Test with ``pytest`` or ``tox -e test``\n* Build docs locally with ``tox -e build_docs``\n\nSee changes in ``CHANGES.rst`` in the repository.\n\nInstall\n-------\n\nSee the `documentation <https://pysm3.readthedocs.io/en/latest/#installation>`_\n\nRelease\n-------\n\nFollow the `Astropy guide to release a new version <https://docs.astropy.org/en/stable/development/astropy-package-template.html>`.\n\n.. |Build Status| image:: https://travis-ci.org/healpy/pysm.svg?branch=master\n   :target: https://travis-ci.org/healpy/pysm\n.. |Documentation Status| image:: https://readthedocs.org/projects/pysm3/badge/?version=latest\n   :target: https://pysm3.readthedocs.io/en/latest/?badge=latest\n.. |PyPI| image:: https://img.shields.io/pypi/v/pysm3\n   :target: https://pypi.org/project/pysm3/\n.. |Conda| image:: https://img.shields.io/conda/vn/conda-forge/pysm3\n   :target: https://anaconda.org/conda-forge/pysm3\n.. |Astropy| image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat\n   :target: http://www.astropy.org/\n',
    'author': 'Andrea Zonca',
    'author_email': 'code@andreazonca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/healpy/pysm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
