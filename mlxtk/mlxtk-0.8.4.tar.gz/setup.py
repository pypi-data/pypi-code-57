# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mlxtk',
 'mlxtk.doit_analyses',
 'mlxtk.inout',
 'mlxtk.operator',
 'mlxtk.plot',
 'mlxtk.scripts',
 'mlxtk.scripts.plot',
 'mlxtk.scripts.scan_plot',
 'mlxtk.scripts.slider',
 'mlxtk.simulation',
 'mlxtk.simulation_set',
 'mlxtk.systems',
 'mlxtk.systems.single_species',
 'mlxtk.tasks',
 'mlxtk.templates',
 'mlxtk.tools',
 'mlxtk.ui']

package_data = \
{'': ['*'], 'mlxtk.scripts': ['animate/*', 'compute/*']}

install_requires = \
['colorama==0.4.3',
 'doit==0.32',
 'future==0.18.2',
 'h5py==2.10',
 'jinja2==2.11.2',
 'matplotlib==3.2.2',
 'numpy-stl==2.11.2',
 'numpy==1.18.5',
 'pandas==1.0.4',
 'pathos==0.2.6',
 'prompt-toolkit==3.0.5',
 'pyside2==5.15.0',
 'pyyaml==5.3.1',
 'scipy==1.4.1',
 'sympy==1.6',
 'tabulate==0.8.7',
 'tqdm==4.46.1']

entry_points = \
{'console_scripts': ['animate_dmat = mlxtk.scripts.animate.dmat:main',
                     'animate_dmat2 = mlxtk.scripts.animate.dmat2:main',
                     'animate_g1 = mlxtk.scripts.animate.g1:main',
                     'animate_g2 = mlxtk.scripts.animate.g2:main',
                     'animate_gpop = mlxtk.scripts.animate.gpop:main',
                     'compute_dmat = mlxtk.scripts.compute.dmat:main',
                     'compute_dmat2 = mlxtk.scripts.compute.dmat2:main',
                     'compute_g1 = mlxtk.scripts.compute.g1:main',
                     'compute_g2 = mlxtk.scripts.compute.g2:main',
                     'create_slideshow = mlxtk.scripts.create_slideshow:main',
                     'dmat2_gridrep = mlxtk.scripts.dmat2_gridrep:main',
                     'dmat2_gridrep_video = '
                     'mlxtk.scripts.dmat2_gridrep_video:main',
                     'dmat_evec_slider = mlxtk.scripts.dmat_evec_slider:main',
                     'dmat_spf_slider = mlxtk.scripts.dmat_spf_slider:main',
                     'fixed_ns = mlxtk.scripts.fixed_ns:main',
                     'fixed_ns_table = mlxtk.scripts.fixed_ns_table:main',
                     'gpop_model = mlxtk.scripts.gpop_model:main',
                     'grab_1b_eigenfunction = '
                     'mlxtk.scripts.grab_1b_eigenfunction:main',
                     'grab_spfs = mlxtk.scripts.grab_spfs:main',
                     'mlxtkenv = mlxtkenv_script:main',
                     'plot_energy = mlxtk.scripts.plot.energy:main',
                     'plot_energy_diff = mlxtk.scripts.plot.energy_diff:main',
                     'plot_entropy = mlxtk.scripts.plot.entropy:main',
                     'plot_entropy_diff = mlxtk.scripts.plot.entropy_diff:main',
                     'plot_expval = mlxtk.scripts.plot.expval:main',
                     'plot_gpop = mlxtk.scripts.plot.gpop:main',
                     'plot_natpop = mlxtk.scripts.plot.natpop:main',
                     'plot_natpop_vs_dmat_evals = '
                     'mlxtk.scripts.plot.natpop_vs_dmat_evals:main',
                     'plot_spfs = mlxtk.scripts.plot.spfs:main',
                     'plot_spfs_vs_norbs = '
                     'mlxtk.scripts.plot.spfs_vs_norbs:main',
                     'print_unit_system = mlxtk.scripts.print_unit_system:main',
                     'recreate_output = mlxtk.scripts.recreate_output:main',
                     'scan_plot_depletion = '
                     'mlxtk.scripts.scan_plot.depletion:main',
                     'scan_plot_energy = mlxtk.scripts.scan_plot.energy:main',
                     'scan_plot_expval = mlxtk.scripts.scan_plot.expval:main',
                     'scan_plot_gpop = mlxtk.scripts.scan_plot.gpop:main',
                     'scan_plot_natpop = mlxtk.scripts.scan_plot.natpop:main',
                     'slider_dmat2_gridrep = '
                     'mlxtk.scripts.slider.dmat2_gridrep:main',
                     'slider_dmat2_spfrep = '
                     'mlxtk.scripts.slider.dmat2_spfrep:main',
                     'slider_dmat_gridrep = '
                     'mlxtk.scripts.slider.dmat_gridrep:main',
                     'slider_dmat_spfrep = '
                     'mlxtk.scripts.slider.dmat_spfrep:main',
                     'slider_g1 = mlxtk.scripts.slider.g1:main',
                     'slider_g2 = mlxtk.scripts.slider.g2:main',
                     'slider_gpop = mlxtk.scripts.slider.gpop:main',
                     'spectrum_1b = mlxtk.scripts.spectrum_1b:main',
                     'thin_out_psi = mlxtk.scripts.thin_out_psi:main']}

setup_kwargs = {
    'name': 'mlxtk',
    'version': '0.8.4',
    'description': 'Toolkit to design, run and analyze ML-MCTDH(X) simulations',
    'long_description': 'mlxtk\n=====\n![PyPI](https://img.shields.io/pypi/v/mlxtk)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mlxtk)\n![PyPI - License](https://img.shields.io/pypi/l/mlxtk)\n[![Updates](https://pyup.io/repos/github/f-koehler/mlxtk/shield.svg)](https://pyup.io/repos/github/f-koehler/mlxtk/)\n[![Python 3](https://pyup.io/repos/github/f-koehler/mlxtk/python-3-shield.svg)](https://pyup.io/repos/github/f-koehler/mlxtk/)\n\nToolkit to design, run and analyze ML-MCTDH(X) simulations\n\nDescription\n-----------\nmlxtk gives the user a simple interface to setup physical systems and provides\ncommon simulation tasks to be used as building blocks to set up rather complex\nsimulations. Data is automatically stored in efficient formats (i.e. HDF5 and\ngzipped files).\n\nSimulations can also be used in the context of parameter scans where each\nsimulation is executed for each specified parameter combination. Submission\nof simulation jobs to computing clusters is easily achieved from the command\nline.\n\nFurthermore, analysis and plotting tools are provided to interpret the\nsimulation outcome.\n',
    'author': 'Fabian Köhler',
    'author_email': 'fkoehler@physnet.uni-hamburg.de',
    'url': 'https://github.com/f-koehler/mlxtk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.9',
}


setup(**setup_kwargs)
