# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jmopenorders', 'jmopenorders.api', 'jmopenorders.core']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.6.1,<4.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'requests>=2.23.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['jmopenorders = jmopenorders.cli:main']}

setup_kwargs = {
    'name': 'jmopenorders',
    'version': '0.2.2',
    'description': 'Jmopenorders',
    'long_description': '[![Tests](https://github.com/jmuelbert/jmopenorders/workflows/Tests/badge.svg)](https://github.com/jmuelbert/jmopenorders/actions?workflow=Tests)\n\n[![Coverage](https://codecov.io/gh/jmuelbert/jmopenorders/branch/master/graph/badge,svg)](https://codecov.io/gh/jmuelbert/jmopenorders)\n\n[![PyPi](https://img.shields.io/pypi/v/jmopenorders.svg)](https://pypi.python.org/pypi/jmopenorders/)\n\n[![(https://readthedocs.org/projects/jmopenorders/badge/)](https://jmopenorders.readthedocs.io/)\n\n[![(https://img.shields.io/badge/license-EUPL-blue.svg)](https://joinup.ec.europa.eu/page/eupl-text-11-12)\n\n# jmopenorders\n\njmopenorders is a generator to generate infos for the affected persons.\n\njmopenorders is written in [Python](https://www.python.org).\npython does run on almosts known platforms.\n\n## Sources\n\nThe master branch represents the latest pre-release code.\n\n- [Releases](https://github.com/jmuelbert/jmopenorders/releases).\n\n- [Milestones](https://github.com/jmuelbert/jmopenorders/milestones).\n\n## Requests and Bug reports\n\n- [GitHub issues (preferred)](https://github.com/jmuelbert/jmopenorders/issues).\n\n## Questions or Comments\n\n## Wiki\n\n- [Main Page](https://github.com/jmuelbert/jmopenorders/wiki).\n- [User Manual](http://jmuelbert.github.io/jmopenorders/).\n\n## Installing\n\nAn install script is preferred. You can you the latest release or build the newest version with the command:\n\n    ``./setup.py sdist``\n\nor\n`python setup.py sdist`\n\nThis build an python installer\n\n[ ~ Dependencies scanned by PyUp.io ~ ]\n\n## License\n\nopenorders is free software; you can redistribute ot and/or modify ir under the terms\nof the [European Public License Version 1.2](https://joinup.ec.europa.eu/page/eupl-text-11-12).\nPlease read the (https://github.com/jmuelbert/jmopenorders/blob/master/LICENSE) for additional information.\n\nEUPL-1.2 © Jürgen Mülbert\n',
    'author': 'Jürgen Mülbert',
    'author_email': 'juergen.muelbert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmuelbert/jmopenorders',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
