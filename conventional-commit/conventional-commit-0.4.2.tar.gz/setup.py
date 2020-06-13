# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitcommit']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=19.2,<20.0',
 'prompt_toolkit>=3.0,<4.0',
 'pyperclip>=1.7,<2.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['commit = gitcommit.gitcommit:main',
                     'gitcommit = gitcommit.gitcommit:main']}

setup_kwargs = {
    'name': 'conventional-commit',
    'version': '0.4.2',
    'description': 'a tool for writing conventional commits, conveniently',
    'long_description': '<p  align="center">\n  <strong>gitcommit</strong>\n  <br>\n  <code>a tool for writing conventional commits, conveniently</code>\n  <br><br>\n  <a href="https://badge.fury.io/py/conventional-commit"><img src="https://badge.fury.io/py/conventional-commit.svg" alt="PyPI version" height="18"></a>\n  <a href="https://travis-ci.org/nebbles/gitcommit/branches"><img src="https://travis-ci.org/nebbles/gitcommit.svg?branch=master" alt="Travis CI build" height="18"></a>\n  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" height="18"></a>\n</p>\n\n# Install\n\nTo install\n\n```\npip install conventional-commit\n```\n\nTo use, run the following command from within a git repository\n\n```\ngitcommit\n```\n\n# Overview\n\nThe purpose of this utility is to expedite the process of committing with a conventional message format in a user friendly way. This tool is not templated, because it sticks rigidly to the [Conventional Commit standard](https://www.conventionalcommits.org), and thus not designed to be \'altered\' on a case by case basis.\n\nCommit messages produced follow the general template:\n\n```\n<type>[(optional scope)]: <description>\n\n[BREAKING CHANGE: ][optional body / required if breaking change]\n\n[optional footer]\n```\n\nAdditional rules implemeted:\n\n1. Subject line (i.e. top) should be no more than 50 characters.\n2. Every other line should be no more than 72 characters.\n3. Wrapping is allowed in the body and footer, NOT in the subject.\n\n# Development\n\nThe old distribution method is documented in\n[docs/dev_distibution_legacy.md](docs/dev_distribution_legacy.md)\n\n_Note: if modifying `.travis.yml` you should verify it by running `travis lint .travis.yml`_\n\n## Getting started\n\n1. Make sure you have [pre-commit](https://pre-commit.com/#install) installed.\n\n1. Make sure you have [pyenv](https://github.com/pyenv/pyenv) installed.\n\n1. Make sure you have [Poetry](https://github.com/sdispater/poetry) installed.\n\n1. `git clone`\n\n1. `pre-commit install`\n\n1. It is highly recommend you enable setting for storing the venvs within your projects.\n\n   ```\n   poetry config virtualenvs.in-project true\n   ```\n\n1. Install project dependencies.\n   ```\n   poetry install\n   ```\n\n## Running the package locally\n\n1. Activate the virtual environment.\n\n   ```\n   source .venv/bin/activate\n   ```\n\n1. Run the package as a module.\n   ```\n   python -m gitcommit\n   ```\n\nAlternatively,\n\n1. Run the package using Poetry\'s venv as context\n   ```\n   poetry run python -m gitcommit\n   ```\n\nOr, if in another directory,\n\n1.  ```\n    ~/GitHub/gitcommit/.venv/bin/python -m gitcommit\n    ```\n\n## Deploy\n\nDeployment is handled automatically by Travis CI. It has been linked to the\nrepository and is automatically watching for pushes to master. It will build\nand test every commit to master. It will also build every tagged commit as\nif it was a branch, and since its a tagged commit, will attempt to publish\nit to PyPI.\n\n1. Don\'t forget to increment version number set in `pyproject.toml`. This can be\n   done with poetry.\n\n   ```\n   poetry version [patch|minor|major]\n   ```\n\n1. Update the version number as stored in the `gitcommit/__version__.py` file to match that designated by Poetry.\n\n1. Tag the commit (by default applies to HEAD commit - make sure you are on the latest `develop` commit).\n\n   ```\n   git tag v#.#.#\n   ```\n\n1. When pushing commits to remote, you must explicitly push tags too.\n   ```\n   git push origin --tags\n   ```\n\n## Acknowledgements\n\nThis work takes inspiration from [another repository porting Commitizen to Python](https://github.com/Woile/commitizen). This repository however uses none of the same source code and is focusing on a different approach.\n\n## License\n\nThis work is published under [GNU GPLv3](./LICENSE).\n',
    'author': 'nebbles',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nebbles/gitcommit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
