# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alphabetsoup']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.76,<2.0',
 'click>=7.1.2,<8.0.0',
 'click_loguru>=0.3.3,<0.4.0',
 'cloudpickle>=1.4.1,<2.0.0',
 'dask[bag]>=2.15.0,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'toolz>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['alphabetsoup = alphabetsoup:cli']}

setup_kwargs = {
    'name': 'alphabetsoup',
    'version': '0.5.3',
    'description': 'tile phylogenetic space with subtrees',
    'long_description': ".. epigraph:: al·pha·bet soup\n              /ˈalfəˌbet so͞op/Submit\n              noun INFORMAL\n              incomprehensible or confusing language, typically containing many abbreviations or symbols.\n\n\nalphabetsoup fixes problems with protein FASTA files:\n+--------------------------+------------------------+\n| Problem                  | Fix                    |\n+--------------------------+------------------------+\n| Unknown character        | Replaces with 'X'      |\n+--------------------------+------------------------+\n| Stop/ambigous at ends    | Trims                  |\n+--------------------------+------------------------+\n| Stop/ambiguous in middle | Optionally fragments   |\n+--------------------------+------------------------+\n| Too short                | Deletes record         |\n+--------------------------+------------------------+\n\n\n+-------------------+------------+------------+\n| Latest Release    | |pypi|     | |Soup|     |\n+-------------------+------------+            +\n| GitHub            | |repo|     |            |\n+-------------------+------------+            +\n| License           | |license|  |            |\n+-------------------+------------+            +\n| Documentation     | |rtd|      |            |\n+-------------------+------------+            +\n| Travis Build      | |travis|   |            |\n+-------------------+------------+            +\n| Coverage          | |coverage| |            |\n+-------------------+------------+            +\n| Pythonicity       | |landscape||            |\n+-------------------+------------+            +\n| Code Grade        | |codacy|   |            |\n+-------------------+------------+            +\n| Dependencies      | |pyup|     |            |\n+-------------------+------------+            +\n| Issues            | |issues|   |            |\n+-------------------+------------+            +\n| Kanban            | |ZenHub|   |            |\n+-------------------+------------+------------+\n\n\n.. |Soup| image:: docs/alphabetsoup.webp\n     :target: https://en.wikipedia.org/wiki/Alphabet_soup_(linguistics)\n     :alt: Alphabet Soup Definition\n\n.. |pypi| image:: https://img.shields.io/pypi/v/alphabetsoup.svg\n    :target: https://pypi.python.org/pypi/alphabetsoup\n    :alt: Python package\n\n.. |repo| image:: https://img.shields.io/github/commits-since/ncgr/alphabetsoup/0.01.svg\n    :target: https://github.com/ncgr/alphabetsoup\n    :alt: GitHub repository\n\n.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg\n    :target: https://github.com/ncgr/alphabetsoup/blob/master/LICENSE.txt\n    :alt: License terms\n\n.. |rtd| image:: https://readthedocs.org/projects/alphabetsoup/badge/?version=latest\n    :target: http://alphabetsoup.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Server\n\n.. |travis| image:: https://img.shields.io/travis/ncgr/alphabetsoup.svg\n    :target:  https://travis-ci.org/ncgr/alphabetsoup\n    :alt: Travis CI\n\n.. |landscape| image:: https://landscape.io/github/ncgr/alphabetsoup/master/landscape.svg?style=flat\n    :target: https://landscape.io/github/ncgr/alphabetsoup\n    :alt: landscape.io status\n\n.. |codacy| image:: https://api.codacy.com/project/badge/Grade/2ebc65ca90f74dc7a9238c202f327981\n    :target: https://www.codacy.com/app/joelb123/alphabetsoup?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LegumeFederation/lorax&amp;utm_campaign=Badge_Grade\n    :alt: Codacy.io grade\n\n.. |coverage| image:: https://codecov.io/gh/ncgr/alphabetsoup/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/ncgr/alphabetsoup\n    :alt: Codecov.io test coverage\n\n.. |issues| image:: https://img.shields.io/github/issues/LegumeFederation/lorax.svg\n    :target:  https://github.com/ncgr/alphabetsoup/issues\n    :alt: Issues reported\n\n.. |requires| image:: https://requires.io/github/ncgr/alphabetsoup/requirements.svg?branch=master\n     :target: https://requires.io/github/ncgr/alphabetsoup/requirements/?branch=master\n     :alt: Requirements Status\n\n.. |pyup| image:: https://pyup.io/repos/github/ncgr/alphabetsoup/shield.svg\n     :target: https://pyup.io/repos/github/ncgr/alphabetsoup/\n     :alt: pyup.io dependencies\n\n.. |ZenHub| image:: https://raw.githubusercontent.com/ZenHubIO/support/master/zenhub-badge.png\n    :target: https://zenhub.com\n    :alt: Powered by ZenHub\n\n\n",
    'author': 'Joel Berendzen',
    'author_email': 'joelb@ncgr.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ncgr/alphabetsoup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
