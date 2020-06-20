# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vktoken']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.0,<2.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['vktoken = vktoken.main:main']}

setup_kwargs = {
    'name': 'vktoken',
    'version': '1.0.2',
    'description': 'A tool for getting VK access token',
    'long_description': '# vktoken\nA tool for getting VK access token\n\n## Install:\n`pip install vktoken`\n\n## Run:\n`vktoken [--help] [--copy] [--version] login [password] [app]`\n\n## Examples:\n* `vktoken +12025550178`  \n* `vktoken --copy +12025550178  "MyPassword" iphone` \n\n## Features:\n* Access token can be copied to the clipboard automatically if you use `--copy` key \n* You can choose any VK app from the list: `android`, `iphone`, `ipad`, `windows-phone` and `desktop`\n',
    'author': 'jieggii',
    'author_email': 'jieggii.contact@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jieggii/vktoken',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
