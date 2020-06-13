# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['retrocookie']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'git-filter-repo>=2.26.0,<3.0.0', 'pygit2>=1.2.1,<2.0.0']

entry_points = \
{'console_scripts': ['retrocookie = retrocookie.__main__:main']}

setup_kwargs = {
    'name': 'retrocookie',
    'version': '0.3.0',
    'description': 'Update Cookiecutter templates with changes from their instances',
    'long_description': "\nRetrocookie\n===========\n\n|Tests| |Codecov| |PyPI| |Python Version| |Read the Docs| |License| |Black| |pre-commit| |Dependabot|\n\n.. |Tests| image:: https://github.com/cjolowicz/retrocookie/workflows/Tests/badge.svg\n   :target: https://github.com/cjolowicz/retrocookie/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/cjolowicz/retrocookie/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/cjolowicz/retrocookie\n   :alt: Codecov\n.. |PyPI| image:: https://img.shields.io/pypi/v/retrocookie.svg\n   :target: https://pypi.org/project/retrocookie/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/retrocookie\n   :target: https://pypi.org/project/retrocookie\n   :alt: Python Version\n.. |Read the Docs| image:: https://readthedocs.org/projects/retrocookie/badge/\n   :target: https://retrocookie.readthedocs.io/\n   :alt: Read the Docs\n.. |License| image:: https://img.shields.io/pypi/l/retrocookie\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=cjolowicz/retrocookie\n   :target: https://dependabot.com\n   :alt: Dependabot\n\n\nRetrocookie updates Cookiecutter_ templates with changes from their instances.\n\nWhen developing Cookiecutter templates,\nyou often need to work in a generated project rather than the template itself.\nReasons for this include the following:\n\n- You need to run the Continuous Integration suite for the generated project\n- Your development tools choke when running on the templated project\n\nAny changes you make in the generated project\nneed to be backported into the template,\ncarefully replacing expanded variables from ``cookiecutter.json`` by templating tags,\nand escaping any use of ``{{`` and ``}}``\nor other tokens with special meaning in Jinja.\n\nRetrocookie helps you in this situation.\n\nIt is designed to fetch commits from the repository of a generated project,\nand import them into your Cookiecutter repository,\nrewriting them on the fly to insert templating tags,\nescape Jinja-special constructs,\nand place files in the template directory.\n\nUnder the hood,\nRetrocookie rewrites the selected commits using git-filter-repo_,\nsaving them to a temporary repository.\nIt then fetches and cherry-picks the rewritten commits\nfrom the temporary repository into the Cookiecutter template,\nusing pygit2_.\n\nMaybe you're thinking,\nhow can this possibly work?\nOne cannot reconstruct a Jinja template from its rendered output.\nHowever, simple replacements of template variables work well in practice\nwhen you're only importing a handful of commits at a time.\n\n\nRequirements\n------------\n\n* Python 3.7+\n* git >= 2.22.0\n\n\nInstallation\n------------\n\nYou can install *Retrocookie* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install retrocookie\n\n\nUsage\n-----\n\nThe basic form:\n\n.. code::\n\n   $ retrocookie <repository> [<commits>...]\n   $ retrocookie <repository> -b <branch> [--create]\n\nThe ``<repository>`` is a filesystem path to the source repository.\nFor ``<commits>``, see `gitrevisions(7)`__.\n\n__ https://git-scm.com/docs/gitrevisions\n\nImport ``HEAD`` from ``<repository>``:\n\n.. code::\n\n   $ retrocookie <repository>\n\nImport the last two commits:\n\n.. code::\n\n   $ retrocookie <repository> HEAD~2..\n\nImport by commit hash:\n\n.. code::\n\n   $ retrocookie <repository> 53268f7 6a3368a c0b4c6c\n\nImport commits from branch ``topic``:\n\n.. code::\n\n   $ retrocookie <repository> --branch=topic\n\nEquivalently:\n\n.. code::\n\n   $ retrocookie <repository> master..topic\n\nImport commits from ``topic`` into a branch with the same name:\n\n.. code::\n\n   $ retrocookie <repository> --branch=topic --create\n\nEquivalently, using short options:\n\n.. code::\n\n   $ retrocookie <repository> -cb topic\n\nImport commits from branch ``topic``, which was branched off ``1.0``:\n\n.. code::\n\n   $ retrocookie <repository> --branch=topic --upstream=1.0\n\nEquivalently:\n\n.. code::\n\n   $ retrocookie <repository> 1.0..topic\n\nImport ``HEAD`` into a new branch ``topic``:\n\n.. code::\n\n   $ retrocookie <repository> --create-branch=topic\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Retrocookie* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _file an issue: https://github.com/cjolowicz/retrocookie/issues\n.. _git-filter-repo: https://github.com/newren/git-filter-repo\n.. _git rebase: https://git-scm.com/docs/git-rebase\n.. _pip: https://pip.pypa.io/\n.. _pygit2: https://github.com/libgit2/pygit2\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n",
    'author': 'Claudio Jolowicz',
    'author_email': 'mail@claudiojolowicz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjolowicz/retrocookie',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
