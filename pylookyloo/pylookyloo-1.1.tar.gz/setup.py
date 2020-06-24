# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylookyloo']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['lookyloo = pylookyloo:main']}

setup_kwargs = {
    'name': 'pylookyloo',
    'version': '1.1',
    'description': 'Python client for Lookyloo',
    'long_description': "# PyLookyloo\n\nThis is the client API for [Lookyloo](https://github.com/Lookyloo/lookyloo).\n\n## Installation\n\n```bash\npip install pylookyloo\n```\n\n## Usage\n\n* You can use the lookyloo command to enqueue an URL.\n\n```bash\nusage: lookyloo [-h] [--url URL] --query QUERY\n\nEnqueue a URL on Lookyloo.\n\noptional arguments:\n  -h, --help     show this help message and exit\n  --url URL      URL of the instance (defaults to https://lookyloo.circl.lu/,\n                 the public instance).\n  --query QUERY  URL to enqueue.\n\nThe response is the permanent URL where you can see the result of the capture.\n```\n\n* Or as a library\n\n```python\n\nfrom pylookyloo import Lookyloo\n\nlookyloo = Lookyloo('https://url.of.lookyloo.instance')\nif lookyloo.is_up:  # to make sure it is up and reachable\n\tpermaurl = lookyloo.enqueue('http://url.to.lookup')\n\n```\n",
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CIRCL/lookyloo/client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
