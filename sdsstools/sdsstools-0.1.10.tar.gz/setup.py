# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sdsstools',
 'sdsstools._vendor',
 'sdsstools._vendor.releases',
 'sdsstools._vendor.toml']

package_data = \
{'': ['*']}

install_requires = \
['docutils>=0.16,<0.17',
 'pygments>=2.5.2,<3.0.0',
 'pyyaml>=4.0',
 'semantic-version>=2.8.4,<3.0.0',
 'six>=1.14.0,<2.0.0']

extras_require = \
{'dev': ['invoke>=1.3.0,<2.0.0',
         'twine>=3.1.1,<4.0.0',
         'wheel>=0.33.6,<0.34.0']}

entry_points = \
{'console_scripts': ['sdss = sdsstools.cli:main']}

setup_kwargs = {
    'name': 'sdsstools',
    'version': '0.1.10',
    'description': 'Small tools for SDSS products',
    'long_description': '# sdsstools\n\n![Versions](https://img.shields.io/badge/python->3.7-blue)\n[![PyPI version](https://badge.fury.io/py/sdsstools.svg)](https://badge.fury.io/py/sdsstools)\n\n`sdsstools` provides several common tools for logging, configuration handling, version parsing, packaging, etc. It\'s main purpose is to consolidate some of the utilities originally found in the [python_template](https://github.com/sdss/python_template), allowing them to become dependencies that can be updated.\n\n**This is not intended to be a catch-all repository for astronomical tools.** `sdsstools` itself aims to have minimal dependencies (i.e., mainly the Python standard library and setuptools).\n\n## Using sdsstools\n\nTo use sdsstools simply install it with\n\n```console\npip install sdsstools\n```\n\nMost likely, you\'ll want to include sdsstools as a dependency for your library. To do so, either add to your `setup.cfg`\n\n```ini\n[options]\ninstall_requires =\n    sdsstools>=0.1.0\n```\n\n(this is equivalent of passing `install_requires=[\'sdsstools>=0.1.0\']` to `setuptools.setup`), or if you are using [poetry](https://poetry.eustace.io/) run `poetry add sdsstools`, which should add this line to your `pyproject.toml`\n\n```toml\n[tool.poetry.dependencies]\nsdsstools = { version="^0.1.0" }\n```\n\n## Logging\n\nsdsstools includes the [sdsstools.logger.SDSSLogger](https://github.com/sdss/sdsstools/blob/f30e00f527660fe8627e33a7f931b44410b0ff06/src/sdsstools/logger.py#L107) class, which provides a wrapper around the standard Python [logging](https://docs.python.org/3/library/logging.html) module. `SDSSLoger` provides the following features:\n\n- A console handler (accessible via the `.sh` attribute) with nice colouring.\n- Automatic capture of warnings and exceptions, which are formatted and redirected to the logger. For the console handler, this means that once the logger has been created, all warnings and exceptions are output normally but are clearer and more aesthetic.\n- A [TimedRotatingFileHandler](https://docs.python.org/3.8/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler) (accessible via the `.fh` attribute) that rotates at midnight UT, with good formatting.\n\nTo get a new logger for your application, simply do\n\n```python\nfrom sdsstools.logger import get_logger\n\nNAME = \'myrepo\'\nlog = get_logger(NAME)\n```\n\nThe file logger is disabled by default and can be started by calling `log.start_file_logger(path)`. By default a `TimedRotatingFileHandler` is created. If you want a normal `FileHandler` use `rotate=False`. The file mode defaults to `mode=\'a\'` (append).\n\n## Configuration\n\nThe `sdsstools.configuration` module contains several utilities to deal with configuration files. The most useful one is [get_config](https://github.com/sdss/sdsstools/blob/d3d337953a37aaff9c38fead76b08b414164775a/src/sdsstools/configuration.py#L40), which allows to read a YAML configuration file. For example\n\n```python\nfrom sdsstools.configuration import get_config\n\nNAME = \'myrepo\'\nconfig = get_config(NAME, allow_user=True)\n```\n\n`get_config` assumes that the file is located in `etc/<NAME>.yml` relative from the file that calls `get_config`, but that can be changed by passing `config_file=<config-file-path>`. Additionally, if `allow_user=True` and a file exists in `~/.config/sdss/<NAME>.yaml`, this file is read and merged with the default configuration, overriding any parameter that is present in the user file. This allows to create a default configuration that lives with the library but that can be overridden by a user.\n\nIn addition to the (recommended) location `~/.config/sdss/<NAME>.yaml`, `get_config` also looks for user configuration files in `~/.config/sdss/<NAME>.yml`, `~/.config/sdss/<NAME>/<NAME>.y(a)ml`, and `~/.<NAME>/<NAME>.y(a)ml`.\n\nAdditionally, `sdsstools.configuration` includes two other tools, `merge_config`, that allows to merge dictionaries recursively, and `read_yaml_file`, to read a YAML file.\n\n## Metadata\n\nsdsscore provides tools to locate and parse metadata files (`pyproject.toml`, `setup.cfg`, `setup.py`). `get_metadata_files` locates the path of the metadata file relative to a given `path`. `get_package_version` tries to find the version of the package by looking for a version string in the metadata file or in the egg/wheel metadata file, if the package has been installed. To use it\n\n```python\nfrom sdsstools.metadata import get_package_version\n\n__version__ = get_package_version(path=__file__, package_name=\'sdss-camera\') or \'dev\'\n```\n\nThis will try to find and parse the version from the metadata file (we pass `__file__` to indicate where to start looking); if that fails, it will try to get the version from the installed package `sdss-camera`. If all fails, it will set the fallback version `\'dev\'`.\n\n## Command Line Interface\n\n`sdsstools` provides the command line tool `sdss`, which is just a thin wrapper around some commonly used [Invoke](https://www.pyinvoke.org/) tasks. Because `sdsstools` tries very hard not to install unnecessary dependencies, and the CLI should only be useful for development, you\'ll need to run `pip install sdsscore[dev]` to be able to use `sdss`.\n\n`sdss` provides the following tasks\n\n| Task | Options | Description |\n| --- | --- | --- |\n| clean | | Removes files produces during build and packaging |\n| deploy | --test | Builds and deploys to PyPI (or the test server) |\n| install-deps | --extras | Installs dependencies from a `setup.cfg` file |\n| docs.build | --target | Builds the Sphinx documentation |\n| docs.show | --target | Shows the documentation in the browser |\n| docs.clean | --target | Cleans the documentation build |\n\n`sdss` assumes that the documentation lives in `docs/sphinx` relative to the root of the repository. This can be changed by setting the `sphinx.target` configuration in an `invoke.yaml` file, for example\n\n```yaml\nsphinx:\n    target: docs\n```\n\n## Bundled packages\n\nFor convenience, `sdsstools` bundles the following products:\n\n- A copy of [releases](https://github.com/bitprophet/releases) that fixes some issues with recent versions of `semantic-version`.\n- A copy of [toml](https://github.com/uiri/toml) to read TOML files (used by the metadata submodule).\n\nYou can access them directly from the top-level namespace, `sdsstools.toml`, `sdsstools.releases`. To use `releases` with sphinx, simply add the following to your `config.py`\n\n```python\nextensions += [\'sdsstools.releases\']\n```\n',
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdss/sdsstools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
