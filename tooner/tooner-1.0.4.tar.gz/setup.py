# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tooner']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tooner',
    'version': '1.0.4',
    'description': 'An easier way to manage and launch sessions for Toontown Rewritten.',
    'long_description': 'An easier way to manage and launch sessions for [Toontown Rewritten](https://toontownrewritten.com).\n\n# What does it do?\n\nCurrently, **tooner** allows you to communicate with Toontown Rewritten\'s login API in order to log in and start a session with very few lines of code.\n\n```python\nlauncher = tooner.ToontownLauncher(directory="...")\nlauncher.play(username="username", password="password")\n```\n\nIf you\'re crazy, you can even combine these lines into one!\n\nAll you have to do is supply the directory of your Toontown Rewritten installation (where the TTREngine is stored) and your login information. On Windows, check your program files directories. On MacOS, this is in your Application Support directory. Eventually, I\'d like to make this library automatically find the installation.\n\nThe best part is that you can do this to **play multiple toons at once**.\n\n# Why does this exist?\n\nSince I normally play on MacOS, there is no way for me to open multiple sessions of the Toontown Rewritten launcher without doing it from the terminal; this was really annoying to do every time I wanted to multitoon (which is a lot), so I set out to make this easier.\n\nUltimately, I was successful in making this functionality work the three major operating systems: Windows, MacOS, and, I assume, on Linux (I haven\'t been able to test this).\n\n# How do I get it?\n\nIt\'s easiest to simply install the package via pip using the following command:\n\n```\npip install tooner\n```\n\nOtherwise, you can close this repository using the command\n\n```\ngit clone https://github.com/jakebrehm/tooner.git\n```\n\nand then you can do whatever you want with it!\n\n# Future improvements\n\nThe most pressing major improvement that could be made is **adding support for ToonGuard**. The only problem is writing it in such a way that makes sense while keeping in mind *tooner*\'s two-line launcher paradigm, as it would require the user to enter a code *after* having run the script.\n\n# Projects using **tooner**\n\nThe following projects are using **tooner**:\n1. [MultiTooner](https://github.com/jakebrehm/multitooner) by [Jake Brehm](https://github.com/jakebrehm)\n\n# Authors\n\n- **Jake Brehm** - *Initial Work* - [Email](mailto:mail@jakebrehm.com) | [Github](http://github.com/jakebrehm) | [LinkedIn](http://linkedin.com/in/jacobbrehm)',
    'author': 'Jake Brehm',
    'author_email': 'mail@jakebrehm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
