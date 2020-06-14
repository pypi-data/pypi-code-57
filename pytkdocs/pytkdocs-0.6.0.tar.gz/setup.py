# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytkdocs', 'pytkdocs.parsers', 'pytkdocs.parsers.docstrings']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pytkdocs = pytkdocs.cli:main']}

setup_kwargs = {
    'name': 'pytkdocs',
    'version': '0.6.0',
    'description': 'Load Python objects documentation.',
    'long_description': '# pytkdocs\n\n[![ci](https://github.com/pawamoy/pytkdocs/workflows/ci/badge.svg)](https://github.com/pawamoy/pytkdocs/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/pytkdocs/)\n[![pypi version](https://img.shields.io/pypi/v/pytkdocs.svg)](https://pypi.org/project/pytkdocs/)\n\nLoad Python objects documentation.\n\n## Requirements\n\n`pytkdocs` requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.8\n\n# make it available globally\npyenv global system 3.6.8\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install pytkdocs\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 pytkdocs\n```\n\n## Usage\n\n`pytkdocs` accepts JSON on standard input and writes JSON on standard output.\n\nInput format:\n\n```json\n{\n  "objects": [\n    {\n      "path": "pytkdocs",\n      "members": true,\n      "inherited_members": false,\n      "filters": [\n        "!^_[^_]"\n      ],\n      "docstring_style": "google",\n      "docstring_options": {\n        "replace_admonitions": true\n      }\n    }\n  ]\n}\n```\n\nOutput format:\n\n```json\n{\n  "loading_errors": [\n    "string (message)"\n  ],\n  "parsing_errors": {\n    "string (object)": [\n      "string (message)"\n    ]\n  },\n  "objects": [\n    {\n      "name": "pytkdocs",\n      "path": "pytkdocs",\n      "category": "module",\n      "file_path": "/media/data/dev/pawamoy/pytkdocs/src/pytkdocs/__init__.py",\n      "relative_file_path": "pytkdocs/__init__.py",\n      "properties": [\n        "special"\n      ],\n      "parent_path": "pytkdocs",\n      "has_contents": true,\n      "docstring": "pytkdocs package.\\n\\nLoad Python objects documentation.",\n      "docstring_sections": [\n        {\n          "type": "markdown",\n          "value": "pytkdocs package.\\n\\nLoad Python objects documentation."\n        }\n      ],\n      "source": {\n        "code": "\\"\\"\\"\\npytkdocs package.\\n\\nLoad Python objects documentation.\\n\\"\\"\\"\\n\\nfrom typing import List\\n\\n__all__: List[str] = []\\n",\n        "line_start": 1\n      },\n      "children": {\n        "pytkdocs.__all__": {\n          "name": "__all__",\n          "path": "pytkdocs.__all__",\n          "category": "attribute",\n          "file_path": "/media/data/dev/pawamoy/pytkdocs/src/pytkdocs/__init__.py",\n          "relative_file_path": "pytkdocs/__init__.py",\n          "properties": [\n            "special"\n          ],\n          "parent_path": "pytkdocs",\n          "has_contents": false,\n          "docstring": null,\n          "docstring_sections": [],\n          "source": {},\n          "children": {},\n          "attributes": [],\n          "methods": [],\n          "functions": [],\n          "modules": [],\n          "classes": []\n        }\n      },\n      "attributes": [\n        "pytkdocs.__all__"\n      ],\n      "methods": [],\n      "functions": [],\n      "modules": [\n        "pytkdocs.__main__",\n        "pytkdocs.cli",\n        "pytkdocs.loader",\n        "pytkdocs.objects",\n        "pytkdocs.parsers",\n        "pytkdocs.properties",\n        "pytkdocs.serializer"\n      ],\n      "classes": []\n    }\n  ]\n}\n```\n\n## Command-line\n\nRunning `pytkdocs` without argument will read the whole standard input,\nand output the result once.\n\nRunning `pytkdocs --line-by-line` will enter an infinite loop,\nwhere at each iteration one line is read on the standard input,\nand the result is written back on one line.\nThis allows other programs to use `pytkdocs` in a subprocess,\nfeeding it single lines of JSON, and reading back single lines of JSON as well.\nThis mode was actually implemented specifically for\n[mkdocstrings](https://github.com/pawamoy/mkdocstrings).\n\n## Configuration\n\nThe configuration options available are:\n\n- `filters`: filters are regular expressions that allow to select or un-select objects based on their name.\n  They are applied recursively (on every child of every object).\n  If the expression starts with an exclamation mark,\n  it will filter out objects matching it (the exclamation mark is removed before evaluation).\n  If not, objects matching it are selected.\n  Every regular expression is performed against every name.\n  It allows fine-grained filtering. Example:\n\n    - `!^_`: filter out every object whose name starts with `_` (private/protected)\n    - `^__`: but still select those who start with two `_` (class-private)\n    - `!^__.*__$`: except those who also end with two `_` (specials)\n  \n- `members`: this option allows to explicitly select the members of the top-object.\n  If `True`, select every members that passes filters. If `False`, select nothing.\n  If it\'s a list of names, select only those members, and apply filters on their children only.\n\n- `docstring_style`: the docstring style to use when parsing the docstring. Only one parser available: `google`.\n\n- `docstring_options`: options to pass to the docstring parser.\n    - `google` accepts a `replace_admonitions` boolean option (default: true). When enabled, this option will\n      replace titles of an indented block by their Markdown admonition equivalent:\n      `AdmonitionType: Title` will become `!!! admonitiontype "Title"`.\n    \n- `inherited_members`: true or false (default). When enabled, inherited members will be selected as well.\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawamoy/pytkdocs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
