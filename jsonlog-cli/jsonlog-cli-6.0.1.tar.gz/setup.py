# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonlog_cli', 'jsonlog_cli.tests']

package_data = \
{'': ['*']}

install_requires = \
['click', 'jsonlog', 'pydantic', 'typing-extensions', 'xdg']

entry_points = \
{'console_scripts': ['jsonlog = jsonlog_cli.cli:main']}

setup_kwargs = {
    'name': 'jsonlog-cli',
    'version': '6.0.1',
    'description': 'Convert structured JSON logs to human-readable output',
    'long_description': 'jsonlog-cli\n===========\n\nA human readable formatter for JSON logs.\n \nIt\'s built for use with [jsonlog] but will work well with any log format that\nuses line delimited JSON.\n\n![Example output](https://raw.githubusercontent.com/borntyping/jsonlog-cli/master/docs/example.png)\n\nUsage\n-----\n\nSee `jsonlog --help` for all options.\n\n### Key-value mode\n\nPass a file as the only argument to `jsonlog`, or read from STDIN by default.\n\n```bash\njsonlog kv docs/example.log\n```\n\n```bash\npython docs/example.py | jsonlog kv\n```\n\n```bash\ncat docs/example.log | jsonlog\n```\n\nOnly show the `timestamp` and `message` fields:\n\n```bash\njsonlog kv --key timestamp --key message docs/example.log\n```\n\nConfigure the keys of multiline values you want to display (can be specified\nmultiple times, and defaults to the `traceback` key.)\n\n```bash\njsonlog kv --key timestamp --key message --multiline-key traceback docs/example.log\n```\n\nConfigure the key to extract and use as the records level, controlling the\ncolour each line is printed in (defaults to the `level` key).\n\n```bash\njsonlog kv --level-key level --key timestamp --key message --multiline-key traceback docs/example.log\n```\n\n### Template mode\n\nOnly show the `timestamp` and `message` fields:\n\n```bash\njsonlog template --format "{timestamp} {message}" docs/example.log\n```\n\nAlso show a multiline key when it\'s present:\n\n```bash\njsonlog template --format "{timestamp} {message}" --multiline-key traceback docs/example.log\n```\n\nConfiguration\n-------------\n\nNamed "patterns" are supported as a way of collecting a set of options for\njsonlog\'s key-value and template modes. If `~/.config/jsonlog/config.json`\nexists, it will be loaded at startup. All fields should be optional.\n\nThe example configuration file below creates patterns named `basic` and\n`comprehensive` for the key-value and template modes. The patterns will each\nshow the `timestamp` and `message` fields of incoming logs. The patterns\nnamed `comprehensive` override all fields, setting their their default values.\n\nCreating a pattern named `default` will set the default options used if no\npattern is specified. Command line options always override options from the\napplication\'s default configuration, the configuration file and the selected\npattern.  \n\n```json\n{\n  "keyvalues": {\n    "basic": {\n      "priority_keys": ["timestamp", "message"]\n    },\n    "comprehensive": {\n      "level_key": "level",\n      "multiline_json": false,\n      "multiline_keys": [],\n      "priority_keys": [],\n      "removed_keys": []\n    }\n  },\n  "templates": {\n    "basic": {\n      "format": "{timestamp} {message}"\n    },\n    "comprehensive": {\n      "level_key": "level",\n      "multiline_json": false,\n      "multiline_keys": [],\n      "format": "{timestamp} {message}" \n    }\n  }\n}\n```\n\nThe `multiline_json` option will parse incoming data using a buffer. This is\nrarely useful, but some applications (e.g. ElasticSearch) output JSON split \nacross multiple lines. Incoming data will be buffered until the whole buffer can\nbe parsed as JSON or a new line starts with `{`. Incoming lines that can be\nimmediately parsed as JSON are not buffered (flushing the buffer first). \n\nAuthors\n-------\n\n* [Sam Clements]\n\n[jsonlog]: https://github.com/borntyping/jsonlog\n[Sam Clements]: https://gitlab.com/borntyping\n',
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
