# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['vibes',
 'vibes.ase',
 'vibes.ase.db',
 'vibes.ase.md',
 'vibes.calculator',
 'vibes.cli',
 'vibes.cli.scripts',
 'vibes.fireworks',
 'vibes.fireworks.cli',
 'vibes.fireworks.tasks',
 'vibes.fireworks.tasks.fw_out',
 'vibes.fireworks.tasks.postprocess',
 'vibes.fireworks.utils',
 'vibes.fireworks.workflows',
 'vibes.green_kubo',
 'vibes.harmonic_analysis',
 'vibes.helpers',
 'vibes.helpers.sobol',
 'vibes.helpers.supercell',
 'vibes.hiphive',
 'vibes.k_grid',
 'vibes.konstanten',
 'vibes.materials_fp',
 'vibes.molecular_dynamics',
 'vibes.phono3py',
 'vibes.phonopy',
 'vibes.relaxation',
 'vibes.slurm',
 'vibes.spglib',
 'vibes.structure',
 'vibes.tasks',
 'vibes.tdep',
 'vibes.templates',
 'vibes.templates.config_files',
 'vibes.templates.settings',
 'vibes.trajectory']

package_data = \
{'': ['*'], 'vibes.cli.scripts': ['run/*']}

install_requires = \
['ase>=3.19.0,<4.0.0',
 'attrs>=19.1,<20.0',
 'click>=7.0,<8.0',
 'click_aliases>=1.0,<2.0',
 'click_completion>=0.5.2,<0.6.0',
 'jconfigparser>=0.1.2,<0.2.0',
 'jinja2>=2.10,<3.0',
 'matplotlib>=3.1,<4.0',
 'netCDF4>=1.5,<2.0',
 'numpy>=1.11,<2.0',
 'pandas>=1.0,<2.0',
 'phonopy>=2.6,<2.7.0',
 'scipy>=1.1.1,<2.0.0',
 'seekpath>=1.8.4,<2.0.0',
 'son>=0.3.2,<0.4.0',
 'spglib>=1.12,<2.0',
 'tables>=3.5,<4.0',
 'xarray>=0.12,<0.13']

extras_require = \
{'fireworks': ['fireworks>=1.9,<2.0',
               'python-gssapi>=0.6.4,<0.7.0',
               'pymongo>=3.8,<4.0',
               'fabric>=2.4,<3.0',
               'paramiko>=2.4,<3.0'],
 'hiphive': ['hiphive>=0.5.0,<0.6.0'],
 'phono3py': ['phono3py>=1.19,<2.0'],
 'postgresql': ['psycopg2>=2.8.0,<3.0.0']}

entry_points = \
{'console_scripts': ['vibes = vibes.cli:cli']}

setup_kwargs = {
    'name': 'fhi-vibes',
    'version': '1.0.0a2',
    'description': 'Fritz Haber Institute Vibrational Simulations',
    'long_description': 'FHI-vibes\n===\n\nWelcome to `FHI-vibes`, a `python` package for _ab initio_ modeling of vibrational properties in anharmonic solids.\n\n## Overview\n\n- [Tutorial](Tutorial/0_intro/)\n- [Documentation](Documentation/0_intro/)\n- If you are interested in scientific work that was performed using `FHI-vibes`, please have a look at [References](References.md)\n\n`FHI-vibes` is preparing a submission to [JOSS](https://joss.theoj.org/).\n\n## Installation\n\n### Prerequisites\n\n- A working `python3.7+` or `python3.6` (see remarks below) environment, e.g., provided by [anaconda](https://docs.conda.io/en/latest/miniconda.html)\n\n- A working `fortran` compiler, e.g., obtained by\n  \n  - `apt-get install gfortran` in Debian-derived systems, or\n  - `conda install -c conda-forge fortran-compiler` when `conda` is used.\n- If you want to use `FHI-aims` for running _ab initio_ calculations, make sure you have a recent version that supports the iPi socket communication.\n\n\n### Install `vibes`\n\n`FHI-vibes` can be installed simply via pip:\n\n```bash\npip install fhi-vibes\n```\n\n**(Important: If you run in to version conflicts that you cannot solve, use a virtual environment created with `python -m venv` or `conda create`.)**\n\n### Configuration\n\nConfigure `vibes` by creating a `~/.vibesrc` configuration file in the home directory. To this end, first run\n\n```\nvibes template configuration > ~/.vibesrc\n```\n\nand edit according to system. The `aims_command` is a command or script that takes care of running aims. This can be either just `mpirun aims.x`, or a script loading necessary modules etc. and finally calling `srun aims.x` on a cluster.\n\n**You\'re now good to go!** Just make sure your vibes virtual environment is activated.\n\n### Remarks for `python3.6`\n\nOn `python3.6`, please install `importlib_resources` and `dataclasses` via \n\n```bash\npip install importlib_resources dataclasses\n```\n\n### Autocompletion\n\nTo activate autocompletion of `vibes` subcommands, add this to your `.bashrc`:\n\n```bash\neval "$(_VIBES_COMPLETE=source vibes)"\n```\n\nand source it.\n\nIf you use the `fishshell`, add a file `~/.config/fish/completions/vibes.fish` containing\n\n```bash\neval (env _VIBES_COMPLETE=source-fish vibes)\n```\n',
    'author': 'Florian Knoop',
    'author_email': 'knoop@fhi-berlin.mpg.de',
    'url': 'https://gitlab.com/flokno/hilde',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
