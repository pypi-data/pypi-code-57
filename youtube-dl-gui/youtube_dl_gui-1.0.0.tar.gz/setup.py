# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['youtube_dl_gui',
 'youtube_dl_gui.GUI',
 'youtube_dl_gui.Threads',
 'youtube_dl_gui.UI']

package_data = \
{'': ['*'], 'youtube_dl_gui.UI': ['images/*', 'resources/*']}

install_requires = \
['pyqt5>=5.15.0,<6.0.0', 'youtube-dl>=2020.6.16,<2021.0.0']

entry_points = \
{'console_scripts': ['youtube_dl_gui = youtube_dl_gui.main:main']}

setup_kwargs = {
    'name': 'youtube-dl-gui',
    'version': '1.0.0',
    'description': 'Yet another youtube-dl frontend written in python3 and qt5',
    'long_description': None,
    'author': 'Vadym Stupakov',
    'author_email': 'vadim.stupakov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Red-Eyed/youtube-dl-gui-qt5',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
