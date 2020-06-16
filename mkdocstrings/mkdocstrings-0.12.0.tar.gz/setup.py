# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mkdocstrings', 'mkdocstrings.handlers']

package_data = \
{'': ['*'], 'mkdocstrings': ['templates/python/material/*']}

install_requires = \
['beautifulsoup4>=4.8.2,<5.0.0',
 'mkdocs>=1.1,<2.0',
 'pymdown-extensions>=6.3,<8.0',
 'pytkdocs>=0.2.0,<0.7.0']

entry_points = \
{'mkdocs.plugins': ['mkdocstrings = mkdocstrings.plugin:MkdocstringsPlugin']}

setup_kwargs = {
    'name': 'mkdocstrings',
    'version': '0.12.0',
    'description': 'Automatic documentation from sources, for MkDocs.',
    'long_description': '# mkdocstrings\n\n[![ci](https://github.com/pawamoy/mkdocstrings/workflows/ci/badge.svg)](https://github.com/pawamoy/mkdocstrings/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/mkdocstrings/)\n[![pypi version](https://img.shields.io/pypi/v/mkdocstrings.svg)](https://pypi.org/project/mkdocstrings/)\n\nAutomatic documentation from sources, for MkDocs.\n\n---\n\n![mkdocstrings_gif1](https://user-images.githubusercontent.com/3999221/77157604-fb807480-6aa1-11ea-99e0-d092371d4de0.gif)\n\n---\n\n- [Features](#features)\n    - [Python handler features](#python-handler-features)\n- [Requirements](#requirements)\n- [Installation](#installation)\n- [Quick usage](#quick-usage)\n\n## Features\n\n- **Language agnostic:** just like `mkdocs`, `mkdocstrings` is written in Python but is language-agnostic.\n  It means you can use it for any language, as long as you implement a\n  [`handler`](https://pawamoy.github.io/mkdocstrings/reference/handlers/__init__/) for it.\n  Currently, we only have a [Python handler](https://pawamoy.github.io/mkdocstrings/reference/handlers/python/).\n  Maybe you\'d like to contribute another one :wink:?\n- **Multiple themes support:** each handler can offer multiple themes. Currently, we only offer the\n  :star: [Material theme](https://squidfunk.github.io/mkdocs-material/) :star: for the Python handler.\n- **Cross-references to other objects:** `mkdocstrings` makes it possible to reference other headings from your\n  Markdown files with the classic Markdown syntax: `[identifier][]` or `[title][identifier]`. This feature is language\n  agnostic as well: you can cross-reference any heading that appear in your Markdown pages.\n  If the handler for a particular language renders headings for documented objects, you\'ll be able to reference them!\n- **Inline injection in Markdown:** instead of generating Markdown files, `mkdocstrings` allows you to inject\n  documentation anywhere in your Markdown contents. The syntax is simple: `::: identifier` followed by a 4-spaces\n  indented YAML block. The identifier and YAML configuration will be passed to the appropriate handler\n  to collect and render documentation.\n- **Global and local configuration:** each handler can be configured globally in `mkdocs.yml`, and locally for each\n  "autodoc" instruction.\n- **Watch source code directories:** you can tell `mkdocstrings` to add directories to be watched by `mkdocs` when\n  serving the documentation, for auto-reload.\n- **Sane defaults:** you should be able to just drop the plugin in your configuration and enjoy your auto-generated docs.\n\n### Python handler features\n\n- **Data collection from source code**: collection of the object-tree and the docstrings is done by\n  [`pytkdocs`](https://github.com/pawamoy/pytkdocs). The following features are possible thanks to it:\n    - **Support for type annotations:** `pytkdocs` collects your type annotations and `mkdocstrings` uses them\n      to display parameters types or return types.\n    - **Recursive documentation of Python objects:** just use the module dotted-path as identifier, and you get the full\n      module docs. You don\'t need to inject documentation for each class, function, etc.\n    - **Support for documented attribute:** attributes (variables) followed by a docstring (triple-quoted string) will\n      be recognized by `pytkdocs` in modules, classes and even in `__init__` methods.\n    - **Support for objects properties:** `pytkdocs` detects if a method is a `staticmethod`, a `classmethod`, etc.,\n      it also detects if a property is read-only or writable, and more! These properties will be displayed\n      next to the object signature by `mkdocstrings`.\n    - **Google-style sections support in docstrings:** `pytkdocs` understands `Arguments:`, `Raises:`\n      and `Returns:` sections, and returns structured data for `mkdocstrings` to render them.\n    - **Admonition support in docstrings:** blocks like `Note: ` or `Warning: ` will be transformed\n      to their [admonition](https://squidfunk.github.io/mkdocs-material/extensions/admonition/) equivalent.\n      *We do not support nested admonitions in docstrings!*\n- **Every object has a TOC entry:** we render a heading for each object, meaning `mkdocs` picks them into the Table\n  of Contents, which is nicely display by the Material theme. Thanks to `mkdocstrings` cross-reference ability,\n  you can even reference other objects within your docstrings, with the classic Markdown syntax:\n  `[this object][package.module.object]` or directly with `[package.module.object][]`\n- **Source code display:** `mkdocstrings` can add a collapsible div containing the highlighted source code\n  of the Python object.\n\nTo get an example of what is possible, check `mkdocstrings`\'\nown [documentation](https://pawamoy.github.io/mkdocstrings), auto-generated from sources by itself of course,\nand the following GIF:\n\n![mkdocstrings_gif2](https://user-images.githubusercontent.com/3999221/77157838-7184db80-6aa2-11ea-9f9a-fe77405202de.gif)\n\n## Roadmap\n\n- [x] **December-January 2020:** Proof of Concept.\n- [x] **January-March 2020:** Refactor.\n- [x] **March-April 2020:** Test suite for [`pytkdocs`](https://github.com/pawamoy/pytkdocs). Bug fixes, enhancements.\n- [ ] **May-June 2020:** Test suite for `mkdocstrings` itself. **Better documentation.** Maybe a second handler, just for the fun.\n\n## Requirements\n\n`mkdocstrings` requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.8\n\n# make it available globally\npyenv global system 3.6.8\n```\n</details>\n\nThis project currently only works with the Material theme of MkDocs.\nTherefore, it is required that you have it installed.\n\n```\npip install mkdocs-material\n```\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install mkdocstrings\n```\n\n## Quick usage\n\n```yaml\n# mkdocs.yml\ntheme:\n  name: "material"\n\nplugins:\n  - search\n  - mkdocstrings\n```\n\nIn one of your markdown files:\n\n```yaml\n# Reference\n\n::: my_library.my_module.my_class\n```\n\nSee the [Usage](https://pawamoy.github.io/mkdocstrings/usage) section of the docs for more examples!\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawamoy/mkdocstrings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
