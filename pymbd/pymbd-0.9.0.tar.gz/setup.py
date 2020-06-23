# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymbd']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1,<=1.15', 'scipy>=1,<2']

extras_require = \
{'mpi': ['mpi4py>=3,<4'], 'test': ['pytest>=5,<6']}

setup_kwargs = {
    'name': 'pymbd',
    'version': '0.9.0',
    'description': 'Many-body dispersion library',
    'long_description': "# Libmbd\n\n[![build](https://img.shields.io/travis/jhrmnn/libmbd/master.svg)](https://travis-ci.org/jhrmnn/libmbd)\n[![coverage](https://img.shields.io/codecov/c/github/jhrmnn/libmbd.svg)](https://codecov.io/gh/jhrmnn/libmbd)\n![python](https://img.shields.io/pypi/pyversions/pymbd.svg)\n[![release](https://img.shields.io/github/release/jhrmnn/libmbd.svg)](https://github.com/jhrmnn/libmbd/releases)\n[![conda](https://img.shields.io/conda/v/libmbd/pymbd.svg)](https://anaconda.org/libmbd/pymbd)\n[![pypi](https://img.shields.io/pypi/v/pymbd.svg)](https://pypi.org/project/pymbd/)\n[![commits since](https://img.shields.io/github/commits-since/jhrmnn/libmbd/latest.svg)](https://github.com/jhrmnn/libmbd/releases)\n[![last commit](https://img.shields.io/github/last-commit/jhrmnn/libmbd.svg)](https://github.com/jhrmnn/libmbd/commits/master)\n[![license](https://img.shields.io/github/license/jhrmnn/libmbd.svg)](https://github.com/jhrmnn/libmbd/blob/master/LICENSE)\n[![code style](https://img.shields.io/badge/code%20style-black-202020.svg)](https://github.com/ambv/black)\n\nLibmbd contains implementations of the [many-body dispersion](http://dx.doi.org/10.1063/1.4865104) (MBD) method in several programming languages and frameworks:\n\n- The Fortran implementation is the reference, most advanced implementation, with support for analytical gradients and distributed parallelism, and additional functionality beyond the MBD method itself. It provides a low-level and a high-level Fortran API, and a C API. Furthermore, Python bindings to the C API are provided.\n- The Python/Numpy implementation is intended for prototyping, and as a high-level language reference.\n- The Python/Tensorflow implementation is an experiment that should enable rapid prototyping of machine learning applications with MBD.\n\nThe Python-based implementations as well as Python bindings to the Libmbd C API are accessible from the Python package called Pymbd.\n\n## Installing Pymbd\n\nThe easiest way to get Pymbd is to install the Pymbd [Conda](https://conda.io/docs/) package, which ships with pre-built Libmbd.\n\n```\nconda install -c libmbd pymbd\n```\n\nAlternatively, if you have Libmbd installed on your system (see below), you can install Pymbd via Pip, in which case it links against the installed Libmbd. To support Libmbd built with ScaLAPACK/MPI, the `mpi` extras is required.\n\n```\npip install pymbd  # or pymbd[mpi]\n```\n\nIf you don’t need the Fortran bindings in Pymbd, you can install it without the C extension, in which case `pymbd.fortran` becomes unimportable:\n\n```\nenv LIBMBD_PREFIX= pip install pymbd\n```\n\n## Installing Libmbd\n\nLibmbd uses CMake for building and installation, and requires a Fortran compiler, LAPACK, and optionally ScaLAPACK/MPI.\n\nOn Ubuntu:\n\n```bash\napt-get install gfortran libblas-dev liblapack-dev [mpi-default-dev mpi-default-bin libscalapack-mpi-dev]\n```\n\nOn macOS:\n\n```bash\nbrew install gcc [open-mpi scalapack]\n```\n\nThe building and installation can then proceed with\n\n```\ngit clone https://github.com/jhrmnn/libmbd.git && cd libmbd\nmkdir build && cd build\ncmake .. [-DENABLE_SCALAPACK_MPI=ON]\nmake\nmake install\n```\n\nThis installs the Libmbd shared library, C API header file, and high-level Fortran API module file.\n\nTests can be run with\n\n```\nmake check\n```\n\n## Examples\n\n```python\nfrom pymbd import mbd_energy_species, ang\nfrom pymbd.fortran import MBDCalc\n\nene_py = mbd_energy_species(  # pure Python implementation\n    [(0, 0, 0), (0, 0, 4*ang)], ['Ar', 'Ar'], [1, 1], 0.83\n)\nwith MBDCalc() as calc:\n    ene_f = calc.mbd_energy_species(  # Fortran implementation\n        [(0, 0, 0), (0, 0, 4*ang)], ['Ar', 'Ar'], [1, 1], 0.83\n    )\nassert abs(ene_f-ene_py) < 1e-15\n```\n\n```fortran\nuse mbd, only: mbd_input_t, mbd_calc_t\n\ntype(mbd_input_t) :: inp\ntype(mbd_calc_t) :: calc\nreal(8) :: energy, gradients(3, 2)\ninteger :: code\ncharacter(200) :: origin, msg\n\ninp%atom_types = ['Ar', 'Ar']\ninp%coords = reshape([0d0, 0d0, 0d0, 0d0, 0d0, 7.5d0], [3, 2])\ninp%xc = 'pbe'\ncall calc%init(inp)\ncall calc%get_exception(code, origin, msg)\nif (code > 0) then\n    print *, msg\n    stop\nend if\ncall calc%update_vdw_params_from_ratios([0.98d0, 0.98d0])\ncall calc%evaluate_vdw_method(energy)\ncall calc%get_gradients(gradients)\ncall calc%destroy()\n```\n\n## Links\n\n- Libmbd documentation: https://jhrmnn.github.io/libmbd\n- Pymbd documentation: https://jhrmnn.github.io/libmbd/pymbd\n\n## Developing\n\nFor development, Libmbd doesn't have to be installed on the system, and Pymbd can be linked against local installation of Libmbd.\n\n```\ngit clone https://github.com/jhrmnn/libmbd.git && cd libmbd\npython3 -m venv venv && source venv/bin/activate\nmake\n# development work...\nmake\n```\n",
    'author': 'Jan Hermann',
    'author_email': 'dev@jan.hermann.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jhrmnn/libmbd',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
