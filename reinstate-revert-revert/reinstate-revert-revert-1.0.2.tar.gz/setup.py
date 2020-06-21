# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reinstate_revert_revert']

package_data = \
{'': ['*']}

install_requires = \
['dulwich>=0.19.16,<0.20.0']

entry_points = \
{'console_scripts': ['reinstate-revert-revert = reinstate_revert_revert.cli:main']}

setup_kwargs = {
    'name': 'reinstate-revert-revert',
    'version': '1.0.2',
    'description': 'pre-commit plugin to improve default commit messages when reverting reverts',
    'long_description': '# reinstate-revert-revert\n\nA tool for cleaning up reverted-revert git commit messages.\n\n## Simple Case\n\nIt will turn\n\n```\nRevert "Revert "Experiment on the flux capacitor""\n\nThis reverts commit deadc0dedeadc0dedeadc0dedeadc0dedeadc0de.\n```\n\ninto\n\n```\nReinstate "Experiment on the flux capacitor"\n\nThis reverts commit deadc0dedeadc0dedeadc0dedeadc0dedeadc0de.\nAnd reinstates commit 0d15ea5e0d15ea5e0d15ea5e0d15ea5e0d15ea5e.\n```\n\n## Complex Case\n\nIf you have gotten yourself into a bind, it will also convert this:\n\n```\nRevert "Revert "Revert "Revert "Revert "Experiment on the flux capacitor"""""\n```\n\ninto this, making it easier to follow the chain:\n\n```\nRevert "Experiment on the flux capacitor"\n\nThis reverts commit deadc0dedeadc0dedeadc0dedeadc0dedeadc0de.\nAnd reinstates commit 0d15ea5e0d15ea5e0d15ea5e0d15ea5e0d15ea5e.\nAnd reverts 1337beef1337beef1337beef1337beef1337beef.\nAnd reinstates 1337f0011337f0011337f0011337f0011337f001.\nAnd reverts 1337c0de1337c0de1337c0de1337c0de1337c0de.\n```\n\nThough once you\xe2\x80\x99re using this as a pre-commit plugin, you should never get to\nthis case in the first place.\n\n## Installation\n\n### As a git hook\n\nThe simplest way to use this package is as a plugin to [pre-commit](https://pre-commit.com/).\n\nA sample configuration:\n\n```yaml\n# Without default_stages, all hooks run in all stages, which means all your\n# pre-commit hooks will run in prepare-commit-msg. That is almost certainly\n# not what you want. This example will run for the default hooks installed.\n# You might have to adjust it for your environment, if you have changed those\n# defaults.\ndefault_stages:\n  - commit\n  - merge-commit\nrepos:\n  # [\xe2\x80\xa6]\n  - repo: https://github.com/erikogan/reinstate-revert-revert\n    rev: v1.0.2\n    hooks:\n      - id: reinstate-revert-revert\n        stages:\n          - prepare-commit-msg\n```\n\nBy default, pre-commit does not install a hook for the `prepare-commit-msg` stage. You probably need to add it for this to work:\n\n```\npre-commit install -t prepare-commit-msg\n```\n\n### As a standalone script\n\n```\npip install reinstate-revert-revert\n```\n\nSee `reinstate-revert-revert --help` for a full set of options.\n\n`reinstate-revert-revert` takes log message file names as positional arguments.\n',
    'author': 'Erik Ogan',
    'author_email': 'erik@ogan.net',
    'maintainer': 'Erik Ogan',
    'maintainer_email': 'erik@ogan.net',
    'url': 'https://github.com/erikogan/reinstate-revert-revert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
