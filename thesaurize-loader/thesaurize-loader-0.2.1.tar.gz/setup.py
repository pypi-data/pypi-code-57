# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thesaurize_loader']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'progress>=1.5,<2.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['thesaurize-loader = thesaurize_loader.__main__:main']}

setup_kwargs = {
    'name': 'thesaurize-loader',
    'version': '0.2.1',
    'description': 'Loads encoded thesaurus into Redis datastore',
    'long_description': "# Thesaurize Loader\nThis utility transforms [OpenOffice](https://openoffice.org) thesaurus data\nfiles (based on Princeton's WordNet) into Redis protocol data streams. This\nutility essentially mass-inserts thesaurus data into a Redis instance for use\nwith the [thesaurize bot](https://github.com/MrFlynn/thesaurize-bot) for\nDiscord.\n\nYou can read more and download the OpenOffice thesaurus\n[here](https://www.openoffice.org/lingucomponent/thesaurus.html).\n\n## Usage\nYou will need to install this utility with pip(x) and have Redis installed and\nrunning. Then run the utility with the following arguments.\n\n```bash\n$ pipx install thesaurize-loader\n$ thesaurize-loader \\\n    --file=https://www.openoffice.org/lingucomponent/MyThes-1.zip \\\n    --connection=redis://localhost:6379\n```\n\nAlternatively, you can download the thesaurus archive linked above and extract \nit. Then run the following command:\n\n```bash\n$ thesaurize-loader --file=file:///path/to/thesaurus.dat --connection=redis://localhost:6379\n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Nick Pleatsikas',
    'author_email': 'nick@pleatsikas.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrFlynn/thesaurize-bot/tools/loader-tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
