# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdfl', 'mdfl.parser']

package_data = \
{'': ['*'],
 'mdfl': ['templates/function/*',
          'templates/function/{{ cookiecutter.name }}.function/*',
          'templates/pack/*',
          'templates/pack/{{ cookiecutter.name }}/*']}

install_requires = \
['cookiecutter>=1.7.2,<2.0.0',
 'docopt>=0.6.2,<0.7.0',
 'lark-parser>=0.8.6,<0.9.0']

entry_points = \
{'console_scripts': ['mdfl = mdfl:main']}

setup_kwargs = {
    'name': 'mdfl',
    'version': '0.3',
    'description': 'A prototype command-line tool for creating datapacks.',
    'long_description': "# PyMDFL [![Package](https://badge.fury.io/py/mdfl.svg)](https://badge.fury.io/py/mdfl)\nA command-line application to generate data packs based on [CRISPYrice](https://github.com/CRISPYricePC/MDFL-Spec/blob/master/spec.md)'s MDFL specification.\n\n## Installation\nInstall with pip: `python -m pip install mdfl`\n\nIf pip doesn't add the package to PATH correctly, you can start the program with `python -m mdfl`.\n\n## Usage\n`mdfl --help` will output usage information:\n```\nPyMDFL: A command-line tool for parsing MDFL and generating Data Packs.\n\nUsage:\n    mdfl <script> [--output=<path>]\n    mdfl <script> [--tree]\n    mdfl -h | --help\n    mdfl -V | --version\n\nOptions:\n    -h --help        Show this screen.\n    -V --version     Show version.\n    --output=<path>  Output path for the datapack.\n    --tree           Print a syntax tree without compiling.\n```\n\nThe `<script>` argument specifies a file that conforms to the MDFL spec. For example, given a file `gems.mdfl`:\n```\nnamespace diamonds {\n  // Namespace for obtaining diamonds.\n\n  fun get {\n    // Give the caller a diamond.\n    give @s minecraft:diamond;\n  }\n}\n\nnamespace emeralds {\n  // Namespace for obtaining emeralds.\n\n  fun get {\n    // Give the caller an emerald.\n    give @s minecraft:emerald;\n  }\n}\n```\nRun `mdfl gems.mdfl` and enter a description for your data pack.\n```\n$ mdfl gems.mdfl\nDescription of gems: All your gems are belong to @s\n```\nThis will generate a zip file `gems.zip` with the following structure:\n```\n├── data\n│  ├── emeralds\n│  │  └── functions\n│  │     └── get.mcfunction\n│  └── diamonds\n│     └── functions\n│        └── get.mcfunction\n└── pack.mcmeta\n```\n",
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
