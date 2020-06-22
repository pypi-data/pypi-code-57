# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['charmonium', 'charmonium.time_block']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.7.0,<6.0.0']

entry_points = \
{'console_scripts': ['time_block = charmonium.time_block._cli:main']}

setup_kwargs = {
    'name': 'charmonium.time-block',
    'version': '0.2.0',
    'description': 'Time a block of code.',
    'long_description': '=====================\ncharmonium.time_block\n=====================\n\nA decorator and a context-manager (with-statment) to time a block of\ncode.\n\n\nQuickstart\n----------\n\n::\n\n    $ pip install charmonium.time_block\n\n.. code:: python\n\n    >>> import charmonium.time_block as ch_time_block\n    >>> ch_time_block._enable_doctest_logging()\n    >>> import time\n    >>>\n    >>> def foo():\n    ...     with ch_time_block.ctx("bar"):\n    ...         time.sleep(0.1)\n    ...\n    >>> foo()\n     > bar: running\n     > bar: 0.1s\n\nEquivalent context-manager:\n\n.. code:: python\n\n\n    >>> import charmonium.time_block as ch_time_block\n    >>> ch_time_block._enable_doctest_logging()\n    >>>\n    >>> def foo():\n    ...     bar()\n    ...\n    >>>\n    >>> @ch_time_block.ctx("bar")\n    ... def bar():\n    ...     time.sleep(0.1)\n    ...\n    >>> foo()\n     > bar: running\n     > bar: 0.1s\n\n`line_prof`_ is extremely detailed and complex, which makes it more\nappropriate when you don\'t know what to measure, whereas this package\nis more appropriate when you already know the bottleneck, and just\nwant to see how slow a few functions/blocks are.\n\n.. _`line_prof`: https://github.com/rkern/line_profiler\n\nUnlike external profiling, this package reports in realtime to\n`logger`_ (destination customizable). This is intended to let the user\nknow what the code is doing right now.\n\n.. _`logger`: https://docs.python.org/3.9/library/logging.html\n\n::\n\n     > download: running\n     > download: 0.1s\n     > processing: running\n     > processing > decompress: running\n     > processing > decompress: 0.2s\n     > processing: 0.4s\n\nSince this plugs into Python\'s\n`logger`_ infrastructure, this can feed a pipeline that checks the\napplication health (e.g. ensuring a microservice is responsive).\n\n.. _`logger`: https://docs.python.org/3.9/library/logging.html\n\nThis records process\'s increase in memory usage (relatively\ncross-platform method using `psutil`_) when ``do_gc=True``, which\ngives a rough estimate of the memory leaked by the block.\n\n.. _`psutil`: https://github.com/giampaolo/psutil\n\nLike function profiling, but unlike other block-profilers, it is\nrecurrent, and it maintains a stack.\n\n.. code:: python\n\n    >>> import charmonium.time_block as ch_time_block\n    >>> ch_time_block._enable_doctest_logging()\n    >>> import time\n    >>>\n    >>> @ch_time_block.decor()\n    ... def foo():\n    ...     time.sleep(0.1)\n    ...     bar()\n    ...\n    >>>\n    >>> @ch_time_block.decor()\n    ... def bar():\n    ...     time.sleep(0.2)\n    ...     with ch_time_block.ctx("baz"):\n    ...         time.sleep(0.3)\n    ...\n    >>> foo()\n     > foo: running\n     > foo > bar: running\n     > foo > bar > baz: running\n     > foo > bar > baz: 0.3s\n     > foo > bar: 0.5s\n     > foo: 0.6s\n\nThis handles recursion. Handling recursion any other way would break\nevaluating self / parent, because parent could be self.\n\n.. code:: python\n\n    >>> import charmonium.time_block as ch_time_block\n    >>> ch_time_block._enable_doctest_logging()\n    >>> import time\n    >>>\n    >>> @ch_time_block.decor(print_args=True)\n    ... def foo(n):\n    ...     if n != 0:\n    ...         time.sleep(0.1)\n    ...         return foo(n - 1)\n    ...\n    >>> foo(2)\n     > foo(2): running\n     > foo(2) > foo(1): running\n     > foo(2) > foo(1) > foo(0): running\n     > foo(2) > foo(1) > foo(0): 0.0s\n     > foo(2) > foo(1): 0.1s\n     > foo(2): 0.2s\n\nThis even works for threads (or more usefully `ThreadPoolExecutor`_).\n\n.. _`ThreadPoolExecutor`: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor\n\n.. code:: python\n\n    >>> import charmonium.time_block as ch_time_block\n    >>> ch_time_block._enable_doctest_logging()\n    >>> import time\n    >>> from concurrent.futures import ThreadPoolExecutor\n    >>>\n    >>> @ch_time_block.decor()\n    ... def foo():\n    ...     time.sleep(0.1)\n    ...     baz()\n    ...\n    >>> @ch_time_block.decor()\n    ... def bar():\n    ...     time.sleep(0.2)\n    ...     baz()\n    ...\n    >>> @ch_time_block.decor()\n    ... def baz():\n    ...     return time.sleep(0.3)\n    ...\n    >>> from threading import Thread\n    >>> threads = [Thread(target=foo), Thread(target=bar)]\n    >>> for thread in threads: # doctest:+SKIP\n    ...     thread.start()\n    ...\n     > foo: running\n     > bar: running\n     > foo > baz: running\n     > bar > baz: running\n     > foo > baz: 0.3s\n     > foo: 0.4s\n     > bar > baz: 0.3s\n     > bar: 0.5s\n    >>> # TODO: get a better example, with named threads\n\nThe results are programatically accessible at runtime. In the dict\nreturned by ``get_stats()``, the stack frame (key) is represented as a\ntuple of strings while the profile result (value) is a pair of time\nand memory used.\n\n.. code:: python\n\n    >>> import charmonium.time_block as ch_time_block\n    >>> ch_time_block._enable_doctest_logging()\n    >>> ch_time_block.clear()\n    >>> import time\n    >>>\n    >>> @ch_time_block.decor()\n    ... def foo():\n    ...     time.sleep(0.1)\n    ...     bar()\n    ...\n    >>>\n    >>> @ch_time_block.decor()\n    ... def bar():\n    ...     time.sleep(0.2)\n    ...\n    >>> foo()\n     > foo: running\n     > foo > bar: running\n     > foo > bar: 0.2s\n     > foo: 0.3s\n    >>> ch_time_block.get_stats() # doctest:+SKIP\n    {(\'foo\', \'bar\'): [(0.200505, 0)], (\'foo\',): [(0.301857, 0)]}\n    >>> ch_time_block.print_stats() # doctest:+SKIP\n    foo       =  100% of total =  100% of parent = (0.30 +/- 0.00) sec = 1 (0.30 +/- 0.00) sec  (0.0 +/- 0.0) b\n    foo > bar =  100% of total =   67% of parent = (0.20 +/- 0.00) sec = 1 (0.20 +/- 0.00) sec  (0.0 +/- 0.0) b\n\nUnlike external profiling, This does not need source-code access, so it will work from ``.eggs``.\n',
    'author': 'Samuel Grayson',
    'author_email': 'sam+dev@samgrayson.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/charmoniumQ/charmonium.time_block.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
