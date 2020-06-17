# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comlipy',
 'comlipy.lib',
 'comlipy.lib.rules',
 'comlipy.tests',
 'comlipy.tests.lib']

package_data = \
{'': ['*']}

install_requires = \
['click==7.0', 'pyyaml==5.3']

entry_points = \
{'console_scripts': ['comlipy = comlipy.main:cli',
                     'comlipy-install = comlipy.main:install']}

setup_kwargs = {
    'name': 'comlipy',
    'version': '1.2.0',
    'description': 'comlipy by slashplus - lint commit messages with python',
    'long_description': '# comlipy by slashplus - lint commit messages with python\n\n<div align="center">\n  <img width="800" src="https://gitlab.com/slashplus-build/comlipy/raw/master/docs/assets/comlipy.svg">\n</div>\n\nDemo generated with [svg-term-cli](https://github.com/marionebl/svg-term-cli) \n\n**comlipy** is a helper that makes it incredibly easy to check whether\nyour commit messages follow predefined or custom commit message \nstandards or not. \n\nThis means that after setting up `comlipy` in combination with \na custom git `commit-msg` hook ([further information](https://git-scm.com/book/uz/v2/Customizing-Git-Git-Hooks)),\n`comlipy` takes care of the provided commit msg and warns you\nwhenever a message does not fit your style. \n\nBy default `comlipy` follows the [conventional commit standards](https://conventionalcommits.org),\nbut you can easily change the configuration in order to fit your needs.\n\n## Requirements\n\n- python 3.7+\n- pip (pip3) or brew\n- poetry\n\n## Installation\n\n### Installation with brew (recommended)\n\n```bash\n# Add the source\nbrew tap slashplus/comlipy git@gitlab.com:slashplus-build/comlipy.git\n\n# Install comlipy\nbrew install comlipy\n```\n\n### Installation with pip\n\n```bash\npip3 install comlipy\n```\n\n### Development installation\n\nInstall the repository by git cloning it and by setting up a \nvirtual environment using poetry:\n\n```bash\ngit clone git@gitlab.com:slashplus-build/comlipy.git # clone repo\ncd comlipy/ # change to comlipy directory\npoetry install # install dependencies\n```\n\nRun comlipy:\n\n```bash\npoetry shell # open the virtual environment\n\n# or just run a single command\n# poetry run comlipy-install\n```\n    \n## Usage\n\n### Setting up a git commit-msg hook (optional)\nComlipy comes with a simple git commit-msg hook installer. \nThis sets up a commit-msg hook that checks the commit message before the \nactual commit. <br>\nAn example `commit-msg` hook can be found [here](https://gitlab.com/slashplus-build/comlipy/blob/master/docs/commit-msg.sample) \n\nMake sure you have initialized `git` in your project. \nAnd then just run `comlipy-install`, or \n`comlipy-install -c \'PATH/TO/CUSTOM/CONFIGFILE.yml\'` \nif you want to set a default config override.\n\n**Note:** <br>\nDon\'t worry, the installer will _not_ automatically override an \nexisting commit-msg hook. In case such file already exists, you will be \nasked if you want to override it.\n\n**Tip:**<br>\nSometimes it can be useful to to set up a custom git hooks path, instead \nof overriding the commit-msg hook directly. <br>\nLearn more about it [here](https://git-scm.com/docs/githooks).\n\n### Setting up a a custom configuration override (optional)\n\nIts on you to configure `comlipy` so it perfectly fits your needs \nby setting up and passing a custom configuration yml file. By doing this, \nyou can override the default configuration i.e. enable or disable rules \nor changing the message behaviour (none, warning, error). \n\nSee [docs](https://gitlab.com/slashplus-build/comlipy/blob/master/docs/) for further details.\n\n## Documentation\n\nDocumentation is currently not finished. Following a list of available \nreferences:\n\n- [docs](https://gitlab.com/slashplus-build/comlipy/blob/master/docs/): ALL documents \n- [rules](https://gitlab.com/slashplus-build/comlipy/blob/master/docs/reference-rules.md): Reference of all available \nvalidation rules with configuration values\n- [ignores](https://gitlab.com/slashplus-build/comlipy/blob/master/docs/reference-ignores.md): Reference of default \nvalidation ignores and how to add custom ignores \n- [commit-msg sample hook](https://gitlab.com/slashplus-build/comlipy/blob/master/docs/commit-msg.sample): Example git \n`commit-msg` hook\n- [cli](https://gitlab.com/slashplus-build/comlipy/blob/master/docs/reference-cli.md): List of available cli flags\n\n## Configuration\n\nIt is possible to change the configuration values. This way you are able \nto change rule behaviour of all rules by providing values \nfor `applicable`, `value`, `level` or you can change global settings\ni.e. the help message. \n\nTherefore you must define a custom YAML file with the rules to override \nand pass the custom config file path via parameter:\n\nIf a config rule is not set, the default value will be used instead.\n\nExample `config-comlipy.yml`\n\n```yaml\n## global definitions\nglobal:\n  help: \'get help here: foo-bar-baz.abc\'\n\nrules:\n  header-min-length:\n    applicable: \'always\'\n    value: 0\n    level: 1\n  header-max-length: \n    applicable: \'always\'\n    value: 123\n    level: 2\n  scope-case:\n    value: \'upper-case\'\n  scope-empty:\n    applicable: \'never\'\n    level: 2\nignores:\n    - \'^SKIPME\' #skip validations where header starts with "SKIPME"\n```\n\n## Tests\n\nYou can run unit.tests by following the python 3 unittest documentation.\nFor example:\n\n```bash\npython -m unittest comlipy.tests.lib.test_ensure\npython -m unittest comlipy.tests.lib.test_rule_checker\n```\n\nor run all tests in batch:\n```bash\n# optionally run it in verbose mode (-v)\npython -m unittest -v comlipy.tests.suite\n```\n\n### Credits & inspiration\n\n- [commitlint](https://github.com/conventional-changelog/commitlint)\n- [conventional commit standards](https://conventionalcommits.org)\n',
    'author': 'slashplus',
    'author_email': 'info@slashplus.de',
    'maintainer': 'slashplus',
    'maintainer_email': 'info@slashplus.de',
    'url': 'https://gitlab.com/slashplus-build/comlipy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
