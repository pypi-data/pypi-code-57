# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonlog_cli', 'jsonlog_cli.tests']

package_data = \
{'': ['*']}

install_requires = \
['click', 'jsonlog', 'jsonschema', 'xdg']

entry_points = \
{'console_scripts': ['jsonlog = jsonlog_cli.cli:main']}

setup_kwargs = {
    'name': 'jsonlog-cli',
    'version': '5.1.0',
    'description': 'Convert structured JSON logs to human-readable output',
    'long_description': 'jsonlog-cli\n===========\n\nA human readable formatter for JSON logs.\n \nIt\'s built for use with [jsonlog] but will work well with any log format that\nuses line delimited JSON.\n\n![Example output](https://raw.githubusercontent.com/borntyping/jsonlog-cli/master/docs/example.png)\n\nUsage\n-----\n\nPass a file as the only argument to `jsonlog`, or read from STDIN by default.\n\n```bash\njsonlog docs/example.log\n```\n\n```bash\npython docs/example.py | jsonlog\n```\n\nConfiguration\n-------------\n\nSee `jsonlog --help` for all options.\n\nOnly show timestamps and messages (defaults to `{timestamp} {level} {name} {message}`).\n\n```bash\njsonlog --format "{timestamp} {message}" docs/example.log\n```\n\nConfigure the keys of multiline values you want to display (can be specified\nmultiple times, and defaults to the `traceback` key.)\n\n```bash\njsonlog --format "{timestamp} {message}" docs/example.log\n```\n\nConfigure the key to extract and use as the records level, controlling the\ncolour each line is printed in (defaults to the `level` key).\n\n```bash\njsonlog --format "{timestamp} {message}" docs/example.log\n```\n\nAuthors\n-------\n\n* [Sam Clements]\n\n[jsonlog]: https://github.com/borntyping/jsonlog\n[Sam Clements]: https://gitlab.com/borntyping\n',
    'author': 'Sam Clements',
    'author_email': 'sam@borntyping.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/borntyping/jsonlog/tree/master/jsonlog-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
