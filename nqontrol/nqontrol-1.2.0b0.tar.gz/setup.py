# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nqontrol',
 'nqontrol.general',
 'nqontrol.gui',
 'nqontrol.gui.assets',
 'nqontrol.gui.widgets',
 'nqontrol.gui.widgets.monitor_section',
 'nqontrol.gui.widgets.second_order_section',
 'nqontrol.gui.widgets.servo_section',
 'nqontrol.servo',
 'nqontrol.servodevice']

package_data = \
{'': ['*']}

install_requires = \
['ADwin>=0.16.2,<0.17.0',
 'Flask>=1.1.2,<2.0.0',
 'dash>=1.11.0,<1.12.0',
 'dash_daq>=0.5.0,<0.6.0',
 'fastnumbers>=3.0.0,<4.0.0',
 'gunicorn>=20.0.4,<21.0.0',
 'jsonpickle>=1.4,<2.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.14,<2.0',
 'openqlab>=0.1.13,<0.2.0',
 'pandas-datareader>=0.5.0,<0.6.0',
 'pandas>=1.0,<2.0',
 'plotly>=4.3,<4.4',
 'scipy>=1.0,<2.0',
 'websocket_client>=0.57.0,<0.58.0']

extras_require = \
{':python_version <= "3.7"': ['importlib-metadata>=1.6,<2.0']}

entry_points = \
{'console_scripts': ['nqontrol = nqontrol.gui.gunirun:main']}

setup_kwargs = {
    'name': 'nqontrol',
    'version': '1.2.0b0',
    'description': 'Python program for digital control-loops.',
    'long_description': '# NQontrol Servo Controller\n\n[![pipeline status](https://gitlab.com/las-nq/nqontrol/badges/master/pipeline.svg)](https://gitlab.com/las-nq/nqontrol/commits/master)\n[![coverage report](https://gitlab.com/las-nq/nqontrol/badges/master/coverage.svg)](https://gitlab.com/las-nq/nqontrol/commits/master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n<img src="doc/_static/system_overview.png" align="right">\n\n`NQontrol` is a Python project aiming the replacement of analog PID controllers in the lab.\n\nThe project is a solution based on the ADwin real-time platform that is able to deliver in excess of 8 simultaneous locking loops running with 200 kHz sampling frequency, and offers five second-order filtering sections per channel for optimal control performance. \nIt can be used up to a control bandwidth of about 12 kHz.\nThis Python package, together with a web-based GUI, makes the system easy to use and adapt for a wide range of control tasks in quantum-optical experiments.\n\nThe source code can be found on [GitLab](https://gitlab.com/las-nq/nqontrol).\n\nRead the latest changes in our [changelog](CHANGELOG.md).\n\n\n## Paper Version\n\nA fixed state of this project is [version 1.1](https://gitlab.com/las-nq/nqontrol/tree/v1.1).\nThe publicated paper about this project is available [here](https://doi.org/10.1063/1.5135873).\nThe preprint version of the paper describing can be found on [arXiv](https://arxiv.org/abs/1911.08824).\n\n\n## Usage Example\n\nHere is a short example for the Python API (see the [full example](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/usage.html) in the docs):\n\n```python\n# Importing a ServoDevice is enough\nfrom nqontrol import ServoDevice\n\n# Create a new servo device object, connecting to ADwin with the device number 0.\n# Number 0 is reserved for a virtual mock device for testing.\nsd = ServoDevice(0)\n\n# Print the timestamp\nprint(f\'Uptime {sd.timestamp}s\')\n\n# Get a servo object to control it.\ns = sd.servo(1)\n\n# Enable in and output\ns.inputSw = True\ns.outputSw = True\n\n# Run a threshold analysis for locking\ns.lockAnalysis()\n# Enable the autolock\ns.autolock(relock=True)\n```\n\n\n## Graphical User Interface\n\n`NQontrol` can also be used with a responsive graphical user interface that runs in a browser (more details in the [docs](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/gui.html)):\n\n![NQontrol GUI](doc/_static/entry.png)\n\n\n## Autolock Feature\n\nAn [autolock feature](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/features.html#autolock) makes it simple to lock all the control loops.\nIt scans the output until a threshold value of the `aux` signal is reached, then it activates the lock.\n\n\n## Documentation\n\nFor more information please read the online documentation:\n\n* Current documentation of the [latest release](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol)\n* Current documentation of the [latest development version](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol)\n\n\n## NQontrol Installation\n\nIt\'s as simple as\n```bash\npip install nqontrol\n```\nBut additionally you need to install the ADwin library.\nFor complete installation instructions please refer to the [documentation page](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/install.html).\n\n\n## Contribution\n\nIf you want to make changes for yourself or contribute to the project, take a look on [this page](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/dev_install.html) to see how to setup the environment.\n',
    'author': 'Christian Darsow-Fromm',
    'author_email': 'cdarsowf@physnet.uni-hamburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/las-nq/nqontrol',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
