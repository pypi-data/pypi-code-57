# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gilbert', 'gilbert.plugins']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'aionotify>=0.2.0,<0.3.0',
 'libsass>=0.19.4,<0.20.0',
 'markdown>=3.2.1,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'stencil-template>=4.2.1,<5.0.0']

entry_points = \
{'console_scripts': ['gilbert = gilbert.cli:main']}

setup_kwargs = {
    'name': 'gilbert',
    'version': '0.5.2',
    'description': 'A simple, extensible static site generator.',
    'long_description': "# Gilbert\n\nAnother static site generator.\n\nhttps://en.wikipedia.org/wiki/William_Gilbert_(astronomer)\n\nThis README contains a brief introduction to the project. Full documentation\n[is available here](https://gilbert.readthedocs.io/en/latest/).\n\n# Quick Start\n\nInstall gilbert:\n\n    $ pip install gilbert\n\nCreate a gilbert project:\n\n    $ gilbert --root mysite init\n\n(You can omit `--root` if it's the current directory.)\n\nCreate page files in mysite/pages/\n\nRender your site:\n\n    $ gilbert --root mysite render\n\nHave gilbert serve your site:\n\n    $ gilbert --root mysite serve\n\nServe your site and re-render on changes:\n\n    $ gilbert --root mysite serve --watch\n\nFinally, list all loaders and plugins:\n\n    $ gilbert --root mysite plugins\n\n\n## Installation requirements\n\nGilbert current requires Python 3.7 or greater.\n",
    'author': 'Curtis Maloney',
    'author_email': 'curtis@tinbrain.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/funkybob/gilbert',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
