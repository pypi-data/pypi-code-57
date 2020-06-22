# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openrover', 'openrover.tests']

package_data = \
{'': ['*'], 'openrover.tests': ['resources/*']}

install_requires = \
['async_generator>=1.10,<2.0',
 'booty>=0.3.0,<0.4.0',
 'pyserial>=3.4,<4.0',
 'pytest-trio>=0.6.0,<0.7.0',
 'pytest>=5.4.2,<6.0.0',
 'trio>=0.15.1,<0.16.0']

setup_kwargs = {
    'name': 'openrover',
    'version': '1.0.0a0',
    'description': 'A Python driver for driving the Rover Robotics OpenRover Basic robot',
    'long_description': '# OpenRover Python Suite\n\nThis is the official Python driver for the [Rover Robotics](https://roverrobotics.com/) "Open Rover Basic" robot. Use this as a starting point to get up and running quickly.\n\nIncluded in this package are:\n\n1. A Python library for programmatically interfacing with the Rover over USB\n2. A command line application "`pitstop`" for upgrading and configuring the Rover firmware\n3. A test suite that confirms the Firmware and hardware are operating as expected.\n\n## Setup\n\nTo install official releases from PyPi:\n\n```shell script\npython3 -m pip install -U pip setuptools\npython3 -m pip install -U openrover --no-cache-dir\n```\n\nOn Linux, you may not have permission to access USB devices. If this is the case, run the following then restart your computer:\n\n```shell script\nsudo usermod -a -G dialout $(whoami)\n```\n\n### Development setup\n\nManual Prerequisites:\n\n* Python3 (recommended to install Python3.6, Python3.7, and Python3.8)\n* [Poetry](https://python-poetry.org/docs/#installation) \n\nInstead, we recommend:\n\n```\ngit clone https://github.com/RoverRobotics/openrover-python.git\ncd openrover-python\npoetry install\n```\n\n#### Useful commands\n\nFor testing, it is recommended to use `tox`, which can run tests on multiple Python interpreters.\n\n<dl>\n    <dt><code>pytest</code></dt>\n    <dd>Test on current Python interpreter</dd>\n    <dt><code>tox</code></dt>\n    <dd>Test on all supported Python minor versions</dd>\n    <dt><code>black .</code></dt>\n    <dd>Reformat code to a uniform style</dd>\n    <dt><code>githooks setup</code></dt>\n    <dd>Install git pre-commit hook to automatically run <code>black</code></dd>\n</dl>\n\n### Caveats\n\n* When running in PyCharm in debug mode, you will get a warning like "RuntimeWarning: You seem to already have a custom sys.excepthook handler installed ..." https://github.com/python-trio/trio/issues/1553\n* Note this is a pyproject (PEP-517) project so it will NOT work to `pip install --editable ...`\n\n\n### pitstop\n\nPitstop is a new utility to bootload your rover and set options. After installing, you can invoke it with `pitstop` or `python3 -m openrover.pitstop`.\n\n```text\n> pitstop --help\nusage: pitstop [-h] [-p port] [-f path/to/firmware.hex] [-m version]\n               [-u k:v [k:v ...]]\n\nOpenRover companion utility to bootload robot and configure settings.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p port, --port port  Which device to use. If omitted, we will search for a possible rover device\n  -f path/to/firmware.hex, --flash path/to/firmware.hex\n                        Load the specified firmware file onto the rover\n  -m version, --minimumversion version\n                        Check that the rover reports at least the given version\n                        version may be in the form N.N.N, N.N, or N\n  -u k:v [k:v ...], --updatesettings k:v [k:v ...]\n                        Send additional commands to the rover. v may be 0-255; k may be:\n                                3=SET_POWER_POLLING_INTERVAL_MS\n                                4=SET_OVERCURRENT_THRESHOLD_100MA\n                                5=SET_OVERCURRENT_TRIGGER_DURATION_5MS\n                                6=SET_OVERCURRENT_RECOVERY_THRESHOLD_100MA\n                                7=SET_OVERCURRENT_RECOVERY_DURATION_5MS\n                                8=SET_PWM_FREQUENCY_KHZ\n                                9=SET_BRAKE_ON_ZERO_SPEED_COMMAND\n                                11=SET_BRAKE_ON_DRIVE_TIMEOUT\n                                12=SET_MOTOR_SLOW_DECAY_MODE\n                                13=SET_TIME_TO_FULL_SPEED\n```\n\n### tests\n\nTo run tests, first attach the rover via breakout cable then run either `openrover-test` or `python3 -m openrover.test`.\nBy default, tests that involve running the motors will be skipped, since you may not want a rover ripping cables out of your computer. If you have made sure running the motors will not damage anything, these tests can be opted in with the flag `--motorok`.\n\n```text\n> openrover-test\n==================== test session starts =====================\nplatform win32 -- Python 3.7.3, pytest-4.3.1, py-1.8.0, pluggy-0.9.0\nrootdir: ..., inifile:\nplugins: trio-0.5.2\ncollected 32 items\n\n..\\openrover\\tests\\test_bootloader.py .s                [  6%]\n..\\openrover\\tests\\test_data.py ..                      [ 12%]\n..\\openrover\\tests\\test_find_device.py ....             [ 25%]\n..\\openrover\\tests\\test_openrover_protocol.py ....      [ 37%]\n..\\openrover\\tests\\test_rover.py .......sssss......ss   [100%]\n\n=========== 24 passed, 8 skipped in 89.14 seconds ============\n```\n\n![OpenRover Basic](https://docs.roverrobotics.com/1-manuals/0-cover-photos/1-open-rover-basic-getting-started-vga.jpg)\n',
    'author': 'Dan Rose',
    'author_email': 'dan@digilabs.io',
    'maintainer': 'Dan Rose',
    'maintainer_email': 'dan@digilabs.io',
    'url': 'https://github.com/RoverRobotics/openrover_python_driver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
