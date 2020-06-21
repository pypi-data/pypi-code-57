# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['context_logging']

package_data = \
{'': ['*']}

install_requires = \
['contextvars_executor>=0.0.1,<0.0.2',
 'deprecated>=1.2.10,<2.0.0',
 'pydantic>=1,<2']

setup_kwargs = {
    'name': 'context-logging',
    'version': '1.1.0',
    'description': 'Tool for easy logging with current context information',
    'long_description': "# context_logging\n\n[![pypi](https://badge.fury.io/py/context_logging.svg)](https://pypi.org/project/context_logging)\n[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://pypi.org/project/context_logging)\n[![Downloads](https://img.shields.io/pypi/dm/context_logging.svg)](https://pypistats.org/packages/context_logging)\n![CI Status](https://github.com/afonasev/context_logging/workflows/ci/badge.svg?branch=master)\n[![Code coverage](https://codecov.io/gh/Afonasev/context_logging/branch/master/graph/badge.svg)](https://codecov.io/gh/Afonasev/context_logging)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n## Description\n\nTool for easy logging with current context information.\n\n```python\nfrom context_logging import current_context\n\nlogging.info('before context')\n# 2019-07-25 19:49:43 INFO before context\n\nwith Context('my_context'):\n    current_context['var'] = 1\n    logging.info('in context')\n    # 2019-07-25 19:49:43 INFO in context {'var': 1}\n\n# 2019-07-25 19:49:43 INFO 'my_context: executed in 00:00:01 {'var': 1}'\n\nlogging.info('after context')\n# 2019-07-25 19:49:43 INFO after context\n```\n\n## Installation\n\n    pip install context_logging\n\n## Usage\n\n### Setup logging with context\n\n```python\nimport logging\nfrom context_logging import current_context, setup_log_record\n\nlogging.basicConfig(\n    format='%(asctime)s %(levelname)s %(name)s %(message)s %(context)s',\n    level=logging.INFO,\n)\nsetup_log_record()\n\ncurrent_context['var'] = 1\nlogging.info('message')\n\n# 2019-07-25 19:49:43,892 INFO root message {'var': 1}\n```\n\n### As contextmanager\n\n```python\nfrom context_logging import Context, current_context\n\nwith Context(var=1):\n    assert current_context['var'] == 1\n\nassert 'var' not in current_context\n```\n\n### Any nesting of contexts is allowed\n\n```python\nwith Context(var=1):\n    assert current_context == {'var': 1}\n\n    with Context(val=2, var=2):\n        assert current_context == {'val': 2, 'var': 2}\n\n    assert current_context == {'var': 1}\n\nassert 'var' not in current_context\n```\n\n### As decorator\n\n```python\n@Context(var=1)\ndef f():\n    assert current_context['var'] == 1\n\nf()\nassert 'var' not in current_context\n```\n\n### With start/finish [DEPRECATED]\n\n```python\nctx = Context(var=1)\nassert 'var' not in current_context\n\nctx.start()\nassert current_context['var'] == 1\n\nctx.finish()\nassert 'var' not in current_context\n```\n\n### Add/remove values from current_context\n```python\nwith Context():\n    assert 'var' not in current_context\n    current_context['var'] = 1\n    assert current_context['var'] == 1\n```\n\n### Explicit context name (else will be used path to the python module)\n\n```python\nwith Context('my_context'):\n    pass\n```\n\n### Execution time logged on exit from context (it can be disabled with `log_execution_time=False` argument)\n\n```python\nwith Context('my_context'):\n    time.sleep(1)\n\n# INFO 'my_context: executed in 00:00:01',\n```\n\nDefault value for log_execution_time param can be changed with env\n\n    export CONTEXT_LOGGING_LOG_EXECUTION_TIME_DEFAULT=0\n\n### Exceptions from context are populated with current_context (it can be disabled with `fill_exception_context=False` argument)\n\n```python\ntry:\n    with Context(var=1):\n        raise Exception(1)\nexcept Exception as exc:\n    assert exc.args = (1, {'var': 1})\n```\n\nDefault value for fill_exception_context param can be changed with env\n\n    export CONTEXT_LOGGING_FILL_EXEPTIONS_DEFAULT=0\n\n### We can set data to root context that never will be closed\n\n```python\nfrom context_logging import root_context\n\nroot_context['env'] = 'test'\n```\n\n### If you want to pass context to other threads use [ContextVarExecutor](https://github.com/hellysmile/contextvars_executor)\n\n```python\nfrom context_logging import ContextVarExecutor\n\nwith ContextVarExecutor() as executor:\n    executor.submit(...)\n\n# OR\n\nloop.set_default_executor(ContextVarExecutor())  # for asyncio loop\n```\n\n## For developers\n\n### Create venv and install deps\n\n    make init\n\n### Install git precommit hook\n\n    make precommit_hook\n\n### Run linters, autoformat, tests etc.\n\n    make pretty lint test\n\n### Bump new version\n\n    make bump_major\n    make bump_minor\n    make bump_patch\n",
    'author': 'Evgeniy Afonasev',
    'author_email': 'ea.afonasev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/context_logging',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
