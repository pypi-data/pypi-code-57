# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brooks_mfc']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=2.3.10,<3.0.0']

entry_points = \
{'console_scripts': ['brooks-mfc = brooks_mfc:command_line']}

setup_kwargs = {
    'name': 'brooks-mfc',
    'version': '0.1.1',
    'description': 'Python driver for Brooks Instrument mass flow controllers',
    'long_description': 'brooks-mfc\n==========\n\nPython driver and command-line tool for [Brooks Instrument mass flow controllers](https://www.brooksinstrument.com/en/products/mass-flow-controllers).\n\n<p align="center">\n  <img height="250" src="https://www.brooksinstrument.com/~/media/brooks/images/products/mass%20flow%20controllers/metal%20sealed/gf100/gf100-gf120-gf125-mass-flow-controller-3-491px.png" />\n</p>\n\nInstallation\n============\n\n```\npip install brooks-mfc\n```\n\nUsage\n=====\n\nThis driver uses an undocumented REST API in the devices\'s web interface for communication.\nThe compatibility and stability of this interface with all Brooks controllers is not guaranteed.\n\n### Command Line\n\nTo test your connection and stream real-time data, use the command-line\ninterface. You can read the flow rate with:\n\n```\n$ brooks-mfc 192.168.1.200\n{\n    "Customer Flow Totalizer": 0.0,\n    "Flow": -0.3,\n    "Flow Hours": 1.0,\n    "Flow Totalizer": 0.0,\n    "Live Setpoint": 0.0,\n    "Operational Hours": 50.0,\n    "Setpoint": 0.0,\n    "Supply Voltage": 22.93,\n    "Temperature": 27.11,\n    "Valve Position": 0.0\n}\n```\n\nYou can optionally specify a setpoint flow with the set flag:\n`brooks-mfc 192.168.1.150 --set 7.5.` The units of the setpoint and return are\nspecified using the `--units` flag. See `mfc --help` for more.\n\n### Python\n\nThis uses Python ≥3.5\'s async/await syntax to asynchronously communicate with\nthe mass flow controller. For example:\n\n```python\nimport asyncio\nfrom brooks_mfc import FlowController\n\nasync def get():\n    async with FlowController(\'the-mfc-ip-address\') as fc:\n        print(await fc.get())\n\nasyncio.run(get())\n```\n\nThe API that matters is `get`, `set`. Optionally, units can be passed with \neither command. If no units are specified the existing units configured for\nthe device are used.\n\n```python\n>>> await fc.get()\n>>> await fc.get(\'%\')\n{\n    "Customer Flow Totalizer": 0.0,\n    "Flow": -0.3,\n    "Flow Hours": 1.0,\n    "Flow Totalizer": 0.0,\n    "Live Setpoint": 0.0,\n    "Operational Hours": 50.0,\n    "Setpoint": 0.0,\n    "Supply Voltage": 22.93,\n    "Temperature": 27.11,\n    "Valve Position": 0.0\n}\n```\n```python\n>>> await fc.set(10)\n>>> await fc.set(10, \'SCCM\')\n```\n\nThere\'s much more that could be set or returned from the flow controllers but \nI haven\'t had a reason to flesh all the the options out. Feel free to submit an \nissue with requests or a PR.\n',
    'author': 'jamesjeffryes',
    'author_email': 'jamesgjeffryes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/numat/brooks_mfc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
