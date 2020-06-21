# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blynclight', 'blynclight.effects', 'blynclight.hid']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'requests>=2.21,<3.0', 'typer>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['blync = blynclight.__main__:cli']}

setup_kwargs = {
    'name': 'blynclight',
    'version': '0.7.2',
    'description': 'Python language bindings for Embrava BlyncLight devices.',
    'long_description': "# `blync`\n\nControl your Embrava BlyncLight from the command-line!\n\nUse the `blync` utility to directly control your Embrava BlyncLight:\n\n\n```console\n$ blync -R        # turn the light on with red color and leave it on\n$ blync --off     # turn the light off\n$ blync -RG --dim # turn the light on with yellow color and dim\n$ blync -RBG      # turn the light on with white color\n```\n\nColors can be specified by values between 0 and 255 using the lower-case\ncolor options or using the upper-case full value options.\n\n\n```console\n$ blync -r 127                # half intensity red\n$ blync -r 255                # full intensity red\n$ blync -R                    # also full intensity red\n$ blync -r 255 -b 255 -g 255  # full intensity white\n$ blync -RBG                  # full intensity white\n```\n\n\nIf that's not enough fun, there are three builtin color modes:\n`fli`, `throbber`, and `rainbow`. All modes continue until the\nuser terminates with a Control-C or platform equivalent.\n\n\n```console\n$ blync fli\n$ blync throbber\n$ blync rainbow\n```\n\n\nInstallation\n\n\n```console\n$ python3 -m pip install blynclight\n$ python3 -m pip install git+https://github.com/JnyJny/blynclight.git # latest\n```\n\nThis module depends on [hidapi](https://github.com/libusb/hidapi), which supports\nWindows, Linux, FreeBSD and MacOS. Check your favorite package managers before\nattempting to download and build the library from source.\n\n**Usage**:\n\n```console\n$ blync [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `-l, --light-id INTEGER`: Light identifier  [default: 0]\n* `-r, --red INTEGER`: Red color value range: 0 - 255  [default: 0]\n* `-b, --blue INTEGER`: Blue color value range: 0 - 255  [default: 0]\n* `-g, --green INTEGER`: Green color value range: 0 - 255  [default: 0]\n* `-R, --RED`: Full value red [255]\n* `-B, --BLUE`: Full value blue [255]\n* `-G, --GREEN`: Full value green [255]\n* `-o, --off / -n, --on`: Turn the light off/on.  [default: False]\n* `-d, --dim`: Toggle bright/dim mode.  [default: False]\n* `-f, --flash`: Enable flash mode.\n* `-p, --play INTEGER`: Select song: 1-15\n* `--repeat`: Repeat the selected song.  [default: False]\n* `--volume INTEGER`: Set the volume: 1-10  [default: 5]\n* `-a, --list-available`\n* `-v, --verbose`\n* `-V, --version`\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `fli`: Flash Light Impressively.\n* `rainbow`: BlyncLights Love Rainbows.\n* `throbber`: BlyncLight Intensifies.\n\n## `blync fli`\n\nFlash Light Impressively.\n\nThis mode cycles light color red, blue, green and then repeats. The\nuser can specify the interval between color changes and the intesity\nof the colors. Color values specified on the command-line are ignored.\n\n\n```console\n$ blync fli -n 1      # one second between color changes\n$ blync fli -i 128    # light intensity is half as bright\n```\n\nThis mode runs until the user interrupts.\n\n**Usage**:\n\n```console\n$ blync fli [OPTIONS]\n```\n\n**Options**:\n\n* `-n, --interval FLOAT`: Seconds between flashes.  [default: 0.1]\n* `-i, --intensity INTEGER`: Integer range: 0 - 255  [default: 255]\n* `--help`: Show this message and exit.\n\n## `blync rainbow`\n\nBlyncLights Love Rainbows.\n\nSmoothly transition the color of the light using a rainbow sequence.\nThe user can slow the speed of the color cycling by adding more\n--slow options to the command line:\n\n\n```console\n$ blync rainbow -s   # slow cycling by 0.1 seconds\n$ blync rainbow -ss  # slow cycling by 0.15 seconds\n```\n\nThis mode runs until the user interrupts.\n\n**Usage**:\n\n```console\n$ blync rainbow [OPTIONS]\n```\n\n**Options**:\n\n* `-s, --slow`: Increase color cycle interval by 0.1 seconds.\n* `--help`: Show this message and exit.\n\n## `blync throbber`\n\nBlyncLight Intensifies.\n\nThis mode increases the intensity of the light color starting with\nthe specified red, green and blue values and ramping the color\nintensity up and down and repeating. The user can increase the rate\nof ramp by adding more -f options to the command line:\n\n\n```console\n$ blync throbber -f   # a little faster\n$ blync throbber -ff  # a little more faster\n$ blync -G throbber   # throb with a green color\n```\n\nThis mode runs until the user interrupts.\n\n**Usage**:\n\n```console\n$ blync throbber [OPTIONS]\n```\n\n**Options**:\n\n* `-f, --faster`: Increases speed.\n* `--help`: Show this message and exit.\n",
    'author': "Erik O'Shaughnessy",
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JnyJny/blynclight.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
