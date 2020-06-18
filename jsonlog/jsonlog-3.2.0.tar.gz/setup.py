# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonlog', 'jsonlog.tests']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses']

setup_kwargs = {
    'name': 'jsonlog',
    'version': '3.2.0',
    'description': 'JSON formatter for the builtin logging module',
    'long_description': 'jsonlog\n=======\n\nA drop-in formatter for Python\'s `logging` module that outputs messages as line\ndelimited JSON.\n\nWhile `jsonlog` provides it\'s own `basicConfig` method so you can get started\nquickly, all of it\'s features and classes can be used with the `logging` module.\n\nUsage\n-----\n\nYou can use `jsonlog` as a drop-in replacement for `logging`:\n\n```python\nimport jsonlog\n\njsonlog.warning("Hello world.")\n```\n\n```json\n{"timestamp": "2019-06-21T19:06:25.285730", "level": "WARNING", "name": "root", "message": "Hello world."}\n```\n\nIt\'s implemented as a log formatter, so you can use `logging` just like you\nnormally would.\n\n```python\nimport jsonlog\nimport logging\n\njsonlog.basicConfig(level=jsonlog.INFO)\njsonlog.warning("Works with functions in the jsonlog module.")\nlogging.warning("And works with functions in the logging module.")\n```\n\n### Configuration using `jsonlog.basicConfig`\n\nThe `jsonlog.basicConfig` function accepts slightly different parameters to\n`logging.basicConfig`. It\'s shown here with the defaults for each parameter.\n\nThe `filename`, `filemode` and `stream` parameters work the same way as their\nequivalents in `logging.basicConfig`, and as such `filename` and `stream` are\nexclusive.\n\n```python\nimport jsonlog\n\njsonlog.basicConfig(\n    level=jsonlog.INFO,\n    indent=None,\n    keys=("timestamp", "level", "message"),\n    timespec="auto",\n    # filename=None,\n    # filemode="a",\n    # stream=None,\n)\n```\n\n### Configuration using `logging.config.dictConfig`\n\nAny of the configuration methods in `logging.config` can be used to configure a\nhandler that uses `jsonlog.formmatters.JSONFormatter` to format records as JSON.\n\n```python\nimport logging.config\n\nlogging.config.dictConfig(\n    {\n        "version": 1,\n        "formatters": {"json": {"()": "jsonlog.JSONFormatter"}},\n        "handlers": {"stream": {"class": "logging.StreamHandler", "formatter": "json"}},\n        "loggers": {"": {"handlers": ["stream"]}},\n    }\n)\n```\n\n### Adding extra attributes to JSON output\n\nRecord attributes provided with `extra=` will be included in the JSON object.\n\n```python\nimport jsonlog\nimport logging\n\njsonlog.basicConfig()\nlogging.warning("User clicked a button", extra={"user": 123})\n```\n\n```json\n{"timestamp": "2019-06-21T19:06:54.293929", "level": "WARNING", "name": "root", "message": "User clicked a button", "user": 123}\n```\n\nIf a mapping is passed as the only positional argument, attributes from the\nmapping will also be included.\n\n```python\nimport jsonlog\nimport logging\n\njsonlog.basicConfig()\nlogging.warning("User clicked a button", {"user": 123})\n```\n\n### Pipelining\n\nTry piping logs through [jq] if you want to read them on the command line!\n\n```bash\npython examples/hello.py 2> >(jq .)\n```\n\n```json\n{\n  "timestamp": "2019-06-21T19:07:43.211782",\n  "level": "WARNING",\n  "name": "root",\n  "message": "Hello world."\n}\n\n```\n\n### Tracebacks\n\nTracebacks are included as a single string - it\'s not very nice to read, but\nmeans it\'ll play nicely with any systems that read the JSON logs you output.\n\n```json\n{"timestamp": "2019-06-21T19:08:37.326897", "level": "ERROR", "name": "root", "message": "Encountered an error", "traceback": "Traceback (most recent call last):\\n  File \\"examples/error.py\\", line 6, in <module>\\n    raise ValueError(\\"Example exception\\")\\nValueError: Example exception"}\n```\n\nTools like [jq] make it easy to extract and read the traceback:\n\n```bash\npython examples/error.py 2> >(jq -r ".traceback")\n```\n\n```\nTraceback (most recent call last):\n  File "examples/error.py", line 6, in <module>\n    raise ValueError("Example exception")\nValueError: Example exception\n```\n\nCompatibility\n-------------\n\n`jsonlog` is written for Python 3.6 and above. Compatibility patches will be\naccepted for Python 3.5 and above, but patches for Python 2 will be rejected.\n\nReferences\n----------\n\n* Build for use with the [logging] module.\n* Partially based on [colorlog].\n* Works great with [jq]!\n\nAuthors\n-------\n\n* [Sam Clements]\n\n[colorlog]: https://gitlab.com/borntyping/colorlog\n[jq]: https://stedolan.github.io/jq/\n[logging]: https://docs.python.org/3/library/logging.html\n[Sam Clements]: https://gitlab.com/borntyping\n',
    'author': 'Sam Clements',
    'author_email': 'sam@borntyping.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/borntyping/jsonlog/tree/master/jsonlog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
