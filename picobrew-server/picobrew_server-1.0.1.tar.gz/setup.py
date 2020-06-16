# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picobrew_server',
 'picobrew_server.beerxml',
 'picobrew_server.blueprints',
 'picobrew_server.utils']

package_data = \
{'': ['*'],
 'picobrew_server': ['static/css/*',
                     'static/font/material-design-icons/*',
                     'static/font/roboto/*',
                     'static/img/*',
                     'static/js/*',
                     'templates/*']}

install_requires = \
['Flask-Cors==3.0.8',
 'Flask==1.1.2',
 'Werkzeug==1.0.1',
 'pybeerxml>=1.0.8,<2.0.0',
 'webargs==6.0.0']

setup_kwargs = {
    'name': 'picobrew-server',
    'version': '1.0.1',
    'description': 'A reverse-engineered server for the Picobrew homebrewing machines',
    'long_description': '# picobrew-server\n<img src="https://img.shields.io/pypi/v/picobrew_server"> <img src="https://img.shields.io/pypi/pyversions/picobrew_server"> <img src="https://img.shields.io/github/workflow/status/hotzenklotz/picobrew-server/Test and Lint/master">\n\n\nThis project reverse-engineers a server for the proprietary PicoBrew protocol for use with the [PicoBrew Zymatic](http://www.picobrew.com/), a homebrewing machine. It is intended to provide an alternative to run the machine without a connection to the official servers at picobrew.com. Run your own server and sync your recipes offline.\n\n# HTTP API\nThe PicoBrew Zymatic\'s built-in Ardunio uses an unencrypted HTTP communication protocol. All request are `GET` requests and are not authenticated. The following documentation is based on Firmware 1.1.8.\n\n- [PicoBrew Zymatic API Docs on Postman](https://documenter.getpostman.com/view/234053/Szf54VEX?version=latest)\n- [PicoBrew Zymatic API Docs on GitHub](https://github.com/hotzenklotz/picobrew-server/wiki/PicoBrew-API)\n\n# Installation\n\n1. Install Python 3.7 or above\n2. In a terminal download, install and run the project:\n```bash\n// Download and install\npip install picobrew_server\n\n// Start the server in production mode on port 80\n\n// Windows \nset FLASK_APP=picobrew_server\nflask run --port 80 --host 0.0.0.0\n\n// OSX / Linux\nexport FLASK_APP=picobrew_server \nflask run --port 80 --host 0.0.0.0\n```\n\n- Connect the PicoBrew machine to your computer and enable DNS spoofing. Re-route `www.picobrew.com` to your computer.\n[More Details](https://github.com/hotzenklotz/picobrew-server/wiki/Install)\n\n# Development \n\n1. Install Python 3.7+ & [Poetry](https://python-poetry.org/):\n\n```bash\npip install poetry\n```\n\n2. Install all dependecies:\n\n```bash\npoetry install\n\n// Start the server on http://localhost:5000\nFLASK_APP=picobrew_server flask run\n```\n\n3. Lint, Format, and Type Check changes:\n```\npylint picobrew_server\nblack picobrew_server\nmypy picobrew_server\n```\n\n\n# Demo\nYou can try out the admin UI for uploading your XML files in this [online demo](https://picobrew.herokuapp.com). Please note, this website is for showcasing only and you should deploy your own version.\n\n\n# Features\n- Import BeerXML files\n- Send all your recipes to the PicoBrew\n- Send cleaning recipes to the PicoBrew\n- Session Logging\n- Session Recovery\n- Admin Web UI\n\nToDo\n\n- Session Charts\n\n# Machine Support\n- Picobrew Zymatic\n\nToDo\n- Picobrew Z Series\n- Picobrew Pico C\n\n# Disclaimer\nThis software is provided "as is" and any expressed or implied warranties are disclaimed. This software submits recipes with temperature targets to your PicoBrew machine and will cause it to heat water. Any damage to your PicoBrew machine is at your own risk.\n\nIf the Zymatic faults and the screen goes blank, DON\'T leave it powered on. The circulating pump will shut off and the heater stays on. A tube in the glycol loop may rupture.\n\n# License\n\nMIT @ Tom Herold\n',
    'author': 'Tom Herold',
    'author_email': 'heroldtom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hotzenklotz/picobrew-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
